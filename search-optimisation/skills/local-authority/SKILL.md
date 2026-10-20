---
name: local-authority
description: >
  Local search and authority building — checks the business listing (Google Business
  Profile), name/address/phone consistency across directories and the site, local
  structured data, and finds earned-link and citation prospects with draft outreach.
  Use for "local SEO", "Google Business Profile", "citations", "backlinks", "link
  building", or "who should link to us". Drafts only — never posts, edits listings,
  or sends outreach. Do NOT use for site-wide technical audits (technical-seo-audit)
  or keyword planning (keyword-research).
license: Apache-2.0
allowed-tools: Read Write Glob Grep
argument-hint: "[--focus listing|citations|links]"
metadata:
  author: Carinya Digital
  version: "0.1.0"
  owner: search-optimisation
  review_cadence: quarterly
  work_shape: generate-draft
  output_class: draft-for-review
---

# Local and authority building

You check how the business shows up in local search and find places that should
mention or link to it. Everything you produce is a draft for a person to post,
submit, or send.

Read [search-optimisation-conventions.md](../../references/search-optimisation-conventions.md)
and [search-data-sources.md](../../references/search-data-sources.md).

## When to use

- Monthly local and authority pass (called by the `seo-agency` agent).
- The user asks about their Google Business Profile, directory listings, citations,
  backlinks, or link-building ideas.

## What this skill does not do

- Does not edit a business listing, submit to a directory, or send email.
- Does not buy links, join link schemes, or write reviews or testimonials.
- Does not invent awards, partnerships, or claims to pitch with — pitches use only
  facts from the practice profile and the site.
- Does not change site code — structured-data gaps are filed as tracker items.

## Preconditions

From the practice profile:

| Input | Required | On missing |
| ----- | -------- | ---------- |
| Canonical business name, address, phone, and service area | Yes | Ask; when unattended, stop this skill and record the gap |
| Location wording rules (e.g. brand line vs postal address) | Yes | Ask; never guess |
| Category and audience (what people search to find the business) | Yes | Ask |
| Known partners, memberships, directories already listed | No | Treat as none |

## Trust spine

Every prospect has a source URL you opened this run. Every NAP check lists the exact
value found and where. Outreach drafts are marked **Draft — not sent**. Facts in a
pitch trace to the profile or a page on the site.

## Workflow

1. **Listing.** Search for the business by name and by "{category} near {town}".
   Record whether a business profile shows, and its name, address, phone, hours,
   category, website link, photos, and review count as displayed. Compare with the
   profile. Do not sign in to edit.
2. **NAP consistency.** Check the site's contact page, footer, structured data
   (`LocalBusiness` / `Organization`), and the top directory and social listings
   found by search. List every mismatch against the canonical values.
3. **Local structured data.** Confirm the site has `LocalBusiness` (or a fitting
   subtype) with name, address, geo, url, and sameAs. A gap becomes a tracker item.
4. **Link and citation prospects.** Search for organisations that already link to or
   list businesses like this one: regional tourism bodies, industry associations,
   landcare and community groups, councils, local media, event listings, partner
   suppliers, and relevant directories. Keep prospects that are relevant, real, and
   reachable. Skip pay-to-play link farms and generic directories with no audience.
   If an SEO-intelligence source is available, add referring domains new or lost since
   the last run.
5. **Draft outreach.** For the top five prospects, write a short pitch that offers
   something real (a story, a field day, a resource page, an event) in the brand
   voice. Note the contact route found; do not send.
6. **File items.** File tracker items for site fixes (NAP mismatch on site, missing
   structured data) per the conventions. Listing and outreach work goes in the report,
   not the tracker, unless the profile says otherwise.

## Outputs

Write `docs/work/seo/local-authority-{YYYY-MM-DD}.md`:

```markdown
# Local and authority — {date}

## Listing status
| Field | Canonical | Found | Source | Action |

## NAP consistency
| Where | Name | Address | Phone | Matches? |

## Structured data
Present / missing fields; tracker item links.

## Link and citation prospects
| Prospect | Why relevant | Source URL | Route | Priority |

## Outreach drafts (Draft — not sent)
### {Prospect}
Subject / message.

## Backlink movement
New / lost referring domains (source, window) or "not available — reason".

## Needs a person
Listing edits to make, directories to submit, pitches to send.
```
