# Document quality

Everything judgeable about a single document, read on its own. Applied per
document, and therefore the only part of a docs review that parallelises.

Judge a document against **its own job**, not against a universal ideal. A
reference page that reads like a tutorial is a finding; so is a tutorial that
reads like a reference. Establish the document's purpose and audience first —
everything below is relative to them.

---

## 1. Purpose and audience

- [ ] The purpose is clear within the first paragraph. A reader can tell in one
      screen whether they are in the right place.
- [ ] The intended audience is evident, from the content if not stated outright.
- [ ] The document knows what kind of document it is. The four kinds behave
      differently and mixing them is the most common structural fault:

| Kind | Answers | Reader is |
| ---- | ------- | --------- |
| Tutorial | "Teach me by doing" | Learning, needs a guaranteed-success path |
| How-to / runbook | "How do I achieve X?" | Working, has a goal already |
| Reference | "What are the details of Y?" | Looking something up |
| Explanation | "Why is it like this?" | Trying to understand |

A document serving two of these at once usually serves neither. Flag the mixture,
name which parts belong where.

## 2. Structure

- [ ] Headings describe content, not decoration. A reader scanning only the
      headings gets an accurate outline.
- [ ] Heading depth is sensible and not skipped (no H2 → H4).
- [ ] Sections appear in the order a reader needs them, not the order the author
      thought of them.
- [ ] Length matches the job. A document that has grown past its purpose is
      usually two documents.
- [ ] Scannable: information is retrievable without reading start to finish,
      unless it is a tutorial, where sequence is the point.
- [ ] Front-loaded: the answer comes before the caveats and the history.

## 3. Writing

- [ ] Sentences carry one idea. Paragraphs carry one point.
- [ ] Jargon is defined at first use, or linked. Acronyms expanded once.
- [ ] Active voice and direct address where the reader must act. "Run the
      migration", not "the migration should then be run".
- [ ] Concrete over abstract. Where a concept needs an example, there is one.
- [ ] No filler: throat-clearing openings, restated headings, or sentences that
      say a section will explain rather than explaining.
- [ ] Consistent person and tense within the document.

## 4. Correctness and currency

- [ ] Instructions are followable. Steps are complete and in order, prerequisites
      stated **before** they are needed, and nothing assumes state the reader was
      never told to create.
- [ ] Commands, paths, and code samples are plausible and internally consistent —
      a variable introduced in step 2 is the one used in step 5.
- [ ] Claims about behaviour match what the documented thing actually does, where
      you can check. Where you cannot check, do not assert that it is wrong; note
      it as unverified.
- [ ] No stale markers: "coming soon" long past, TODOs, dated references to
      versions or people, links to deprecated things.
- [ ] Dates, versions, and status fields are current if present.

## 5. Completeness

- [ ] The document delivers what its title and opening promise.
- [ ] Error and failure paths are covered where the reader will hit them, not
      only the happy path.
- [ ] Nothing critical is left implicit because "everyone knows" — the audience
      definition decides what counts as known.
- [ ] Where the document defers to another, it names it and links it.

## 6. Self-containment

- [ ] The document does not require reading a specific other document first
      unless it says so.
- [ ] Links carry enough context that a reader knows why to follow them before
      they do.
- [ ] No orphan references: "as discussed above" where it was not, "see the
      diagram" where there is none.

---

## Not findings

Do not raise these. Each one trains readers to discount the review:

- **Style preferences the set is consistent about.** If every document uses a
  convention you would not have chosen, that is the house style, not a fault.
  Inconsistent application of it is the finding.
- **Length alone.** A long reference document is not a problem. A long document
  that should be three is, and the finding is the boundary, not the length.
- **Missing content outside the document's job.** A tutorial that does not
  document every flag is correct, not incomplete.
- **Repetition that orients the reader** and points at the source of truth. See
  the restatement test in [cross-document.md](cross-document.md).
- **Prose polish on a document whose facts are wrong.** Fix the ordering: report
  the correctness finding and let the wording follow.
