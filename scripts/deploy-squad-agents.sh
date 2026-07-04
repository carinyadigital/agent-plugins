#!/usr/bin/env bash
# deploy-squad-agents.sh — apply carinyaparc instance deployments to cloud platforms.
#
# Usage:
#   ./scripts/deploy-squad-agents.sh --dry-run --instance ../carinyaparc
#   ./scripts/deploy-squad-agents.sh apply --instance ../carinyaparc
#   ./scripts/deploy-squad-agents.sh apply --ritual weekly-planning --dry-run-first --instance ../carinyaparc
#   ./scripts/deploy-squad-agents.sh pause|resume --id weekly-planning-product-manager --instance ../carinyaparc
#   ./scripts/deploy-squad-agents.sh apply --run-now --ritual weekly-planning --instance ../carinyaparc
#
# Reads:  {instance}/config/deployments/*.json
#         {instance}/config/cadence/{ritual}.md
#         managed-agents/{agent}/agent.yaml
#
# Secrets (env): CURSOR_API_TOKEN, ANTHROPIC_ADMIN_KEY — never stored in repo.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CATALOGUE_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

INSTANCE_PATH=""
MODE="dry-run"
RITUAL_FILTER=""
DEPLOYMENT_ID=""
DRY_RUN_FIRST=false
RUN_NOW=false

usage() {
  sed -n '2,12p' "$0"
  exit "${1:-0}"
}

resolve_instance() {
  local raw="${1:-}"
  if [[ -z "$raw" ]]; then
    echo "error: --instance <path> is required (carinyaparc repo root)" >&2
    exit 1
  fi
  if [[ -d "$raw" ]]; then
    cd "$raw" && pwd
  else
    cd "$raw" 2>/dev/null && pwd || {
      echo "error: instance path not found: $raw" >&2
      exit 1
    }
  fi
}

sha256_file() {
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$1" | awk '{print $1}'
  else
    sha256sum "$1" | awk '{print $1}'
  fi
}

resolve_platform() {
  local cookbook_platform="$1"
  local deployment_platform="$2"
  if [[ "$deployment_platform" != "null" && -n "$deployment_platform" ]]; then
    echo "$deployment_platform"
    return
  fi
  if [[ "$cookbook_platform" == "either" ]]; then
    if [[ -n "${CURSOR_API_TOKEN:-}" ]]; then
      echo "cursor"
    elif [[ -n "${ANTHROPIC_ADMIN_KEY:-}" ]]; then
      echo "claude-cma"
    else
      echo "either"
    fi
    return
  fi
  echo "$cookbook_platform"
}

validate_instance() {
  local instance="$1"
  if [[ ! -f "${instance}/config/instance.json" ]]; then
    echo "error: missing ${instance}/config/instance.json" >&2
    exit 1
  fi
  if [[ ! -d "${instance}/config/deployments" ]]; then
    echo "error: missing ${instance}/config/deployments/" >&2
    exit 1
  fi
  if command -v python3 >/dev/null 2>&1 && [[ -f "${instance}/scripts/validate-deployments.py" ]]; then
    python3 "${instance}/scripts/validate-deployments.py" "$instance" || exit 1
  fi
}

list_deployments() {
  local instance="$1"
  local ritual="$2"
  find "${instance}/config/deployments" -maxdepth 1 -name '*.json' -print | sort
}

deployment_enabled() {
  local file="$1"
  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print('true' if d.get('enabled', True) else 'false')" "$file"
}

deployment_field() {
  local file="$1"
  local field="$2"
  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); v=d.get(sys.argv[2]); print('' if v is None else v)" "$file" "$field"
}

