#%%
import requests
import pandas as pd

# Specify the parameters for the API request
start_date = '2023-05-01'
end_date = '2023-05-07'
country_codes = ['DE', 'SE', 'NO']  # Replace with the desired country codes

# Create an empty DataFrame to store the results
result_df = pd.DataFrame()

# Iterate through each country code
for country_code in country_codes:
    # Construct the API endpoint URL
    url = f'https://www.nordpoolgroup.com/api/marketdata/page/24?currency=,EUR,EUR&endDate={end_date}&startDate={start_date}&country={country_code}'

    # Send the API request and retrieve the data
    response = requests.get(url)
    data = response.json()

    # Extract the hourly prices from the response
    hourly_prices = data['data']['Rows']

    # Create a DataFrame from the hourly prices data
    df = pd.DataFrame(hourly_prices)

    # Convert the timestamp to a datetime object
    df['Time'] = pd.to_datetime(df['StartTime'])

    # Convert the PriceAmount column to numeric
    df['PriceAmount'] = pd.to_numeric(df['PriceAmount'])

    # Group the data by hour and calculate the average price
    hourly_average = df.groupby(df['Time'].dt.hour)['PriceAmount'].mean()

    # Append the hourly average prices to the result DataFrame
    result_df[country_code] = hourly_average

# Display the result DataFrame
print(result_df)
