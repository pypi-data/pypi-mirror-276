import requests 
from bs4 import BeautifulSoup

def extractHtml(website,parser):
    r = requests.get(website)
    parsed_data = BeautifulSoup(r.text,parser)
    return parsed_data