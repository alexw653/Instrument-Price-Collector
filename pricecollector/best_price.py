from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

def print_products(search):
    acc = search.replace(" ", "-")

    url = f"https://www.sharmusic.com/search?keywords={acc}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    page_text = doc.find(class_="global-views-pagination-count")

    pages = int(str(page_text).split(">")[1].split("<")[0].split("of ")[1])
    num_pages = input(f"There are {pages} pages for this product, how many pages do you want to look through? (Enter an Integer) ")
    n_pages = int(num_pages)

    items_found = {}

    for page in range(1, n_pages + 1):
        url = f"https://www.sharmusic.com/search?page={page}&keywords={acc}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        #print(doc)
        div = doc.find(class_="facets-facet-browse-items")
        items = div.find_all(text=re.compile(search))
        #print(items)
        for item in items:
            parent = item.parent.parent
            link = None
            if parent.name == "a":
                link = parent['href']
                l = "https://www.sharmusic.com"+str(link)
                try:
                    price = parent.parent.next_sibling.find(class_="product-views-price-lead custom-related-item").string
                    fixed_price = price.replace(",", "").replace("$","")
                    #print(fixed_price)
                    items_found[item] = {"price": float(fixed_price), "link": l}
                except:
                    pass

    sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])

    for item in sorted_items:
        print(item[0])
        print(f"${item[1]['price']}")
        print(item[1]['link'])
        print("______________________________________________________________")

    return sorted_items

def convert_to_df(sorted_items):
    frame = pd.DataFrame()
    name_list = []
    price_list = []
    link_list = []
    for item in sorted_items:
        name_list.append(item[0])
        price_list.append(item[1]['price'])
        link_list.append(item[1]['link'])
    frame['Product Name'] = name_list
    frame['Price'] = price_list
    frame['Link'] = link_list
    frame.set_index("Product Name", inplace = True)
    return frame

if __name__ == "__main__":
    search = input("What instrument accessory do you want to search for? (capitalize first letter of each word) ")
    sorted_items = print_products(search)
    df = convert_to_df(sorted_items)
    print(df)
