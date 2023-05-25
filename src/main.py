#%%  IMPORTS
from src.data_preparing.fetch_seffaflik_datas import *
from src.data_preparing.fetch_currency_rates import *
from src.data_preparing.fetch_population_data import fetch_population_data
# from prophet import Prophet
from neuralprophet import NeuralProphet



#%% DATES
start_date = "2020-01-01"
end_date = "2023-05-01"



#%% FETCH SEFFAFLIK DATA AND SAVE IT TO DISK
seffaflik_data = fetch_seffaflik_datas(start_date, end_date)
seffaflik_data.to_csv("../data/seffaflik_data.csv", encoding='utf-8-sig',index=False)



#%% FETCH POPULATION DATA AND SAVE IT TO DISK
population_data = fetch_population_data(start_date, end_date)
population_data.to_csv("../data/population_data.csv", encoding='utf-8-sig', index=False)



#%% READ SEFFALIK AND POPULATION DATAS DIRECTLY FROM DISK AND MERGE
seffaflik_data = pd.read_csv("../data/seffaflik_data.csv")
population_data = pd.read_csv("../data/population_data.csv")
all_data = pd.merge(seffaflik_data, population_data, on=["Tarih", "Saat"], how="left")
all_data['Saat'] = all_data['Saat'].astype(str).str.zfill(2)  # Convert integers to zero-padded strings
all_data['Timestamp'] = pd.to_datetime(all_data['Tarih'] + ' ' + all_data['Saat'] + ':00:00')
# Drop the 'Tarih' and 'Saat' columns if you no longer need them
all_data = all_data.drop(['Tarih', 'Saat'], axis=1)




#%% FETCH CURRENCY RATES AND EUROPE AVG. ENERGY PRICE. THEN MERGE WITH ALL_DATA



#%% PROPHET
df = all_data




#%% NEURAL PROPHET
df = all_data
df = df.rename(columns={'Timestamp': 'ds'})
df = df.rename(columns={'PTF (TRY/MWh)': 'ds'})
df.drop_duplicates(subset=['ds'], keep='first', inplace=True)
metrics = NeuralProphet().fit(df,  freq = "H")
forecast = NeuralProphet().predict(df)


#%% CAT BOOST


