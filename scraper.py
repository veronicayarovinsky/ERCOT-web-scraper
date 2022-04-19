# ERCOT Web Scraper: Stores LMPs by Electrical Bus Data daily
# Veronica Yarovinsky - April, 2022

import os
from bs4 import BeautifulSoup
import requests
import zipfile, io
import re
import glob

LMP_DATA_LINK = "http://mis.ercot.com/misapp/GetReports.do?reportTypeId=12300&reportTitle=LMPs%20by%20Resource%20Nodes,%20Load%20Zones%20and%20Trading%20Hubs&showHTMLView=&mimicKey"
# SAVE_PATH = "/Users/veronicayarovinsky/Desktop/ERCOT-web-scraper/ERCOT-data"
SAVE_PATH = os.getcwd() + "/ERCOT-data"

def main():
    new_downloads = scrape()            # scrape webpage for urls to download
    download_files(new_downloads)       # downloads files in reverse order (oldest to most recent)
    print("Downloaded " + str(len(new_downloads)) + " new files to " + SAVE_PATH + ".")


def scrape():
    # read the html using BeautifulSoup
    requests_response = requests.get(LMP_DATA_LINK)
    html = requests_response.text
    page = BeautifulSoup(html, features='lxml')

    new_downloads = []                      # initiate array for urls of files to download

    new_data = True

    print("Locating files to donwload ...")

    if len(os.listdir(SAVE_PATH) ) != 0:        # if files have previously been downloaded
        last_download = get_last_download()     # prevents duplicate downloads

        while new_data == True:
            for table in page.find_all('tr'):                           # prevents duplicates
                for row in table.find_all('tr'):
                    if 'xml' not in str(row) and 'href' in str(row) and new_data == True:
                        download_link = row.find('a').get('href')
                        download_url = requests.get('http://mis.ercot.com' + download_link)
                        filename = get_filename(download_url)

                        if last_download[-19:] == filename[-19:]:       # compares last 19 characters of filename (date and time)
                            new_data = False                            # stops scraping webpage if file has already been downloaded
                        else:
                            new_downloads.append(download_url)

    else:                                       # folder is empty
        for table in page.find_all('tr'):                               # prevents duplicates
            for row in table.find_all('tr'):
                if 'xml' not in str(row) and 'href' in str(row) and new_data == True:
                    download_link = row.find('a').get('href')
                    download_url = requests.get('http://mis.ercot.com' + download_link)
                    filename = get_filename(download_url)
                    new_downloads.append(download_url)

    return new_downloads


def download_files(new_downloads):
    print("Downloading the files ...")
    for url in reversed(new_downloads):
        zip = zipfile.ZipFile(io.BytesIO(url.content))
        zip.extractall(SAVE_PATH)


def get_last_download():
    last_download = max(glob.glob(SAVE_PATH + '/*'), key=os.path.getctime)
    last_download = last_download.replace('_', '.')
    return last_download


def get_filename(download_url):
    file_info = download_url.headers['content-disposition']
    filename = re.findall("filename=(.+)", file_info)[0]
    if '.zip' in filename:
        filename = filename[:-4]
        filename = filename.replace('_', '.')
        
    return filename


main()
