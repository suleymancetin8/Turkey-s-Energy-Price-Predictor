#%% IMPORTING LIBRARIES
import pandas as pd
from seffaflik.elektrik import santraller, tuketim, uretim, yekdem
from seffaflik.elektrik.piyasalar import dengesizlik, dgp, genel, gip, gop, ia, yanhizmetler
from seffaflik.__ortak.__araclar import make_requests as __make_requests
from datetime import datetime, timedelta



#%%

def fetch_seffaflik_datas(start_date, end_date):


    happened_production_data = uretim.gerceklesen(baslangic_tarihi= start_date, bitis_tarihi=end_date)
    happened_production_data = happened_production_data[["Tarih", "Saat", "Toplam"]]
    happened_production_data.rename(columns={"Toplam": "GERÇEKLEŞEN ÜRETİM"}, inplace=True)
    
    planned_production_data = uretim.kgup(baslangic_tarihi=start_date, bitis_tarihi=end_date)
    planned_production_data = planned_production_data[["Tarih", "Saat", "Toplam"]]
    planned_production_data.rename(columns={"Toplam": "PLANLANAN ÜRETİM"}, inplace=True)
    
    happened_usage_data = tuketim.gerceklesen(baslangic_tarihi=start_date, bitis_tarihi=end_date)
    happened_usage_data.rename(columns={"Tüketim": "GERÇEKLEŞEN TÜKETİM"}, inplace=True)
    
    planned_usage_data = tuketim.tahmin(baslangic_tarihi=start_date, bitis_tarihi=end_date)
    planned_usage_data.rename(columns={"Tüketim": "PLANLANAN TÜKETİM"}, inplace=True)
    
    happened_day_ahead_price_data = gop.ptf(baslangic_tarihi=start_date, bitis_tarihi = end_date)
    happened_day_ahead_price_data.rename(columns={"PTF": "PTF (TRY/MWh)"}, inplace=True)
    
    # temp_dt = datetime.strptime(start_date, '%Y-%m-%d')
    # end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')
    # planned_day_ahead_price_data = pd.DataFrame()

    # while temp_dt <= end_date_dt:
    #     temp_str_time = temp_dt.strftime('%Y-%m-%d')
    #     print(temp_str_time)
    #     temp_data = gop.kptf(tarih=temp_str_time)
    #     print(temp_data)
    #     planned_day_ahead_price_data =pd.concat([planned_day_ahead_price_data, temp_data], ignore_index=True)
    #     temp_dt += timedelta(days=1)  
    
    
    seffaflik_data = pd.merge(happened_production_data, planned_production_data, on=["Tarih", "Saat"])
    seffaflik_data = pd.merge(seffaflik_data, happened_usage_data, on=["Tarih", "Saat"])
    seffaflik_data = pd.merge(seffaflik_data, planned_usage_data, on=["Tarih", "Saat"])
    seffaflik_data = pd.merge(seffaflik_data, happened_day_ahead_price_data, on=["Tarih", "Saat"])

    seffaflik_data["Saat"] = seffaflik_data["Saat"].astype(str).str.zfill(2)
    # seffaflik_data["Tarih"] = seffaflik_data["Tarih"].astype(str)
    # seffaflik_data["Saat"] = seffaflik_data["Saat"].astype(str)
    return seffaflik_data
#%%
