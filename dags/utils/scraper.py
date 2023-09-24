import newspaper
import logging

logger = logging.getLogger(__name__)

def scrape_data_from_url(url):
    try:
        article = newspaper.Article(url)
        article.download()
        article.parse()
        logger.info(f"Scraped data from URL: {url}")
        return {
            'url': url,
            'title': article.title,
            'text': article.meta_description,
            'main_image': article.top_image
        }
    
    except Exception as e:
        logger.error(f"Could not scrape data due to error: {str(e)}")
        return {
            'url': url,
            'title': None,
            'text': None,
            'main_image': None
        }   