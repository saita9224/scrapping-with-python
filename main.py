import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL
url = "https://www.jumia.co.ke/"

# Send a GET request to the URL
page = requests.get(url)

data = []
if page.status_code == 200:
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(page.text, "html.parser")
    
    all_ele = soup.find_all("a", class_="core")

    for ele in all_ele:
        item = {}

        # Extract title
        title_elem = ele.find("div", class_="name")
        if title_elem:
            item['Title'] = title_elem.text.strip()
        else:
            item['Title'] = "Title not available"

        # Extract price
        price_elem = ele.find("div", class_="prc")
        if price_elem:
            item['Price'] = price_elem.text.strip()[3:]  # Assuming 'SH ' prefix
            # Extract previous price from data-oprc attribute
            data_oprc_value = price_elem.get("data-oprc")  # No need to check again
            if data_oprc_value:
                item['Pre_price'] = data_oprc_value.strip()  # Assuming no prefix removal needed
            else:
                item['Pre_price'] = "Previous price not available"
        else:
            item['Price'] = "Price not available"
            item['Pre_price'] = "Previous price not available"

        data.append(item)

    # Create DataFrame
    df = pd.DataFrame(data) 

    # Write DataFrame to Excel file
    df.to_excel("Jumia.xlsx", index=False)  # Specify index=False to omit row numbers
else:
    print(f"Failed to retrieve the page. Status code: {page.status_code}")
