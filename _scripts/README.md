# IBR bibliography pipeline

Rebuilds `IBR_bibliography.csv/.md`, `IBR_method_gaps.md` and `ibr.html` (the published page)
from the paperbrain corpus in `~/all_papers/cards/` plus CrossRef.

All scripts resolve their own paths — run them from anywhere. Intermediate JSON lives in
`data/`, so the common cases need **no network at all**.

## Common tasks

```bash
cd ~/all_papers/IBR/_scripts

python3 export.py       # regenerate CSV + Markdown from data/final2.json   (offline, instant)
python3 gen.py          # regenerate ../ibr.html for republishing            (offline, instant)
```

Edit `gaps.py` to change the 17 method gaps, then rerun `gen.py` and `export.py`.
Edit the quartile sets at the top of `merge2.py` to correct a Q-rating, then rerun
`merge2.py` → `gen.py` → `export.py`.

## Full rebuild (hits CrossRef; slow)

Only needed when the underlying corpus in `~/all_papers/cards/` changes.

| # | Script | Does | Network |
|---|---|---|---|
| 1 | `enrich.py` | Filters cards for IBR/TEC; resolves each via CrossRef — card DOI, then DOI scraped from the PDF (`pdftotext -f 1 -l 3`), then bibliographic title match → `data/enriched.json` | yes, ~10 min |
| 2 | `build.py` | Dedupes, assigns quartiles, applies manual metadata repairs → `data/final.json` | no |
| 3 | `patch.py` | Recovers papers the first region filter missed → `data/extra.json` | yes |
| 4 | `merge.py` | Merges those in; tags b-value papers | no |
| 5 | `rescue.py` | DOI-recovery pass over still-excluded cards → `data/rescued.json` | yes |
| 6 | `sweep.py` | 20 CrossRef regional queries (~1,000 hits) → `data/sweep.json` | yes, ~5 min |
| 7 | `merge2.py` | Filters the sweep to geoscience; merges library + sweep + ML → `data/final2.json` | no |
| 8 | `gen.py` | Renders `../ibr.html` | no |
| 9 | `export.py` | Writes the CSV and Markdown deliverables | no |

`ml.json`, `extra2.json` and `cand3.json` in `data/` were built by ad-hoc CrossRef lookups
during the session; `merge2.py` consumes them as-is.

## Publishing

`ibr.html` is published at
**https://claude.ai/code/artifact/9591e5b7-c1ea-45f6-9952-343b34736636**

To update it, pass that URL as `url` to the Artifact tool — read it first, and never publish
without the `url` or you create a second artifact and orphan the link.

## Two things that bit us, kept as regression notes

- **Plain "Burma".** The original region regex required `indo-burma|burmese|myanmar` and
  silently dropped Fitch 1972 and Westerweel 2019. Any new region filter must match bare
  `\bburma`.
- **Unicode hyphens.** CrossRef returns U+2010 in strings like "deep‐learning", which defeats
  ASCII-hyphen keyword matching. `merge2.py` normalises `[‐-―−­]` to `-`
  before tagging. Keep that.

## Caveats baked into the output

- Journal quartiles are assigned from journal-level knowledge, **not** a live Scimago pull —
  scimagojr.com is behind a Cloudflare bot challenge. Unknown journals are `unrated`, never
  guessed. Verify before quoting a quartile in a submission.
- CrossRef misses pre-1990 Indian literature published without DOIs (*MAUSAM*, *Current
  Science*, *JGSI* are thin here). Absence of a DOI-indexed paper is not proof nobody did the
  work.
