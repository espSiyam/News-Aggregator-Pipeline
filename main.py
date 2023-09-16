import requests
from bs4 import BeautifulSoup

PROTHOM_ALO_XML_URL = "https://www.prothomalo.com/sitemap.xml"
JUGANTOR_XML_URL = "https://www.jugantor.com/sitemap.xml"
KALER_KANTHO_XML_URL = "https://www.kalerkantho.com/sitemap.xml"

def fetch_xml_content(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, "xml")

def parse_sitemap(xml_soup):
    news_urls = xml_soup.find_all("url")
    result = [xml_url.find('loc').text for xml_url in news_urls]
    return result

def parse_from_prothomalo():
    initial_sitemap_soup = fetch_xml_content(PROTHOM_ALO_XML_URL)
    latest_sitemap_url = initial_sitemap_soup.find("lastmod").find_next("loc").text
    
    sitemap_index_soup = fetch_xml_content(latest_sitemap_url)
    return parse_sitemap(sitemap_index_soup)

def parse_from_jugantor():
    sitemap_soup = fetch_xml_content(JUGANTOR_XML_URL)
    all_links = sitemap_soup.find_all('loc')
    
    irrelevant_links = [link.text for link in all_links if len(link.text.split("/")) < 6]
    proper_links = list(set(link.text for link in all_links) - set(irrelevant_links))
    return proper_links

def parse_from_kalerkantho():
    sitemap_soup = fetch_xml_content(KALER_KANTHO_XML_URL)
    latest_news_sitemap = sitemap_soup.find_all("loc")[1].text
    news_sitemap_soup = fetch_xml_content(latest_news_sitemap)
    return parse_sitemap(news_sitemap_soup)

if __name__ == "__main__":
    prothomalo_urls = parse_from_prothomalo()
    print("Prothom Alo URLs:")
    print("Total URLs:", len(prothomalo_urls))
    print(prothomalo_urls[:5])

    jugantor_urls = parse_from_jugantor()
    print("\nJugantor URLs:")
    print("Total URLs:", len(jugantor_urls))
    print(jugantor_urls[:5])

    kalerkantho_urls = parse_from_kalerkantho()
    print("\nKaler Kantho URLs:")
    print("Total URLs:", len(kalerkantho_urls))
    print(kalerkantho_urls[:5])
