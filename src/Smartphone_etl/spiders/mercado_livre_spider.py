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
            '../raw_data/mercadolivre_products.json': {
                'format': 'json',
                'encoding': 'utf8',
            }
        }
    }

    def parse(self, response):
        products = response.css('div.poly-card__content')
        
        for product in products:
            product_name = product.css('h2.poly-box.poly-component__title a::text').get()
            prices = product.css('span.andes-money-amount__fraction::text').getall()
            cents = product.css('span.andes-money-amount__cents::text').getall()
            rating_value = product.css('span.poly-reviews__rating::text').get()
            
            price_whole = None
            if prices and cents:
                price_whole = f"R$ {prices[0]},{cents[0]}"
            
                
            yield {
                'product_name': product_name,
                'price_whole': price_whole,
                'rating_value': rating_value
            }
        
        if self.page_count < self.max_page_count:
            next_page = response.css('li.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                print("Next page URL:", next_page)
                yield scrapy.Request(url=next_page, callback=self.parse)
