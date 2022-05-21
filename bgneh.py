import requests
from bs4 import BeautifulSoup


def gammal_search(query: str):
    elgammal_search_url = "http://www.elgammalelectronics.com/Home/SearchResults?TheSearchParameter="
    r = requests.get(elgammal_search_url + query)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = []
    table = soup.find('table', attrs={'class':'gridtable'})
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values
    # returns a list of lists
    # each list is of the format ['ITEM_NAME', 'ITEM_DESC', 'PRICE_NUM', 'CURRENCY']
    return data

def fut_search(query: str):
    fut_search_url = f"https://store.fut-electronics.com/search?page=1&q={query}"
    r = requests.get(fut_search_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    no_of_pages = soup.find_all('div', id="paging")[0].find_all('a')[-2].text
    data = []
    for page in range(1, int(no_of_pages) + 1):
        fut_search_url = f"https://store.fut-electronics.com/search?page={page}&q={query}"
        r = requests.get(fut_search_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        grid_div = soup.find_all('div', attrs={'class':'four columns'})
        for item in grid_div:
            item_name = item.findChildren("h3")
            item_price = item.findChildren("h4")
            data.append([item_name[0].text, item_price[0].text])
    return data