plan_deployment() {
  local instance="$1"
  local deploy_file="$2"
  local agent ritual squad platform resolved_platform repos_json schedule_json enabled
  local cookbook ritual_file ritual_hash cookbook_platform

  agent="$(deployment_field "$deploy_file" agent)"
  ritual="$(deployment_field "$deploy_file" ritual)"
  squad="$(deployment_field "$deploy_file" squad)"
  platform="$(deployment_field "$deploy_file" platform)"
  enabled="$(deployment_enabled "$deploy_file")"
  if [[ "$enabled" == "true" ]]; then
    enabled_bool="true"
  else
    enabled_bool="false"
  fi

  cookbook="${CATALOGUE_ROOT}/managed-agents/${agent}/agent.yaml"
  if [[ ! -f "$cookbook" ]]; then
    echo "error: missing cookbook for agent '${agent}': ${cookbook}" >&2
    exit 1
  fi

  cookbook_platform="$(python3 -c "
import re, pathlib, sys
text = pathlib.Path(sys.argv[1]).read_text()
m = re.search(r'^platform:\s*(\S+)', text, re.M)
print(m.group(1) if m else '')
" "$cookbook")"

  resolved_platform="$(resolve_platform "$cookbook_platform" "$platform")"

  repos_json="$(python3 -c "import json; print(json.dumps(json.load(open('$deploy_file')).get('repos', [])))")"
  schedule_json="$(python3 -c "import json; print(json.dumps(json.load(open('$deploy_file')).get('schedule', {})))")"

  ritual_file=""
  ritual_hash="null"
  if [[ "$ritual" != "null" && -n "$ritual" ]]; then
    ritual_file="${instance}/config/cadence/${ritual}.md"
    if [[ ! -f "$ritual_file" ]]; then
      echo "error: missing ritual ${ritual_file}" >&2
      exit 1
    fi
    ritual_hash="$(sha256_file "$ritual_file")"
  fi

  local deploy_id
  deploy_id="$(deployment_field "$deploy_file" id)"

  python3 -c "
import json, sys
ritual = sys.argv[1] if sys.argv[1] not in ('null', '') else None
ritual_hash = sys.argv[2] if sys.argv[2] not in ('null', '') else None
enabled = sys.argv[3] == 'true'
print(json.dumps({
    'id': sys.argv[4],
    'agent': sys.argv[5],
    'platform': sys.argv[6],
    'squad': sys.argv[7],
    'repos': json.loads(sys.argv[8]),
    'ritual': ritual,
    'ritual_hash': ritual_hash,
    'schedule': json.loads(sys.argv[9]),
    'enabled': enabled,
    'cookbook': sys.argv[10],
    'ritual_path': sys.argv[11] or None,
}))
" "${ritual}" "${ritual_hash}" "${enabled_bool}" "${deploy_id}" "${agent}" \
    "${resolved_platform}" "${squad}" "${repos_json}" "${schedule_json}" \
    "${cookbook}" "${ritual_file}"
}

emit_dashboard_import() {
  local instance="$1"
  local plan_json="$2"
  local out_dir="${instance}/.deploy-artifacts"
  mkdir -p "$out_dir"
  local deploy_id
  deploy_id="$(echo "$plan_json" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")"
  local out_file="${out_dir}/${deploy_id}.json"
  echo "$plan_json" | python3 -c "
import json, sys, datetime
plan = json.load(sys.stdin)
plan['generated_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')
plan['import_note'] = 'Manual dashboard import until platform schedule API is wired'
json.dump(plan, sys.stdout, indent=2)
" > "$out_file"
  echo "wrote ${out_file}"
}

apply_via_api() {
  local plan_json="$1"
  local platform
  platform="$(echo "$plan_json" | python3 -c "import json,sys; print(json.load(sys.stdin)['platform'])")"

  case "$platform" in
    cursor)
      if [[ -z "${CURSOR_API_TOKEN:-}" ]]; then
        return 1
      fi
      # Placeholder: Cursor Automations API not yet wired in this repo.
      return 1
      ;;
    claude-cma)
      if [[ -z "${ANTHROPIC_ADMIN_KEY:-}" ]]; then
        return 1
      fi
      # Placeholder: Claude CMA schedule API not yet wired in this repo.
      return 1
      ;;
    *)
      return 1
      ;;
  esac
}

