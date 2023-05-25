#%%
import pandas as pd
import requests


# Fetch the TL interest rate data from the Central Bank of the Republic of Turkey's public API
def fetch_tl_interest_rate(start_date, end_date):
    url = f'https://evds2.tcmb.gov.tr/service/evds/series=TP.DK.USD.A.YTL-0074&pageNumber=1&startDate={start_date}&endDate={end_date}&type=json'
    response = requests.get(url)
    data = response.json()

    # Extract the interest rate data from the API response
    interest_rate_data = data['items']

    # Create an hourly date range between the start and end dates
    date_range = pd.date_range(start=start_date, end=end_date, freq='H')

    # Create an hourly DataFrame with the date range
    hourly_df = pd.DataFrame({'Date': date_range})

    # Set the Date column as the index of the DataFrame
    hourly_df.set_index('Date', inplace=True)

    # Extract the interest rate values from the data and convert them to float
    interest_rates = [float(item['TP_DK_USD_A_YTL_0074']) for item in interest_rate_data]

    # Repeat each interest rate value for each hour within the hour range
    hourly_interest_rates = pd.Series(interest_rates, index=date_range).ffill()

    # Assign the hourly interest rates to the DataFrame
    hourly_df['TL Interest Rate'] = hourly_interest_rates
    
    return hourly_df

    # %%
