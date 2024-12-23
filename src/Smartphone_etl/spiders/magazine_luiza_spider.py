import scrapy


class MagazineLuizaSpiderSpider(scrapy.Spider):
    name = "magazine_luiza_spider"
    allowed_domains = ["www.magazineluiza.com.br"]
    start_urls = ["https://www.magazineluiza.com.br/busca/smartphone/"]

    def parse(self, response):
        pass
