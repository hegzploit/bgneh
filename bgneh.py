import contextlib
from operator import itemgetter
from unittest import result
import requests
from bs4 import BeautifulSoup
from iterfzf import iterfzf
from typing import List, Dict, Tuple, Callable
from prettytable import from_csv


def gammal_search(query: str):
    elgammal_search_url = "http://www.elgammalelectronics.com/Home/SearchResults?TheSearchParameter="
    r = requests.get(elgammal_search_url + query)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = []
    table = soup.find('table', attrs={'class': 'gridtable'})
    items = table.find_all('tr')
    for item in items:
        with contextlib.suppress(Exception):
            cols = item.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            link = item.find(attrs={'style': 'cursor:pointer;'}).get('id')
            link = link.split("-")[1:]
            link = "-".join(link)
            link = f"http://www.elgammalelectronics.com/Products/Details/{link}"
            cols.append(link)
            data.append([ele for ele in cols if ele])
    data = [item for item in data if item]
    data = [[f"{item[0]} {item[1]}", float(
        item[2]), item[-1]] for item in data]
    data.sort(key=itemgetter(1))
    return data


def fut_search(query: str):
    fut_search_url = f"https://store.fut-electronics.com/search?page=1&q={query}"
    r = requests.get(fut_search_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        no_of_pages = int(soup.find_all('div', id="paging")[
            0].find_all('a')[-2].text)
    except Exception:
        no_of_pages = 1
    data = []
    for page in range(1, no_of_pages + 1):
        fut_search_url = f"https://store.fut-electronics.com/search?page={page}&q={query}"
        r = requests.get(fut_search_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        grid_div = soup.select('div[class*="four columns"]')
        for item in grid_div:
            item_name = item.findChildren("h3")[0].text
            item_price = item.findChildren("h4")[0].text
            item_price = item_price.strip("LE ").replace(",", "")
            link = item.findChildren("a")[0].get('href')
            link = f"https://store.fut-electronics.com{link}"
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
    results = soup.find(
        'ul', attrs={'class': 'products columns-4 columns__wide--5'})
    results = results.find_all('li')
    for result in results:
        title = result.find(
            'h2', attrs={'class': 'woocommerce-loop-product__title'}).text
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
    results = soup.find(
        'ul', attrs={'class': 'products columns-4 columns__wide--5'})
    results = results.find_all('li')
    for result in results:
        title = result.find(
            'h2', attrs={'class': 'woocommerce-loop-product__title'}).text
        price = result.find(
            'span', attrs={'class': 'woocommerce-Price-amount amount'}).text
        price = price.strip(u'\xa0EGP')
        data.append([title, price])
    return data


SearchEngineFunction = Callable[str, List[Tuple[str, float]]]


class Scraper():

    def __init__(self, shop_engine, query: str):
        self.shop_engine = shop_engine
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        }
        self.query = query

    def run(self) -> List[Tuple[str, float]]:
        return self.shop_engine(self.query)

    def save_to_csv(self, filename: str) -> None:
        from pandas import DataFrame
        data = self.run()
        # make sure it's two columns
        data = [[item[0], item[1]] for item in data]
        df = DataFrame(data,  columns=['Name', 'Price'])
        df.to_csv(filename, index=False)


def main() -> None:
    query = input("Enter query: ")

    shop_engines: dict = {
        "Gammal Electronics": gammal_search,
        "Fut Electronics": fut_search,
        "Ram-E-Shop": ram_search,
        "Free Electronics": free_search,
    }

    search_engine = iterfzf(
        shop_engines,
        multi=True
    )
    for engine in search_engine:
        scarper = Scraper(shop_engine=shop_engines[engine], query=query)
        scarper.save_to_csv(filename=f"{engine}_{query}.csv")
        with open(f"{engine}_{query}.csv", 'r') as f:
            print(from_csv(f))


main()
