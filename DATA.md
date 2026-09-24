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
  ttsclean20180127.csv                   191,418,461   missing
  ModelData.csv                                    ?   missing
  ModelAll.csv                                     ?   missing
  model_data_2.csv                        23,258,820   present, but saved without
                                                       the .csv extension: rename it
```

`model/predictions.ipynb` also reads `model/mod_pred_data.csv`, a grid of
future dates × size groups × states "built separately". It was never saved
and isn't in the surviving data. The notebook now rebuilds it when it's
missing: 84 quarter-end dates × 3 size groups × 2 states, all recovered from
the notebook's saved outputs except which two states were used. If you
remember them, change `PRED_STATES` in that cell.

## Lineage

```
TTSX_..._p1.xlsx + p2.xlsx
  └─ wrangle/first_look_TTS ──► TTS.csv
       └─ (step not in any saved notebook) ──► live_20180118
            └─ wrangle/tts_6 ──► live20180119.csv, ttsclean20180119.csv
                 └─ wrangle/tts_9 ──► ttsclean20180123.csv
                      └─ (step not saved) ──► ttsclean20180127.csv
                           └─ model/model_01 ──► ModelData.csv
                                └─ model/make_modeling_data ──► model_data_2.csv
                                     └─ model_08, model_median_*, mod_med_3f_*, predictions

(no saved notebook writes ModelAll.csv; it's read by model_02–04, 05a, 06)
```

`model_data_2.csv` has 364,212 rows (installations from 1998-01-09 to
2016-12-31) with these columns: `row_id` (index), `num_days`, `num_weeks`,
`num_months`, `size_kw`, `scaleSize`, `state`, `cost_per_watt`, `install_date`.

## What runs

| Notebooks | Input | Status |
|---|---|---|
| `model/model_08_random_forest`, `model_median_01`, `model_median_02`, `mod_med_3f_*` | `model_data_2.csv` | runs end to end (smoke-tested with synthetic data) |
| `model/model_median_no_poly_exclusion` | `model_data_2.csv` | runs, except cells 43–53: they use a grid search (cell 30) that was switched to a raw cell to skip its ~30 min run. Change it back to code to run them. |
| `model/predictions` | `model_data_2.csv`, `mod_pred_data.csv` | runs end to end. It rebuilds the prediction grid if `mod_pred_data.csv` is missing, but the grid's two states are a guess (CA, AZ). |
| `wrangle/first_look_TTS`, `tts_2nd_look` | raw xlsx / `TTS.csv` | inputs exist; not test-run (slow: reads 280 MB of Excel) |
| `wrangle/tts_5`, `tts_6` | `live_20180118` | inputs exist; not test-run |
| `wrangle/tts_7`, `tts_9`, `story/tts_story_boolean` | `ttsclean20180119/23` | after rerunning `tts_6` / `tts_9` |
| `model/model_01`, `story/tts_story_01`, `story/stat_sig` | `ttsclean20180127.csv` | missing input |
| `model/model_02`–`06`, `make_modeling_data` | `ModelAll.csv` / `ModelData.csv` | missing input |
| `archive/**` | older OpenPV dataset | not maintained; the data is gone |

The older OpenPV intermediates `20180105` and `thing0108` survive in
`local/data/toss/`, but nothing outside `archive/` uses them.
