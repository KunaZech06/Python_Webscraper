# Import packages
import requests
from bs4 import BeautifulSoup
import sqlite3

# Declaring url, webdriver and extract page content
myUrl = 'https://www.barnesandnoble.com/w/effective-python-brett-slatkin/1130203296?ean=9780134853987'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (HTML, like Gecko) "
                         "Chrome/79.0.3945.88 Safari/537.36 "}

# Create Data-table and connecting to Database.
conn = sqlite3.connect('webScrape_k.db')
c = conn.cursor()
c.execute(''' CREATE TABLE IF NOT EXISTS data_k(isbn_13 TEXT, Publisher TEXT, PublicationDate TEXT, 
Series TEXT, EditionDescription TEXT, Pages INT, 
SalesRank TEXT, Width REAL, Height REAL, 
Depth REAL, Price REAL) ''')


def webScrapper(url):
    page = requests.get(myUrl, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')
    table_data = soup.find_all('tr')
    print(table_data)
    # Extract required information
    isbn_13 = table_data[0].text.replace("\n", "").replace(":", ": ")
    print(isbn_13)
    publisher = table_data[1].text.replace("\n", "").replace(":", ": ")
    print(publisher)
    publicationDate = table_data[2].text.replace("\n", "").replace(":", ": ")
    print(publicationDate)
    series = table_data[3].text.replace("\n", "").replace(":", ": ")
    print(series)
    editionDescription = table_data[4].text.replace("\n", "").replace(":", ": ")
    print(editionDescription)
    pages = table_data[5].text.replace("\n", "").replace(":", ": ")
    print(pages)
    salesRank = table_data[6].text.replace("\n", "").replace(":", ": ")
    print(salesRank)

    # getting individual product dimensions.
    fullWidth = table_data[7].text
    fullWidth = fullWidth.split(" x ")
    productWidth = fullWidth[0].replace("\n", "").replace('Product dimensions: ', "")
    print("Product Width: " + productWidth)
    productHeight = fullWidth[1]
    print("Product Height: " + productHeight)
    productDepth = fullWidth[2]
    print("Product Depth: " + productDepth)

    # Retrieve price
    dataPrice = soup.find_all('div', class_="price-current-old-details")
    for i in dataPrice:
        price = i.text.replace("\n", "")
    print("Price: " + price)
    print("\n" + "\n")

    # Commit data into Database.
    c.execute("INSERT INTO data_k VALUES(?,?,?,?,?,?,?,?,?,?,?)",
              (isbn_13, publisher, publicationDate, series, editionDescription,
               pages, salesRank, productWidth, productHeight, productDepth, price))
    conn.commit()


webScrapper(myUrl)

# This code is when the HTML is downloaded as a local file.
'''
with open('file1.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')
    table_data_header = soup.find_all('th')
    table_data = soup.find_all('td')
    # print(table_data)
'''

# Checking Database data.
c.execute(''' SELECT * FROM data_k''')
results = c.fetchall()
print(results)

conn.close()
