# 
"""
Scrapes the website: https://www.medicineindia.org/

collected 35k medicine details

"""

from bs4 import BeautifulSoup
import csv
import os
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
    print ('============ Scraping URL %s ============' %url)
    response = requests.get(url=url)
    alphabet = url[-1]
    soup = BeautifulSoup(response.content, 'html.parser')
    count = 0
    table = soup.find('table', attrs={'class': 'table table-striped table-bordered'})
    table_data = []
    for table_row in table.findAll('tr', attrs={'class': 'medicine-brand-row'}):
        # print (table_row.td.a.span.text)
        row_data = {}
        row_data['medicine'] = table_row.td.a.span.text
        row_data['description_url'] = table_row.td.a['href']
        company_info = table_row.find('td', attrs = {'itemprop': 'manufacturer'})
        row_data['company'] = company_info.a.span.text
        row_data['company_url'] = company_info.a['href']
        # row_data['package'] = table_row.td.text
        # row_data['strength'] = table_row.td.text
        row_data['price'] = table_row.find('td', attrs={'itemprop': 'offers'}).span.text
        table_data.append(row_data)
        count += 1
        # if count == 10:
        #     break
    save_scraped_data(table_data, alphabet=alphabet)
    print ('COUNT OF ROWS %s' %count)
    print ('============= completed scraping %s =============' %url)


def save_scraped_data(table_data, alphabet):
    alphabet = alphabet + '.csv'
    header_keys = table_data[0].keys()
    store_location = os.path.join(os.getcwd(), 'ExtractedData', 'medicineIndia', alphabet)
    print ('+++++++ Writing data to csv at %s +++++++' % store_location)

    with open(store_location, 'w') as ofile:
        dict_writer = csv.DictWriter(ofile, header_keys)
        dict_writer.writeheader()
        dict_writer.writerows(table_data)
    
    print ('\n\n+++++++ Done writing data to CSV file +++++++\n')


def get_alphabet_urls():
    alphabets = string.ascii_lowercase
    medicine_brands = 'medicine-brands/'
    medicine_url = urljoin(MAIN_LINK, medicine_brands)
    alphabet_urls = []

    for alphabet in alphabets:
        alphabet_url = urljoin(medicine_url, alphabet)
        alphabet_urls.append(alphabet_url)

    return alphabet_urls


get_medicine_by_brandname()
