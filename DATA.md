# Data

The data isn't in this repo. The notebooks read it from `local/data/`, a
gitignored directory at the repo root (paths in the notebooks look like
`../local/data/...` because they run from inside `wrangle/`, `story/` or `model/`).

## Source

Lawrence Berkeley National Laboratory, *Tracking the Sun* (TTS), the public
data file published through NREL's OpenPV project, downloaded 9 Nov 2017:

- `TTSX_LBNL_OpenPV_public_file_p1.xlsx`
- `TTSX_LBNL_OpenPV_public_file_p2.xlsx`
- `PublicDataFile_UserGuide.pdf` (the data dictionary)

From the original notes (`local/data/LBNL_openpv_tts_data/README.txt`):

> The xlsx files are the public, "cleaned" version of the data: about 60
> fields, lots of empty cells, with many fields canonicalized. It looks like a
> reduced version of the rawer OpenPV CSV (80+ fields), with many of the more
> cryptic fields removed. Plan: read the xlsx with `pd.read_excel` and export a
> CSV, since Excel doesn't handle 200 MB files well.

Current TTS releases use a different schema and cover more years, so a fresh
download won't be a drop-in replacement for these files.

## Expected layout and file sizes

Sizes are from an `ls -l` saved in a 2018 notebook output. They were checked
against the author's surviving copy in 2026.

```
local/data/LBNL_openpv_tts_data/
  TTSX_LBNL_OpenPV_public_file_p1.xlsx   185,901,845   raw source (present)
  TTSX_LBNL_OpenPV_public_file_p2.xlsx    95,456,887   raw source (present)
  PublicDataFile_UserGuide.pdf               859,629   (present)
  TTS.csv                                501,984,387   missing, regenerable
  live_20180118                          232,427,884   (present)
  live20180119.csv                       226,627,007   missing, regenerable
  ttsclean20180119.csv                   190,295,601   missing, regenerable
  ttsclean20180123.csv                   187,478,829   missing, regenerable
  ttsclean20180127.csv                   191,418,461   missing, regenerable
  ModelData.csv                                    ?   missing, regenerable
  ModelAll.csv                                     ?   missing, regenerable
  model_data_2.csv                        23,258,820   present, but saved without the
                                                       .csv extension and without the
                                                       state column (see below)
```

The surviving `model_data_2` is a later save that dropped the `state` column.
Rename it to `model_data_2.csv`, put `live_20180118` next to it, and run
`python wrangle/restore_state_column.py` from the repo root. The script looks
up each row's state in `live_20180118` by `row_id` and only rewrites the file
if every row matches on date and size. With the state restored, the notebooks
reproduce their saved 2018 results (see "What runs" below).

The prediction grid, `model/mod_pred_data.csv` (84 quarter-end dates × 3 size
groups × CA and TX), and its input `model/prediction_times.csv` are small
enough to live in the repo. `model/make_prediction_dates` and
`make_prediction_data` rebuild both exactly.

## Lineage

```
TTSX_..._p1.xlsx + p2.xlsx
  └─ wrangle/first_look_TTS ──► TTS.csv
       └─ (step not in any saved notebook) ──► live_20180118
            └─ wrangle/tts_6 ──► live20180119.csv, ttsclean20180119.csv
                 └─ wrangle/tts_9 ──► ttsclean20180123.csv
                      └─ story/tts_cost_dependence_orig ──► ttsclean20180127.csv
                           └─ model/model_01 ──► ModelData.csv
                                ├─ model/model_02_raw ──► ModelAll.csv
                                │    └─ model_02–04, model_05a_ridge_17, model_06_lasso_b
                                └─ model/make_modeling_data ──► model_data_2.csv
                                     └─ model_08, model_median_*, mod_med_3f_*,
                                        predictions, report_support

model/make_prediction_dates ──► prediction_times.csv
  └─ model/make_prediction_data ──► mod_pred_data.csv ──► predictions, report_support
```

`story/tts_cost_dependence_hack` is a variant of `_orig` that writes the same
file; which of the two produced the surviving results isn't recorded.

`model_data_2.csv` has 364,212 rows (installations from 1998-01-09 to
2016-12-31) with these columns: `row_id` (index), `num_days`, `num_weeks`,
`num_months`, `size_kw`, `scaleSize`, `state`, `cost_per_watt`, `install_date`.

## What runs

