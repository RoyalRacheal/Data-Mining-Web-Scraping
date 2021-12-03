import requests
from bs4 import BeautifulSoup
import csv

new_file = open("C:/Users/user/Desktop/DATA SCIENCE/Assignments/smartphones_data_mining.csv", mode = "w", encoding = "utf-8", newline = "")
pen = csv.writer(new_file)
pen.writerow(["S/N", "Brand", "Specifications", "old price", "old lp", "old hp", "new price", "new lp", "new hp", "discount", "rating"])
smartphones_data = []
index = 1
        

url = "https://www.jumia.com.ng/smartphones/"
headers = requests.utils.default_headers()
headers.update(
    {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"}
    )

my_response = requests.get(url, headers)
# print(my_response.status_code)

first_soup = BeautifulSoup(my_response.content, features = "lxml")
# print(first_soup)


pages_soup = first_soup.find("div", attrs = {"class" : "pg-w -ptm -pbxl"})  ###For each pages
list_of_pages_soup = pages_soup.find_all()

for pages in list_of_pages_soup: ###A for loop for the pages
    print(pages.prettify())
    smartphone_pages = pages.find("a")

    second_soup = first_soup.find("div", attrs = {"class" : "-paxs row _no-g _4cl-3cm-shs"})
    # print(second_soup)

    list_of_soups = second_soup.find_all("article", attrs = {"class" : "prd _fb col c-prd"})

    ####A for loop for each smartphone
    for soup in list_of_soups: 
        print(soup.prettify())
        smartphones_details = soup.find("a")
        
        ###Phone's brand
        smartphones_brand = smartphones_details.get("data-brand")
        print(smartphones_brand)

        ##Smartphones' specification
        Specifications_div = soup.find("div", attrs = {"class" : "info"})
        Specifications_raw = Specifications_div.text
        if "₦" in Specifications_raw:
            Specifications = Specifications_raw.split("₦")[0]
            print(Specifications)
        
        ###old_price
        try: ###if there is an old price
            old_price_div = soup.find("div", attrs = {"class" : "old"})
            old_price_raw = old_price_div.text
            if "-" in old_price_raw:
                old_lp = int(old_price_raw.split(" - ")[0].lstrip("₦ ").replace(",", ""))
                old_hp = int(old_price_raw.split(" - ")[1].lstrip("₦ ").replace(",", ""))
                smartphones_old_price = None
            else: ###If there is a single price
                smartphones_old_price = int(old_price_raw.lstrip("₦ ").replace(",", ""))
                print(smartphones_old_price)
                old_lp = None
                old_hp = None
        except:
            smartphones_old_price = None
            old_lp = None
            old_hp = None

        ###New price
        try:
            new_smartph_div = soup.find("div", attrs = {"class" : "prc"})
            new_price_raw = new_smartph_div.text
            if "-" in new_price_raw:
                new_lp = int(new_price_raw.split(" - ")[0].lstrip("₦ ").replace(",", ""))
                new_hp = int(new_price_raw.split(" - ")[1].lstrip("₦ ").replace(",", ""))
                smartphones_new_price = None
            else:
                smartphones_new_price = int(new_price_raw.lstrip("₦ ").replace(",", ""))
                print(smartphones_new_price)
                new_lp = None
                new_hp = None
        except:
            sneaker_new_price = None
            new_lp = None
            new_hp = None
        
        ###Discount
        try:
            smartph_discount_div = soup.find("div", attrs = {"class" : "tag _dsct _sm"})
            smartphones_discount = smartph_discount_div.text 
            print(smartphones_discount)  
        except:
            smartphones_discount = None

        ###Smartphone's rating
        try:
            rating_div = soup.find("div", attrs = {"class" : "stars _s"})
            smart_rating_phrase = rating_div.text
            # print(rating_phrase)
            smartphones_rating = float(smart_rating_phrase.split(" ")[0])
            print(smartphones_rating)
        except:
            smartphones_rating = None
        smartphones_data.append([smartphones_brand, Specifications, smartphones_old_price, old_lp, old_hp, smartphones_new_price, new_lp, new_hp, smartphones_discount, smartphones_rating])
        index += 1

pen.writerows(smartphones_data)
new_file.close()
