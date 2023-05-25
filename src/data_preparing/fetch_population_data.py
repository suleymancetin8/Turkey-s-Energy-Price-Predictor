#%%
import requests
import pandas as pd
from datetime import datetime


def fetch_population_data(start_date, end_date):
    start_year = start_date[0:4]
    end_year = end_date[0:4]
    # API endpoint and parameters
    url = "https://api.worldbank.org/v2/country/TUR/indicator/SP.POP.TOTL"
    params = {
        "format": "json",
        "date": str(start_year) + ":" + str(end_year)
    }

    # Make the API request
    response = requests.get(url, params=params)
    data = response.json()[1]  # Extract the data from the response

    # Extract year and population from the data
    years = [entry['date'] for entry in data]
    population = [entry['value'] for entry in data]

    # Create a dataframe
    df = pd.DataFrame({'Tarih': years, 'Nüfus': population})



    df.loc[df['Tarih'].str.contains('2022'), 'Nüfus'] = 84339267
    new_row = pd.Series({'Tarih': '2023', 'Nüfus': 84320888})
    # Concatenate new row at the top
    df = pd.concat([pd.DataFrame([new_row]), df], ignore_index=True)
    df.reset_index(inplace=True, drop=True)
    # Print the dataframe
    print(df)




    # Original population data
    df_population = pd.DataFrame({
        # 'Tarih': ['2023-01-01','2022-01-01', '2021-01-01', '2020-01-01', '2019-01-01', '2018-01-01'],
        "Tarih": df["Tarih"],
        # 'Nüfus': [84320888, 84339267.0, 84775404.0, 84135428.0, 83481684.0, 82809304.0]
        "Nüfus": df["Nüfus"]
    })

    # Convert 'Tarih' column to datetime
    for index in range(len(df_population)):
        df_population['Tarih'].loc[index] = datetime.strptime(df_population['Tarih'].loc[index], '%Y') 
        



    # Generate complete datetime index
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    # end_date = start_date + pd.DateOffset(years=6,)
    index = pd.date_range(start_date, end_date, freq='H')

    # Create the dataset with Tarih and Saat columns
    df_complete = pd.DataFrame(index=index)
    df_complete['Tarih'] = df_complete.index
    df_complete['Saat'] = df_complete.index.strftime('%H')

    # Merge the population data with the complete dataset
    df_merged = pd.concat([df_complete, df_population.set_index('Tarih')], axis=1, join='outer')

    # Fill missing 'Nüfus' values with the last known population value
    df_merged['Nüfus'] = df_merged['Nüfus'].ffill()

    
    
    # Reset the index, format 'Tarih' column, and rename the columns
    df_merged = df_merged.reset_index()
    df_merged['Tarih'] = df_merged['Tarih'].dt.strftime('%Y-%m-%d')
    df_merged = df_merged.rename(columns={'index': 'Tarih'})

    # Reorder the columns
    df_merged = df_merged[['Tarih', 'Saat', 'Nüfus']]
    df_merged = df_merged.iloc[:, 1:]
    # Print the merged dataset
    #df_merged.drop(columns=['Tarih','Saat'], inplace=True)
    # df_merged['Tarih'] = df_merged['Tarih'].astype(str)
    # df_merged['Saat'] = df_merged['Saat'].astype(str)
    return df_merged
# %%
