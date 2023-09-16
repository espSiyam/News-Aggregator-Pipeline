import newspaper

def scrape_data_from_url(url):
    article = newspaper.Article(url)
    article.download()
    article.parse()
    return {
        'url': url,
        'title': article.title,
        'text': article.meta_description,
        'main_image': article.top_image
    }