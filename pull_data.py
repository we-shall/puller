# Scrape the website: https://www.medicineindia.org/

from bs4 import BeautifulSoup
import csv
import requests
import string
from urllib.parse import urljoin

MAIN_LINK = 'https://www.medicineindia.org/'


def get_medicine_by_brandname():
    alphabet_urls = get_alphabet_urls()
    print ('\nStarting the scraping process...\n')
    for url in alphabet_urls:
        try:
            print ('scrape -> %s' %url)
            scrape_url(url=url)
        except:
            # Raise whatever exception you got!
            print ('issue while scraping the link -> %s' %url)
            pass
    print ('\nXXXXXXX - Ending the scraping process - XXXXXXX\n')


def scrape_url(url):
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, 'html.parser')
    count = 0
    table = soup.find('table', attrs={'class': 'table table-striped table-bordered'})
    for table_row in table.findAll('tr', attrs={'class': 'medicine-brand-row'}):
        print (table_row.td.a.span.text)
        # name of medine
        # url of medicine
        # name of company
        # url of company
        # Package
        # strength
        # Price
        
        count += 1
        if count == 10:
            break
    print (count)
    return


def save_scraped_data():
    return 0


def get_alphabet_urls():
    alphabets = string.ascii_lowercase
    medicine_brands = 'medicine-brands/'
    medicine_url = urljoin(MAIN_LINK, medicine_brands)
    alphabet_urls = []

    for alphabet in alphabets:
        alphabet_url = urljoin(medicine_url, alphabet)
        alphabet_urls.append(alphabet_url)

    return alphabet_urls


# get_medicine_by_brandname()
scrape_url(url='https://www.medicineindia.org/medicine-brands/a')
