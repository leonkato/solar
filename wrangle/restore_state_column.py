"""Restore the 'state' column to model_data_2.csv.

The surviving copy of model_data_2.csv (April 2018) was saved without the
'state' column that the 3-feature notebooks need. model_data_2's row_id is
live_20180118's row number (that file's first, unnamed column), so the state
can be looked up there. The file is rewritten only if every row matches on
install_date and size_kw; the original is kept as model_data_2_nostate.csv.

Run from the repo root:  python wrangle/restore_state_column.py
"""
import os
import sys

import pandas as pd

d = 'local/data/LBNL_openpv_tts_data/'
mod = pd.read_csv(d + 'model_data_2.csv', index_col='row_id', parse_dates=['install_date'])
if 'state' in mod.columns:
    sys.exit('model_data_2.csv already has a state column; nothing to do')
live = pd.read_csv(d + 'live_20180118', usecols=['Unnamed: 0', 'install_date', 'size_kw', 'state'],
                   index_col='Unnamed: 0', parse_dates=['install_date'])
print(f'model_data_2: {len(mod):,} rows   live_20180118: {len(live):,} rows')

j = mod.join(live, rsuffix='_live', how='left')
missing = j.state.isna().sum()
date_bad = (j.install_date != j.install_date_live).sum()
size_bad = ((j.size_kw - j.size_kw_live).abs() > 1e-6).sum()
print(f'rows not found: {missing}   date mismatches: {date_bad}   size mismatches: {size_bad}')
if missing or date_bad or size_bad:
    sys.exit('checks FAILED; file left unchanged')

out = j[['num_days', 'num_weeks', 'num_months', 'size_kw', 'scaleSize', 'state', 'cost_per_watt', 'install_date']]
os.replace(d + 'model_data_2.csv', d + 'model_data_2_nostate.csv')
out.to_csv(d + 'model_data_2.csv')
print('checks passed; wrote model_data_2.csv with state (original kept as model_data_2_nostate.csv)')
