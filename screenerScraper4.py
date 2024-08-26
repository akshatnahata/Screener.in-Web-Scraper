import requests
from bs4 import BeautifulSoup
import pandas as pd

# Fetch the webpage
url = "https://www.screener.in/company/RELIANCE/consolidated/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the <li> elements with the desired structure
items = soup.find_all('li', class_='flex flex-space-between')

# Extract the names and values
data = []
for item in items:
    name = item.find('span', class_='name').get_text(strip=True)
    value = item.find('span', class_='number').get_text(strip=True)
    # Handling potential currency or percentage symbols
    value = value.replace('₹', '').replace('%', '').strip()
    data.append([name, value])

# Save to CSV
df = pd.DataFrame(data, columns=['Name', 'Value'])
df.to_csv('key_value_data.csv', index=False)

print("Data saved to key_value_data.csv")
