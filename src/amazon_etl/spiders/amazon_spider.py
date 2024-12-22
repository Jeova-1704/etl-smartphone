import scrapy
import os

class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ['www.amazon.com.br', 'api.scraperapi.com']
    start_urls = ["https://www.amazon.com.br/s?k=smartphone"]
    SCRAPERAPI_KEY = os.getenv("SCRAPERAPI_KEY")

    def start_requests(self):
        headers = {"User-Agent": os.getenv("USER_AGENT")}
        for url in self.start_urls:
            scraperapi_url = f"http://api.scraperapi.com/?api_key={self.SCRAPERAPI_KEY}&url={url}"
            yield scrapy.Request(scraperapi_url, headers=headers)

    def parse(self, response):
        pass
    
    
