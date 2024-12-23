import scrapy
import os


class MercadoLivreSpiderSpider(scrapy.Spider):
    name = "mercado_livre_spider"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/smartphone"]
    SCRAPERAPI_KEY = os.getenv("SCRAPERAPI_KEY")
    page_count = 1
    max_page_count = 10
    
    custom_settings = {
        'FEEDS': {
            '../data/mercadolivre_products.json': {
                'format': 'json',
                'encoding': 'utf8',
            }
        }
    }

    def parse(self, response):
        pass
