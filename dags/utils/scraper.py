import newspaper
import logging
from deep_translator import GoogleTranslator
from datetime import datetime

logger = logging.getLogger(__name__)

def scrape_category_urls(url):
    try:
        if "kalerkantho" in url:
            cat = url.split("/")[4]
            return cat
        else:
            cat = url.split("/")[3]
            return cat
    except Exception as e:
        logger.error(f"Could not scrape category due to error: {str(e)}")

def scrape_data_from_url(url):
    date = datetime.now().strftime("%Y-%m-%d")
    try:
        article = newspaper.Article(url)
        article.download()
        article.parse()

        title = article.title
        text = article.meta_description
        translated_title = GoogleTranslator(source='auto', target='en').translate(title)
        translated_text = GoogleTranslator(source='auto', target='en').translate(text)
        top_image = article.top_image
        category = scrape_category_urls(url)
        website = url.split('.')[1]

        logger.info(f"Scraped data from URL: {url}")

        return {
            'date': date,
            'website': website,
            'url': url,
            'title': title,
            'text': text,
            'translated_title': translated_title,
            'translated_text': translated_text,
            'category': category,
            'main_image': top_image
        }

    except Exception as e:
        logger.error(f"Could not scrape data due to error: {str(e)}")
        return {
            'date': date,
            'url': url,
            'title': None,
            'text': None,
            'main_image': None
        }   