| Notebooks | Input | Status |
|---|---|---|
| `model/model_08_random_forest`, `model_median_01`, `model_median_02`, `mod_med_3f_*` | `model_data_2.csv` (with state restored) | verified on the real data in 2026: reproduces the 2018 results (see below) |
| `model/model_median_no_poly_exclusion` | `model_data_2.csv` | runs, except cells 43–53: they use a grid search (cell 30) that was switched to a raw cell to skip its ~30 min run. Change it back to code to run them. |
| `model/predictions` | `model_data_2.csv`, `mod_pred_data.csv` | verified on the real data in 2026 |
| `model/make_prediction_dates`, `make_prediction_data` | none / `prediction_times.csv` | verified in 2026: rebuild both CSVs exactly |
| `wrangle/first_look_TTS`, `tts_2nd_look` | raw xlsx / `TTS.csv` | inputs exist; not test-run (slow: reads 280 MB of Excel) |
| `wrangle/tts_5` | `live_20180118` | inputs exist; not test-run |
| `wrangle/tts_6` | `live_20180118` | verified on the real data in 2026: reproduces the 2018 results after a fix (see below) |
| `wrangle/tts_7` | `ttsclean20180119.csv` | inputs exist; not test-run |
| `wrangle/tts_9` | `ttsclean20180119.csv` | verified on the real data in 2026: reproduces the 2018 results exactly |
| `story/tts_story_boolean` | `ttsclean20180123.csv` | verified on the real data in 2026: reproduces the 2018 results after a fix (see below) |
| `story/tts_cost_dependence_orig` | `ttsclean20180123.csv` | verified on the real data in 2026: reproduces the 2018 results after a fix (see below); writes `ttsclean20180127.csv` |
| `model/model_01`, `story/tts_story_01`, `story/stat_sig`, `story/cap_support` | `ttsclean20180127.csv` | verified on the real data in 2026: `model_01`, `tts_story_01` and `cap_support` needed fixes (see below); `stat_sig` reproduces the 2018 results exactly |
| `model/model_02_raw`, `make_modeling_data` | `ModelData.csv` | verified on the real data in 2026: both run clean with no fixes; `make_modeling_data`'s `model_data_2.csv` output matches a pre-regeneration backup of the surviving file to ~1e-14 (see below) |
| `model/model_02`–`06` | `ModelAll.csv` | verified on the real data in 2026: all run clean; `model_02`–`04` and `model_06_lasso_b`'s grid searches show the same ill-conditioned-polynomial drift as the median models (see below); `model_05a_ridge_17` matches 2018 almost exactly; `model_06_lasso_b` has two pre-existing bugs unrelated to library upgrades (see below) |
| `archive/**` | older OpenPV dataset | not maintained; the data is gone |

The older OpenPV intermediates `20180105` and `thing0108` survive in
`local/data/toss/`, but nothing outside `archive/` uses them.

## 2026 verification

The eight notebooks above were rerun on the real data with the versions in
`requirements.txt` (Python 3.14) and compared with their saved 2018 outputs:

- Median models (`mod_med_3f_*`, the weekly and daily fits in `model_median_01`
  and `model_median_02`, the median models in `predictions`): identical to
  about 12 decimal places.
- Random forest and the raw-row models in `predictions`: within ±0.002 R².
  These involve randomness (random forests, unseeded shuffles).
- Monthly-median polynomial fits, where the grid search reaches degree 13–20 on
  about 228 points: `model_median_01` now picks degree 17 (R² 0.655) instead
  of 13 (0.748); `model_median_02` picks degree 7 (0.865) instead of 8 (0.863).
  The split is fixed, so this is newer numpy/scipy solving an ill-conditioned
  fit differently. The lab notes already flagged the monthly model as unstable.

The prediction-grid notebooks were rerun too and rebuild `prediction_times.csv`
and `mod_pred_data.csv` identically. That run caught a silent pandas change:
subtracting two `Period`s now returns an offset (`<12 * Weeks>`) rather than a
number, so week and month counts are now taken with `.n` (in
`make_prediction_dates`, `make_modeling_data` and `story/stat_sig`).

### Full-chain regeneration from `live_20180118` (2026)

The rest of the chain — everything between the surviving `live_20180118` and
`model_data_2.csv`, plus the wrangle/story/model notebooks that read from it —
was regenerated and verified in 2026. Before rerunning `make_modeling_data`
(which overwrites `model_data_2.csv`), the surviving file was copied to
`model_data_2_restored_backup.csv`. The regenerated `model_data_2.csv` was
compared against that backup: same shape (364,212 x 8), same columns, same
index, and every numeric column matched to within 7e-15 (`size_kw`,
`cost_per_watt`) or exactly (`num_days`, `num_weeks`, `num_months`,
`scaleSize`); `state` and `install_date` matched with zero mismatches. This is
well inside the 1e-9 tolerance and confirms the chain reproduces 2018.

Library-change fixes (source changed, saved 2018 outputs left as-is; each
verified to reproduce the 2018 results after the fix):

