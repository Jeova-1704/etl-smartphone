import subprocess

class RunProcess:
    def __init__(self):
        pass
    
    def run_process_mercadolivre(self):
        print("Iniciando processamento dos dados do Mercado Livre...")
        subprocess.run(["python", "mercado_livre_processing.py"])
        print("Processamento dos dados finalizado")
        
    def run_process_magazine_luiza(self):
        print("Iniciando processamento dos dados da magazine luiza...")
        subprocess.run(["python", "magazine_luiza_processing.py"])
        print("Processamento dos dados finalizado")
        
    def run_process_amazon(self):
        print("Iniciando processamento dos dados da amazon...")
        subprocess.run(["python", "amazon_processing.py"])
        print("Processamento dos dados finalizado")

if __name__ == "__main__":
    run_process = RunProcess()
    run_process.run_process_mercadolivre()
    run_process.run_process_magazine_luiza()
    run_process.run_process_amazon()