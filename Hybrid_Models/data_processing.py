Python 3.14.4 (tags/v3.14.4:23116f9, Apr  7 2026, 14:10:54) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> def load_data():
...     read male and female files
...     assign sex labels
...     merge datasets
...     compute cohort = year - age
...     sort dataset
...     return data
... 
... 
... def prepare_rh_data(df):
...     convert categorical variables → indices
...     create stan_data dictionary
