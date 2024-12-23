import scrapy
import os

class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ['www.amazon.com.br', 'api.scraperapi.com']
    start_urls = ["https://www.amazon.com.br/s?k=smartphone"]
    SCRAPERAPI_KEY = os.getenv("SCRAPERAPI_KEY")
    page_count = 1
    max_page_count = 10
    
    custom_settings = {
        'FEEDS': {
            '../raw_data/amazon_products.json': {
                'format': 'json',
                'encoding': 'utf8',
            },
        },
    }

    def start_requests(self):
        headers = {"User-Agent": os.getenv("USER_AGENT")}
        for url in self.start_urls:
            scraperapi_url = f"http://api.scraperapi.com/?api_key={self.SCRAPERAPI_KEY}&url={url}"
            yield scrapy.Request(scraperapi_url, headers=headers)

    def parse(self, response):
        product_cards_list = response.css('div.puis-card-container')

        for product in product_cards_list:
            product_name = product.css("h2.a-size-base-plus span::text").get()
            price_whole = product.css('span.a-price-whole::text').get()
            price_fraction = product.css('span.a-price-fraction::text').get()
            rating_value = product.css('span.a-icon-alt::text').get()
            
            # Formatar o preço
            if price_whole and price_fraction:
                price = f"R$ {price_whole},{price_fraction}"
            else:
                price = None

            if rating_value:
                rating_value = rating_value.split(" ")[0]
                
                
            yield {
                "product_name": product_name,
                "price_whole": price,
                "rating_value": rating_value
            }

        next_page = response.css('a::attr(href)').re('.*page=\\d+')
        print(next_page)

        if next_page:
            next_page_url = f"https://www.amazon.com.br{next_page[0]}"
            
            next_page_scraperapi_url = f"http://api.scraperapi.com/?api_key={self.SCRAPERAPI_KEY}&url={next_page_url}"
            print(f"Próxima página: {next_page_scraperapi_url}")
            
            yield scrapy.Request(url=next_page_scraperapi_url, callback=self.parse)
