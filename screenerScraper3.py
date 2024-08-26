import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Fetch the webpage
url = "https://www.screener.in/company/RELIANCE/consolidated/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract tables and other data
tables = soup.find_all('table', class_='data-table')
other_data = soup.find_all('div', class_='specific-class-or-id')  # Adjust the class or ID based on what you're targeting

all_data = []

# Process the tables
for table in tables:
    headers = [re.sub(r'\s*\+$', '', header.text.strip()) for header in table.find_all('th')]
    rows = []
    for row in table.find_all('tr'):
        cols = [re.sub(r'\s*\+$', '', ele.text.strip()) for ele in row.find_all('td')]
        if cols:
            rows.append(cols)
    if rows:
        df = pd.DataFrame(rows, columns=headers)
        all_data.append(df)

# Process other data
# Example: Extracting text from divs
for data in other_data:
    text_content = data.get_text(strip=True)
    # Do something with this text, such as adding it to a DataFrame or appending it to a list

# Concatenate all DataFrames and save to CSV
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv('reliance_data_cleaned.csv', index=False)
    print("Table data saved to reliance_data_cleaned.csv")

# Optionally save other data to a separate CSV or add it to the existing one

print("Additional data processed")
