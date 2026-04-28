Python 3.14.4 (tags/v3.14.4:23116f9, Apr  7 2026, 14:10:54) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> def load_input_data():
...     read male file if exists
...     read female file if exists
...     standardize columns
...     merge datasets
...     create cohort = year - age
...     return dataframe, sex_labels
... 
... 
... def prepare_rh_data(df):
...     convert age, year, cohort, sex → indices
...     create stan_data dictionary
...     return stan_data, levels
... 
... 
... def prepare_lc_data(df):
...     convert age, year → indices
...     return stan_data, levels
... 
... 
... def prepare_apc_data(df):
...     convert age, year, cohort → indices
...     return stan_data, levels
... 
... 
... def prepare_cbd_data(df):
...     center age
