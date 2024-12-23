import subprocess

def run_spiders():
    # Rodar o spider da Amazon
    print("Iniciando scraping da Amazon...")
    subprocess.run(["scrapy", "crawl", "amazon_spider"])
    
    # Rodar o spider do Mercado Livre
    # print("Iniciando scraping do Mercado Livre...")
    # subprocess.run(["scrapy", "crawl", "mercadolivre_spider"])

if __name__ == "__main__":
    run_spiders()
