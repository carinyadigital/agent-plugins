# Cross-document review

Everything that can only be judged by holding the whole set at once: boundaries,
duplication, consistency, and cohesion. A document that reads perfectly alone can
still be wrong here, because the fault is in the relationship between documents,
not inside any one of them.

This work cannot be parallelised per document. Splitting it destroys the very
comparison it performs.

---

## 1. Boundaries

Every document should have one job, statable in a sentence. When you cannot state
it, or when two documents share one, the set has a boundary problem.

### Tests

- **One-sentence job.** Write each document's job as "the place where a reader
  learns X". If you need "and" to cover it, the document may be doing two jobs.
- **Single home per question.** For each question a reader might arrive with,
  exactly one document should be the right answer. Two candidates is a boundary
  failure; zero is a gap.
- **Distinct audience or purpose.** Two documents may cover the same subject at
  different altitudes (an overview and a reference) — that is legitimate, and the
  boundary is the altitude. Name it. Two documents at the *same* altitude on the
  same subject is not.
- **Stated boundaries.** Strong doc sets say what each document does *not* cover
  and where that material lives instead. Absence of this is a warning, not a
  fault.

### Failure modes

| Symptom | What it means |
| ------- | ------------- |
| Two documents both plausibly answer the same question | Contested ownership; readers land in the wrong one |
| A document's title promises more than its content covers | Boundary drift; readers leave without the answer |
| A document accumulates content because no better home exists | Missing document, showing up as a bloated one |
| Content in a document its audience will never open | Wrong home; the audience determines placement |

---

## 2. Duplication

The central discipline: **not all repetition is duplication.** Naive detection
flags every summary and produces noise that trains readers to ignore the review.
Classify before flagging.

### Taxonomy

| Kind | Description | Action |
| ---- | ----------- | ------ |
| **Divergent** | Same question, two documents, **different answers** | `blocking` — always |
| **Verbatim** | Same content, materially identical, in two or more places | `warning` — one source of truth, others link |
| **Contested scope** | Two documents each behave as the authority on a topic | `warning` — resolve the boundary first |
| **Legitimate restatement** | A summary or orientation that repeats a fact *and points at the source of truth* | **Do not flag** |
| **Necessary repetition** | A prerequisite or warning repeated because a reader may arrive mid-set | **Do not flag** |

### Why divergent duplication is always blocking

Verbatim duplication costs maintenance: someone updates one copy and forgets the
other. Divergent duplication has already *had* that failure. The reader now has
two answers and no way to tell which is current, and the confident-looking wrong
one is as likely to be chosen as the right one. Actively misleading beats merely
untidy, every time.

When you find divergence, do not simply report "these disagree". Establish which
is correct where you can, and say how you know — recency, corroboration
elsewhere, or consistency with the thing being documented. Where you cannot
establish it, say that explicitly: the reader needs to know the answer is
genuinely unknown, not that you did not look.

### The restatement test

Before flagging repetition, ask: **does this repetition serve a reader who
arrived here, and does it point onward?**

A getting-started page that states the default port and links to the
configuration reference is doing its job. The same page silently restating the
full configuration table is duplication. The difference is whether the passage
claims to be the source of truth or defers to one.

---

## 3. Consistency

Same set, same answers, same language.

- **Terminology.** One concept, one name. Flag synonyms used interchangeably
  ("tenant" and "workspace" for the same thing), and the sharper failure: one
  name used for two different concepts in different documents.
- **Facts.** Version numbers, commands, paths, endpoints, ports, environment
  variables, file names. These drift silently and are the most common source of
  divergent duplication.
- **Structure.** Sibling documents at the same level should follow the same
  shape. When four of five runbooks open with Prerequisites and the fifth does
  not, the fifth is the finding.
- **Cross-references.** Links resolve, and they point at what the surrounding
  text claims they point at. A link whose target has been restructured is worse
  than a broken one, because it fails silently.
- **Voice and formatting.** Consistent person, tense, and mood; consistent
  heading case, code-block language tags, admonition style. Individually trivial;
  collectively they are what makes a set feel authored rather than assembled.

---

## 4. Cohesion

Does the set read as one work, or as N documents that happen to share a folder?

- **Entry point.** A new reader knows where to start, without being told.
- **Reading order.** Where sequence matters, it is expressed — and documents that
  depend on earlier ones say so.
- **Altitude.** Documents at the same level of the hierarchy sit at the same
  level of detail. A tree where one child is a 40-page reference and its sibling
  is three paragraphs signals a structural problem, not merely uneven effort.
- **Navigation.** Every document is reachable. Orphans (nothing links to them)
  and dead ends (they link nowhere onward) both break the set.
- **Coverage.** The set delivers what its entry point promises. Gaps matter most
  where the structure implies something exists — a nav entry with no page, a
  "see X for details" where X never got written.

---

## 5. Judging without a declared map

Most doc sets never declare their intended structure. Infer it, and say you
inferred it:

1. Look for a declared map first: an index, table of contents, nav config
   (`mkdocs.yml`, `docusaurus.config.js`, `SUMMARY.md`, sidebar files), or a
   README that lists the set.
2. Absent one, infer from directory structure, naming conventions, and the
   documents' own stated purposes.
3. Absent that, infer from content alone, and lower your confidence accordingly.

Where the structure is inferred rather than declared, boundary findings are
weaker — you are comparing against your reconstruction of the author's intent,
not their stated intent. Say so. A missing declared map is itself worth raising
as a `suggestion`: it is the cheapest fix for most boundary problems, because it
forces the set's owners to state each document's job.
