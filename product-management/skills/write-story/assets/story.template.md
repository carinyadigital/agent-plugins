---
type: story
id: "{TRACKER-KEY or EPIC-ID-Sn}"
parent: "{epic id}"
priority: P1
status: To do
mvp: false
---

### S{n}: {Short title}

**Statement:** As a {role}, I want {capability}, so that {benefit}.

**Independent test criterion:** {One sentence a reviewer can demonstrate.}

**Priority:** P{0-3}

**Design:** {./design.md#section or none}

#### Acceptance criteria

```gherkin
Scenario: {Happy path name}
  Given {precondition}
  When {single trigger}
  Then {observable outcome}
```

<!-- Optional EARS block when --ears or rule-shaped requirements -->
<!--
#### EARS

- THE SYSTEM SHALL {behaviour}
-->
