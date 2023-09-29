import newspaper
import logging
from deep_translator import GoogleTranslator
import random 

logger = logging.getLogger(__name__)

# Define a list of news categories
NEWS_CATEGORIES = [
    'Politics',
    'Business',
    'Technology',
    'Health',
    'Entertainment',
    'Science',
    'Sports',
    'World',
    'Environment',
    'Education'
]

def scrape_data_from_url(url):
    try:
        article = newspaper.Article(url)
        article.download()
        article.parse()

        title = article.title
        text = article.meta_description
        translated_text = GoogleTranslator(source='auto', target='en').translate(text)
        top_image = article.top_image
        category = random.choice(NEWS_CATEGORIES)

        logger.info(f"Scraped data from URL: {url}")

        return {
            'url': url,
            'title': title,
            'text': text,
            'translated_text': translated_text,
            'category': category,
            'main_image': top_image
        }

    except Exception as e:
        logger.error(f"Could not scrape data due to error: {str(e)}")
        return {
            'url': url,
            'title': None,
            'text': None,
            'main_image': None
        }   