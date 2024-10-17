import requests
from bs4 import BeautifulSoup

def get_altcoin_season_index():
    url = 'https://www.blockchaincenter.net/altcoin-season-index/'
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # You might need to update this selector after inspecting the website
        index_value_div = soup.find('div', class_='index-value')
        
        if index_value_div is not None:
            index_value = index_value_div.get_text()
            return float(index_value)
        else:
            print("Could not find the Altcoin Season Index on the page.")
            return None
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    index_value = get_altcoin_season_index()
    if index_value is not None:
        print(f"Current Altcoin Season Index: {index_value}")
    else:
        print("Could not retrieve the Altcoin Season Index.")