toggle_enabled() {
  local instance="$1"
  local deploy_id="$2"
  local action="$3"
  local found=false
  local file
  for file in "${instance}/config/deployments/"*.json; do
    [[ -f "$file" ]] || continue
    local id
    id="$(deployment_field "$file" id)"
    if [[ "$id" == "$deploy_id" ]]; then
      found=true
      python3 -c "
import json, sys
path, action = sys.argv[1], sys.argv[2]
with open(path) as f:
    data = json.load(f)
data['enabled'] = action == 'resume'
with open(path, 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')
print(f\"{'enabled' if data['enabled'] else 'disabled'}: {data['id']}\")
" "$file" "$action"
      break
    fi
  done
  if [[ "$found" == false ]]; then
    echo "error: deployment id not found: ${deploy_id}" >&2
    exit 1
  fi
}

# --- parse args ---
ARGS=("$@")
i=0
while [[ $i -lt ${#ARGS[@]} ]]; do
  arg="${ARGS[$i]}"
  case "$arg" in
    --help|-h) usage 0 ;;
    --instance)
      i=$((i + 1))
      INSTANCE_PATH="${ARGS[$i]:-}"
      ;;
    --ritual)
      i=$((i + 1))
      RITUAL_FILTER="${ARGS[$i]:-}"
      ;;
    --id)
      i=$((i + 1))
      DEPLOYMENT_ID="${ARGS[$i]:-}"
      ;;
    --dry-run) MODE="dry-run" ;;
    --dry-run-first) DRY_RUN_FIRST=true ;;
    --run-now) RUN_NOW=true ;;
    apply) MODE="apply" ;;
    pause|resume) MODE="$arg" ;;
    *)
      echo "error: unknown argument: $arg" >&2
      usage 1
      ;;
  esac
  i=$((i + 1))
done

if [[ -z "$INSTANCE_PATH" ]]; then
  # Default sibling checkout
  if [[ -d "${CATALOGUE_ROOT}/../carinyaparc" ]]; then
    INSTANCE_PATH="${CATALOGUE_ROOT}/../carinyaparc"
  else
    echo "error: --instance <path> is required" >&2
    exit 1
  fi
fi

INSTANCE_ROOT="$(resolve_instance "$INSTANCE_PATH")"
validate_instance "$INSTANCE_ROOT"

if [[ "$MODE" == "pause" || "$MODE" == "resume" ]]; then
  if [[ -z "$DEPLOYMENT_ID" ]]; then
    echo "error: --id <deployment-id> required for pause/resume" >&2
    exit 1
  fi
  toggle_enabled "$INSTANCE_ROOT" "$DEPLOYMENT_ID" "$MODE"
  exit 0
fi

echo "Digital Agency — deploy squad agents"
echo "  instance:  ${INSTANCE_ROOT}"
echo "  catalogue: ${CATALOGUE_ROOT}"
echo "  mode:      ${MODE}"
[[ -n "$RITUAL_FILTER" ]] && echo "  ritual:    ${RITUAL_FILTER}"
echo ""

plans=()
for deploy_file in $(list_deployments "$INSTANCE_ROOT" "$RITUAL_FILTER"); do
  if [[ -n "$RITUAL_FILTER" ]]; then
    ritual_val="$(deployment_field "$deploy_file" ritual)"
    [[ "$ritual_val" == "$RITUAL_FILTER" ]] || continue
  fi
  if [[ -n "$DEPLOYMENT_ID" ]]; then
    id_val="$(deployment_field "$deploy_file" id)"
    [[ "$id_val" == "$DEPLOYMENT_ID" ]] || continue
  fi
  plan="$(plan_deployment "$INSTANCE_ROOT" "$deploy_file")"
  plans+=("$plan")
done

if [[ ${#plans[@]} -eq 0 ]]; then
  echo "No deployments matched filters."
  exit 0
fi

for plan in "${plans[@]}"; do
  echo "$plan" | python3 -m json.tool
  echo ""
done

if [[ "$MODE" == "dry-run" ]]; then
  echo "dry-run complete — ${#plans[@]} deployment(s) planned, no changes applied."
  exit 0
fi

if [[ "$DRY_RUN_FIRST" == true ]]; then
  echo "(dry-run-first) plans printed above; proceeding to apply..."
fi

for plan in "${plans[@]}"; do
  enabled="$(echo "$plan" | python3 -c "import json,sys; print('true' if json.load(sys.stdin).get('enabled') else 'false')")"
  if [[ "$enabled" != "true" ]]; then
    deploy_id="$(echo "$plan" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")"
    echo "skip disabled: ${deploy_id}"
    continue
  fi
  if apply_via_api "$plan"; then
    deploy_id="$(echo "$plan" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")"
    echo "applied via API: ${deploy_id}"
  else
    emit_dashboard_import "$INSTANCE_ROOT" "$plan"
  fi
done

if [[ "$RUN_NOW" == true ]]; then
  echo ""
  echo "run-now: trigger manual execution in Cursor Cloud Agents or Claude CMA dashboard"
  echo "  expected output: planning PR + labelled issues (never direct push to main)"
fi

echo "apply complete."
