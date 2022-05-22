from operator import itemgetter
from unittest import result
import requests
from bs4 import BeautifulSoup


# def gammal_search(query: str):
#     elgammal_search_url = "http://www.elgammalelectronics.com/Home/SearchResults?TheSearchParameter="
#     r = requests.get(elgammal_search_url + query)
#     soup = BeautifulSoup(r.text, 'html.parser')
#     data = []
#     table = soup.find('table', attrs={'class':'gridtable'})
#     rows = table.find_all('tr')
#     for row in rows:
#         cols = row.find_all('td')
#         cols = [ele.text.strip() for ele in cols]
#         data.append([ele for ele in cols if ele]) # Get rid of empty values
#     # returns a list of lists
#     # each list is of the format ['ITEM_NAME', 'ITEM_DESC', 'PRICE_NUM', 'CURRENCY']
#     return data
# 
def gammal_search(query: str):
    elgammal_search_url = "http://www.elgammalelectronics.com/Home/SearchResults?TheSearchParameter="
    r = requests.get(elgammal_search_url + query)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = []
    table = soup.find('table', attrs={'class':'gridtable'})
    items = table.find_all('tr')
    for item in items:
        try:
            cols = item.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            link = item.find(attrs={'style':'cursor:pointer;'}).get('id')
            link = link.split("-")[1:]
            link = "-".join(link)
            link = "http://www.elgammalelectronics.com/Products/Details/" + link
            cols.append(link)
            data.append([ele for ele in cols if ele])
        except:
            pass
    data = [item for item in data if item]
    data = [[f"{item[0]} {item[1]}", float(item[2]), item[-1]] for item in data]
    data.sort(key=itemgetter(1))
    return data


def fut_search(query: str):
    fut_search_url = f"https://store.fut-electronics.com/search?page=1&q={query}"
    r = requests.get(fut_search_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        no_of_pages = soup.find_all('div', id="paging")[0].find_all('a')[-2].text
    except:
        no_of_pages = 1
    data = []
    for page in range(1, int(no_of_pages) + 1):
        fut_search_url = f"https://store.fut-electronics.com/search?page={page}&q={query}"
        r = requests.get(fut_search_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        grid_div = soup.select('div[class*="four columns"]')
        for item in grid_div:
            item_name = item.findChildren("h3")[0].text
            item_price = item.findChildren("h4")[0].text
            item_price = item_price.strip("LE ").replace(",", "")
            link = item.findChildren("a")[0].get('href')
            link = "https://store.fut-electronics.com" + link
            data.append([item_name, float(item_price), link])
    data.sort(key=itemgetter(1))
    return data

# Test this more cuz it seems to break often
def ram_search(query: str):
    params = {
        's': query,
        'product_cat': '0',
        'post_type': 'product',
    }

    data = {
        'ppp': '-1',
        's': 'ic',
        'product_cat': '0',
        'post_type': 'product',
    }
    r = requests.post('https://ram-e-shop.com/', params=params, data=data)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = []
    results = soup.find('ul', attrs={'class':'products columns-4 columns__wide--5'})
    results = results.find_all('li')
    for result in results:
        title = result.find('h2', attrs={'class':'woocommerce-loop-product__title'}).text
        price = result.find('bdi').text
        data.append([title, price])
    return data

def free_search(query: str):
    params = {
        's': query,
        'product_cat': '0',
        'post_type': 'product',
    }

    data = {
        'ppp': '-1',
        's': 'ic',
        'product_cat': '0',
        'post_type': 'product',
    }
    r = requests.post('https://free-electronic.com/', params=params, data=data)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = []
    results = soup.find('ul', attrs={'class':'products columns-4 columns__wide--5'})
    results = results.find_all('li')
    for result in results:
        title = result.find('h2', attrs={'class':'woocommerce-loop-product__title'}).text
        price = result.find('span', attrs={'class':'woocommerce-Price-amount amount'}).text
        price = price.strip(u'\xa0EGP')
        data.append([title, price])
    return data

print(ram_search("ic"))