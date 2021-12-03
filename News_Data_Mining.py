import requests
from bs4 import BeautifulSoup
import csv

####File for the first CSV
new_file = open("C:/Users/user/Desktop/DATA SCIENCE/Assignments/News_data_mining.csv", mode = "w", encoding = "utf-8", newline = "")
pen = csv.writer(new_file)
pen.writerow(["S/N", "News link", "news source", "Date Reported"])
News_data_link = []
index = 1

# ####File for the 2nd CSV
new_file2 = open("C:/Users/user/Desktop/DATA SCIENCE/Assignments/News_data_content_mining.csv", mode = "w", encoding = "utf-8", newline = "")
pen2 = csv.writer(new_file2)
pen2.writerow(["S/N", "News Content", "news source", "Date Reported"])
News_data_content = []
index2 = 1

for num in range(1, 100):
    # To get urls from pagination
    url = ""
    if num == 1:
        url = "https://punchng.com/?s=bandit" 
    else:
        url = f"https://punchng.com/page/{num}/?s=bandit"


    headers = requests.utils.default_headers()
    headers.update(
        { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
        )

    my_response = requests.get(url, headers)
    # print(my_response.status_code)

    first_soup = BeautifulSoup(my_response.content, features = "lxml")
    # print(first_soup)


    articles_pages = first_soup.find("div", attrs = {"class" : "nav-links"})
    list_of_article_pages = articles_pages.find()
    for pages in list_of_article_pages: ###For loop for all the pages
        list_of_article_pages.find("a")

        second_soup = first_soup.find("div", attrs = {"class" : "columns column-content"}) ### .find is a method
        # print(second_soup)

        list_of_soups = second_soup.find_all("div", attrs = {"class" : "entry entry-box"})
        # print(list_of_soups)

        ###News Source
        for soup in list_of_soups: 
            print(soup.prettify())
            news_source = "Punch"

            ###news_link
            try:
                news_details = soup.find("a")
                # print(news_details)
                news_link = news_details.get("href")
                # print(news_link)
            except:
                news_details = None
                news_link = None

            ###Getting all the links for the dates
            try:
                news_details = soup.find("a")
                news_link = news_details.get("href")
                url2 = f"{news_link}"
            except:
                news_details = None
                news_link = None
                url2 = None

            my_response2 = requests.get(url2, headers)
            # print(my_response2.status_code)

            First_soup2 = BeautifulSoup(my_response2.content, features = "lxml")
            # print(First_soup2)

            second_soup2 = First_soup2.find("div", attrs = {"class" :"entry-content"})
            # print(second_soup2)

            try:
                news_date_raw = second_soup2.find("span", attrs = {"class" : "entry-date"})
                news_date = news_date_raw.text
                if "Published " in news_date:
                    refine_news_date = news_date.lstrip("Published")
                    # print(refine_news_date)
                else:
                    refine_news_date = news_date
            except:
                news_date_raw = None
                news_date = None

            try:
                news_article =second_soup2.find("p")
                news_real_article = news_article.text
            except:
                news_article = None

                ###Writing into the files
            News_data_link.append([index, news_link, news_source, refine_news_date])
            index += 1

            News_data_content.append([index2, news_real_article, news_source, refine_news_date])
            index2 += 1

pen.writerows(News_data_link)
new_file.close()
pen2.writerows(News_data_content)
new_file2.close()    

