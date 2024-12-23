import scrapy
import json
import os

class MagazineLuizaSpider(scrapy.Spider):
    name = "magazine_luiza_spider"
    allowed_domains = ["magazineluiza.com.br"]
    start_urls = ["https://www.magazineluiza.com.br/busca/smartphone/"]
    page_count = 1
    max_page_count = 10

    SCRAPERAPI_KEY = os.getenv("SCRAPERAPI_KEY")

    custom_settings = {
        'FEEDS': {
            '../raw_data/magazine_luiza_products.json': {
                'format': 'json',
                'encoding': 'utf8',
            }
        }
    }

    def parse(self, response):

        jsonld_script = response.css('script[type="application/ld+json"]::text').get()

        if jsonld_script:
            try:
        
                data = json.loads(jsonld_script)

                for product in data.get('@graph', []):
            
                    product_name = product.get("name")
                    price = product.get("offers", {}).get("price")
                    price_currency = product.get("offers", {}).get("priceCurrency")
                
                    aggregate_rating = product.get("aggregateRating", {})
                    rating_value = aggregate_rating.get("ratingValue")

            
                    price_whole = None
                    if price:
                        price_whole = f"{price_currency} {price}"

            
                    yield {
                        'product_name': product_name,
                        'price_whole': price_whole,
                        'rating_value': rating_value
                    }

            except json.JSONDecodeError:
                self.logger.error('Erro ao decodificar o JSON-LD')

        if self.page_count < self.max_page_count:
            next_page = response.css('a[aria-label^="Go to page"]::attr(href)').get()
            
            if next_page:
                next_page_url = response.urljoin(next_page)
                self.page_count += 1
                yield scrapy.Request(next_page_url, callback=self.parse)
                