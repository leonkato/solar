# Residential solar: cost per watt over time

A 2017–18 Springboard data science capstone. The question: using LBNL's
*Tracking the Sun* dataset (about 1.1 M US solar installations, 1998–2016),
how has the installed cost per watt of residential solar changed, and what can
we expect over the next couple of years?

For a quick overview, see [`docs/Solar_Slides.pdf`](docs/Solar_Slides.pdf).
The full write-up is [`docs/solar_capstone_report_final.pdf`](docs/solar_capstone_report_final.pdf).

## Findings

Residential cost per watt is noisy. Models of individual installations top out
at a modest R², but models of the **median** cost per watt fit well and give
stable 6–8 quarter extrapolations.

| Model | Notebook | Test R² |
|---|---|---|
| OLS, polynomial (degree 14) in time, size, state | `model/model_04` | 0.534 |
| Ridge / Lasso on the same features | `model/model_05a_ridge_17`, `model_06_lasso_b` | ≈ 0.53 (no gain: not overfit, just noisy) |
| Random forest on raw installations | `model/model_08_random_forest` | 0.596 (judged to be fitting noise) |
| OLS poly on **weekly median**, time only (degree 8) | `model/model_median_01` | 0.849 |
| OLS poly on **monthly median**, time + size group (degree 8) | `model/model_median_02` | 0.863 |
| Median models with state added | `model/mod_med_3f_*` | 0.68–0.75 (state doesn't help) |

`model/predictions.ipynb` puts the models side by side and extrapolates
through 2018. [`model/README.md`](model/README.md) has the full lab notes.

## Layout

```
wrangle/   load the raw TTS xlsx, clean it, write the modelling CSVs
story/     exploratory analysis and the "data story" notebooks
model/     modelling experiments, the final prediction comparison, lab notes
docs/      proposal, milestone report, final report, slides
archive/   superseded notebooks (older OpenPV dataset, scratch work, early model iterations)
DATA.md    where the data came from, expected files and sizes, and the lineage
```

Reading order: `wrangle/first_look_TTS` → `tts_2nd_look` → `tts_5` → `tts_6`
→ `tts_7` → `tts_9` → `story/tts_story_01` → `tts_story_boolean` → `stat_sig`
→ `model/model_01` → `make_modeling_data` → `model_02`…`08` → `model_median_01`
→ `model_median_02` → `mod_med_3f_*` → `predictions`.

## Running it

The data isn't in the repo. See [`DATA.md`](DATA.md) for what goes in
`local/data/` and which notebooks can run with the files that survive.

```
python -m venv .venv && . .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

The notebooks were written for Python 3.6 (pandas 0.22, scikit-learn 0.19) and
have been updated for current library versions. Saved outputs are still the
original 2018 results, so a rerun can be compared against them. Only the
`model/` notebooks that read `model_data_2.csv` have been test-run on the new
versions, and that was against synthetic data. The others got the same
mechanical updates but haven't been run.

Notebooks in `archive/` weren't updated and their data paths are one level off.
They're kept for the record.
