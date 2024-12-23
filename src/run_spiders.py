import subprocess

class RunSpiders:
    def __init__(self):
        pass
    
    def run_spider_amazon(self):
        print("Iniciando scraping da Amazon...")
        subprocess.run(["scrapy", "crawl", "amazon_spider"])
        
    def run_spider_mercadolivre(self):
        print("Iniciando scraping do Mercado Livre...")
        subprocess.run(["scrapy", "crawl", "mercado_livre_spider"])
        
    def run_spider_magazineluiza(self):
        print("Iniciando scraping da Magazine Luiza...")
        subprocess.run(["scrapy", "crawl", "magazine_luiza_spider"])


if __name__ == "__main__":
    run_spiders = RunSpiders()
    run_spiders.run_spider_amazon()
    run_spiders.run_spider_mercadolivre()
    run_spiders.run_spider_magazineluiza()
