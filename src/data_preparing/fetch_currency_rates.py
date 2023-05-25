#%%
import pandas as pd
from forex_python.converter import get_rate
from datetime import datetime, timedelta

#%%
def fetch_currency_rates(start_date, end_date):
    start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
    
    usd_try_rate_data = []
    eur_try_rate_data = []
    eur_usd_rate_data = []
    
    x=1
    while start_date_dt <= end_date_dt:
        print(x)
        x+=1
        usd_try_rate_data.append({'Tarih': start_date_dt.date(), 'Saat': start_date_dt.hour, 'USD-TRY': get_rate('USD', 'TRY', start_date_dt)})
        eur_try_rate_data.append({'Tarih': start_date_dt.date(), 'Saat': start_date_dt.hour, 'EUR-TRY': get_rate('EUR', 'TRY', start_date_dt)})
        eur_usd_rate_data.append({'Tarih': start_date_dt.date(), 'Saat': start_date_dt.hour, 'EUR-USD': get_rate('EUR', 'USD', start_date_dt)})
        start_date += timedelta(hours=1)
        
    usd_try_rate_data = pd.DataFrame.from_records(usd_try_rate_data)
    eur_try_rate_data = pd.DataFrame.from_records(eur_try_rate_data)
    eur_usd_rate_data = pd.DataFrame.from_records(eur_usd_rate_data)
    
    return pd.concat([usd_try_rate_data, eur_try_rate_data, eur_usd_rate_data])
#%%