- `wrangle/tts_6`: `pd.read_csv(..., error_bad_lines=False, warn_bad_lines=True)`
  → `on_bad_lines='warn'` (pandas removed the old kwargs).
- `story/tts_cost_dependence_orig`: `dfRes.corr()` → `dfRes.corr(numeric_only=True)`
  (pandas `.corr()` no longer silently drops non-numeric columns).
- `model/model_01`: `sns.regplot('num_days', 'cost_per_watt', dfMod, ...)` →
  keyword arguments `x=`, `y=`, `data=` (seaborn made these keyword-only).
- `story/tts_story_01`, `story/cap_support` (both have the same 3D surface-plot
  cell): `theData.fillna(method='bfill')` → `theData.bfill()` (pandas removed
  `fillna`'s `method` kwarg); `fig.gca(projection='3d')` →
  `fig.add_subplot(projection='3d')` (matplotlib removed `projection` from
  `Figure.gca`).

One non-library fix: `story/tts_story_boolean` cell 15 assigned its groupby
result to `byYeMoN`, but the next cell reads `byYeMoTP` (the commented-out line
above it, and every other cell's naming convention in that notebook, confirm
`byYeMoTP` was the intended name) — a leftover copy/paste bug, not a version
issue. Renamed the assignment to `byYeMoTP`.

`model/model_06_lasso_b` has two pre-existing bugs, also unrelated to library
versions, left unfixed because they're informational cells with no downstream
dependents: cell 11 references `dfMod100k`, which is never defined anywhere in
the notebook (only `dfMod` is); cell 24 calls `trainVsTest(model.cv_results_)`,
a function that's never defined in this notebook (sibling notebooks define
`trainVsTestResults`, with a different expected results shape, so it isn't a
simple rename). Both cells error and are skipped; the actual grid-search cells
that other cells depend on all ran cleanly.

A transient `ImportError: DLL load failed while importing _tools ... An
Application Control policy has blocked this file` appeared once when
`story/tts_cost_dependence_orig` imported `statsmodels.api`; a plain `python -c
"import statsmodels.api"` worked immediately, and a full rerun of the notebook
succeeded with no code change, so this was flagged as one-off environment
noise (antivirus/AppLocker scanning a DLL on first load), not a bug.

Numeric results, 2018 vs. 2026 (R² unless noted):

| Notebook | 2018 | 2026 | Notes |
|---|---|---|---|
| `wrangle/tts_6`, `tts_9` | row counts / value_counts | identical | exact match at every checked cell |
| `story/tts_cost_dependence_orig` | OLS 0.374, 0.379, 0.397, 0.420, 0.441 | same | exact match |
| `model/model_01` | row-filter chain 745688→...→364212; OLS 0.401, 0.439, 0.459, 0.439, 0.459 | same | exact match; raw (unscaled) `PolynomialFeatures`+`LinearRegression` cells (64–72, 79–80) diverge numerically — same ill-conditioning as the median models, not fixed |
| `story/stat_sig` | corr −0.611365, OLS 0.376 | same | exact match |
| `model/model_02` | degree 18, R² 0.45456 | degree 9, R² 0.45349 | ill-conditioned poly fit, close R² |
| `model/model_03` (small grid) | degree 3, R² 0.4850506445537449 | degree 3, R² 0.4850506445537447 | effectively exact |
| `model/model_03` (big grid) | degree 14, R² 0.51694 | degree 8, R² 0.51463 | ill-conditioned poly fit, close R² |
| `model/model_04` | degree 14, R² 0.53402 | degree 8, R² 0.53184 | ill-conditioned poly fit, close R² |
| `model/model_05a_ridge_17` | alpha 1.0, degree 17, R² 0.53499 | alpha 1.0, degree 17, R² 0.53499 | matches almost exactly |
| `model/model_06_lasso_b` (poly fixed at 17) | alpha 0.0001, R² (2018 `cv_results_` shows degree 7, inconsistent with the source's `poly_space=[17]` — a pre-existing stale-output quirk, not something we fixed) | alpha 0.0001, degree 17, R² 0.52645 | see note |
| `model/model_06_lasso_b` (poly fixed at 10) | alpha 0.0001, R² 0.5191 (degree in saved output shows 7, same quirk) | alpha 0.0001, degree 10, R² 0.52526 | see note |

The polynomial-degree drift in `model_02`–`04` and `model_06_lasso_b` is the
same phenomenon already documented above for the monthly-median fits:
unscaled-magnitude, high-degree `PolynomialFeatures` on ~364k rows is
ill-conditioned, so a newer numpy/scipy picks a different "best" degree via
grid search while R² stays close. `model_05a_ridge_17` and the small grid in
`model_03` don't drift because Ridge regularization and/or a narrow degree
range keep the fit well-conditioned.
