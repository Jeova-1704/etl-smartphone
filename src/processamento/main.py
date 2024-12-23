import subprocess

class RunProcess:
    def __init__(self):
        pass
    
    def run_process_mercadolivre(self):
        print("Iniciando processamento dos dados do Mercado Livre...")
        subprocess.run(["python", "mercado_livre_processing.py"])
        
if __name__ == "__main__":
    run_process = RunProcess()
    run_process.run_process_mercadolivre()