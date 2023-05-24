#%%
from data_preparing.fetch_seffaflik_datas import *
from data_preparing.fetch_currency_rates import * 
from data_preparing.fetch_population_data import population_data
#%%
start_date = "2020-01-01"
end_date = "2023-01-03"
#%%
seffaflik_data = fetch_seffaflik_datas(start_date, end_date)
#%%
population_data = fetch_population_data(start_date, end_date)
# %%
