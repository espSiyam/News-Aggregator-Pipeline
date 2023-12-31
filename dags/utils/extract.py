import requests
from bs4 import BeautifulSoup
import logging
import pickle

PROTHOM_ALO_XML_URL = "https://www.prothomalo.com/sitemap.xml"
JUGANTOR_XML_URL = "https://www.jugantor.com/sitemap.xml"
KALER_KANTHO_XML_URL = "https://www.kalerkantho.com/sitemap.xml"

PROTHOM_ALO_URL_LIST = "dags/data/prothomalo_urls_list.pkl"
JUGANTOR_URL_LIST = "dags/data/jugantor_urls_list.pkl"
KALER_KANTHO_URL_LIST = "dags/data/kalerkantho_urls_list.pkl"

logger = logging.getLogger(__name__)

def fetch_xml_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return BeautifulSoup(response.content, "xml")
    except Exception as e:
        logger.error(f"Could not fetch content due to error: {str(e)}")

def parse_sitemap(xml_soup):
    news_urls = xml_soup.find_all("url")
    result = [xml_url.find('loc').text for xml_url in news_urls]
    return result

def save_list_to_file(list_to_save, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(list_to_save, f)

def parse_from_prothomalo():
    initial_sitemap_soup = fetch_xml_content(PROTHOM_ALO_XML_URL)
    latest_sitemap_url = initial_sitemap_soup.find("lastmod").find_next("loc").text
    
    sitemap_index_soup = fetch_xml_content(latest_sitemap_url)
    save_list_to_file(parse_sitemap(sitemap_index_soup), PROTHOM_ALO_URL_LIST)
    logger.info("Extracted URLs from Prothom Alo. Total URLs: {}".format(len(parse_sitemap(sitemap_index_soup))))

def parse_from_jugantor():
    sitemap_soup = fetch_xml_content(JUGANTOR_XML_URL)
    all_links = sitemap_soup.find_all('loc')
    
    irrelevant_links = [link.text for link in all_links if len(link.text.split("/")) < 6]
    proper_links = list(set(link.text for link in all_links) - set(irrelevant_links))
    save_list_to_file(proper_links, JUGANTOR_URL_LIST)
    logger.info("Extracted URLs from Jugantor. Total URLs: {}".format(len(proper_links)))

def parse_from_kalerkantho():
    sitemap_soup = fetch_xml_content(KALER_KANTHO_XML_URL)
    latest_news_sitemap = sitemap_soup.find_all("loc")[1].text
    news_sitemap_soup = fetch_xml_content(latest_news_sitemap)
    save_list_to_file(parse_sitemap(news_sitemap_soup), KALER_KANTHO_URL_LIST)
    logger.info("Extracted URLs from Kaler Kantho. Total URLs: {}".format(len(parse_sitemap(news_sitemap_soup))))   