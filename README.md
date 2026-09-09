# Indo-Burma Ranges — Seismology Bibliography & Method-Gap Portal

A chronological bibliography of the **Indo-Burma Ranges, Northeast India and the adjoining
Myanmar–Bengal margin (1934–2026)**, a ranked analysis of methods proven elsewhere but never
applied here, and detailed work plans for the three most startable of them.

Built and maintained by Tapaswi. Live site: **<https://tapaswidata-a11y.github.io/ibr-research-plans/>**

---

## Pages

| Page | What it is | Live | Source |
|---|---|---|---|
| **Portal** | Entry point to everything below | [index](https://tapaswidata-a11y.github.io/ibr-research-plans/) | [`index.html`](index.html) |
| **Bibliography Explorer** | 895 entries, 1934–2026, strictly chronological. Click any bar in the year chart to filter; search and tag filters for Q1–Q3, b-value, TEC, AI/ML, held-locally and scope. Closes with 17 ranked method gaps. | [ibr.html](https://tapaswidata-a11y.github.io/ibr-research-plans/ibr.html) | [`ibr.html`](ibr.html) — **generated**, see below |
| **Do the b-Value Anomalies Survive?** | Rank 01 work plan: re-testing 28 regional b-value claims with b-positive and the b-significant test | [bvalue_plan.html](https://tapaswidata-a11y.github.io/ibr-research-plans/bvalue_plan.html) | [`bvalue_plan.html`](bvalue_plan.html) |
| **Does TEC See It Coming?** | Rank 09 work plan: GNSS-TEC anomaly detection with the alarm scoring the literature omits, plus the ML layer | [tec_plan.html](https://tapaswidata-a11y.github.io/ibr-research-plans/tec_plan.html) | [`tec_plan.html`](tec_plan.html) |
| **Dark Fibre Seismology** | Gap 14 field guide: DAS from φ-OTDR fundamentals to open trial datasets to getting fibre in Northeast India | [das_primer.html](https://tapaswidata-a11y.github.io/ibr-research-plans/das_primer.html) | [`das_primer.html`](das_primer.html) |

## Datasets

| File | Contents | Download |
|---|---|---|
| `IBR_bibliography.csv` | All 895 entries — year, authors, title, venue, quartile, DOI, tags, scope, held-locally flag | [CSV](https://tapaswidata-a11y.github.io/ibr-research-plans/IBR_bibliography.csv) |
| `IBR_bibliography.md` | The same list as a Markdown table with resolvable DOI links | [Markdown](https://tapaswidata-a11y.github.io/ibr-research-plans/IBR_bibliography.md) |
| `IBR_method_gaps.md` | The 17 method gaps, ranked 1–17, with the reasoning and key references for each | [Markdown](https://tapaswidata-a11y.github.io/ibr-research-plans/IBR_method_gaps.md) |
| `_scripts/data/dropped_offtopic.txt` | The 58 wider-scope entries removed as off-topic, listed in full | [txt](https://tapaswidata-a11y.github.io/ibr-research-plans/_scripts/data/dropped_offtopic.txt) |
| `SESSION.md` | Project state: current counts, pipeline notes, decisions taken, open threads | [SESSION.md](https://tapaswidata-a11y.github.io/ibr-research-plans/SESSION.md) |

---

## Rebuilding

`ibr.html`, the CSV and the two Markdown files are **generated** — edit the scripts, not the output.
Everything below is offline; the intermediate JSON in `_scripts/data/` means no network is needed.

```bash
cd _scripts
python3 gen.py       # regenerate ../ibr.html
python3 export.py    # regenerate ../IBR_bibliography.{csv,md} and ../IBR_method_gaps.md
```

- Change the **17 gaps or their ranking** → `gaps.py` (the `RANK` dict at the bottom; two asserts
  catch a duplicate rank or a misspelled key), then rerun `gen.py` and `export.py`.
- Correct a **journal quartile** → the quartile sets at the top of `merge2.py`, then
  `merge2.py` → `merge3.py` → `gen.py` → `export.py`.
- Remove more **off-topic entries** → extend `OFF` (or add a DOI to `RESCUE`) in `merge3.py`,
  then `merge3.py` → `gen.py` → `export.py`.

A **full rebuild** hits CrossRef and OpenAlex and takes ~20 minutes; it is only needed when the
underlying paperbrain corpus changes:

```
enrich.py → build.py → patch.py → merge.py → rescue.py → sweep.py → merge2.py → merge3.py → gen.py → export.py
```

The three work-plan pages (`bvalue_plan.html`, `tec_plan.html`, `das_primer.html`) are
hand-written HTML — edit them directly.

### Publishing a page as a Claude Artifact

The pages in this repo are complete HTML documents, because GitHub Pages serves them as-is. The
Claude Artifact publisher wraps page content in its own `<!doctype html><head></head><body>`
skeleton, so publishing a file from here unmodified would nest one document inside another:

```bash
python3 _scripts/artifact_strip.py das_primer.html    # -> /tmp/das_primer.artifact.html
```

Publish the printed path against the artifact's existing URL so the link is preserved.

---

## How the corpus was assembled, and what to distrust

- **Two scopes, one sequence.** 634 entries are *about* the region — its name is in the title.
  261 more, marked *mentions IBR*, are wider-scope studies found by searching OpenAlex over
  abstracts and keeping only records whose abstract names the region while the title does not.
  Both are in one chronological list; filter them apart on the page.
- **58 entries were removed as off-topic.** Abstract matching also caught Bengal arsenic
  hydrochemistry, monsoon and cyclone meteorology, a mollusc description and several humanities
  papers. The filter in `merge3.py` requires a wider-scope record to read as earth science and not
  belong to an off-topic subject; it never touches title-gated entries or papers held locally.
  The full discard list is in `_scripts/data/dropped_offtopic.txt` — **check it before treating this
  bibliography as exhaustive.**
- **Journal quartiles are not authoritative.** Scimago's bulk table sits behind a bot challenge, so
  Q1/Q2/Q3 were assigned from journal-level knowledge rather than pulled from the live ranking.
  Unknown journals are marked `unrated` rather than guessed. **Re-check any quartile before quoting
  it in a submission.**
- **Absence of a DOI-indexed paper is not proof nobody did the work.** CrossRef covers Indian
  journal literature before ~1990 poorly, and covers theses and grey literature worse. Every
  "no regional study" in the gap analysis means *a targeted search returned nothing* — check for
  theses and reports before writing a proposal on any gap.
- **Ranking is judgement, not measurement.** The 17 gaps are ordered by what could begin with the
  archive and one GPU already in hand, how novel the regional result would be, and how much the
  answer would matter. It assumes no field budget and no ship time; ranks 14–17 are held back by
  money, permits and partnerships rather than by science.

## Repository layout

```
index.html              portal
ibr.html                bibliography explorer  (generated by _scripts/gen.py)
bvalue_plan.html        rank 01 work plan
tec_plan.html           rank 09 work plan
das_primer.html         gap 14 DAS field guide
IBR_bibliography.csv    generated
IBR_bibliography.md     generated
IBR_method_gaps.md      generated
SESSION.md              project state and open threads
_scripts/               pipeline, plus every intermediate JSON in _scripts/data/
.nojekyll               disables Jekyll so _scripts/ is served rather than skipped
```

`.nojekyll` matters: GitHub Pages runs Jekyll by default, and Jekyll silently omits
underscore-prefixed directories from the built site — without it, everything under `_scripts/`
returns 404 on the live site while still appearing in the repository.
