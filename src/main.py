import subprocess
import os
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import pytz
import threading
from datetime import datetime, timedelta
from pyngrok import ngrok

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_URL_API = None
PUBLIC_URL_DASHBOARD = None
processes = []

def run_scraping():
    print("Running scraping...")
    subprocess.Popen(["python", "run_spiders.py"], cwd=BASE_DIR).wait()

def run_processing_data():
    print("Running processing data...")
    processamento_dir = os.path.join(BASE_DIR, "processamento")
    subprocess.Popen(["python", "main.py"], cwd=processamento_dir).wait()

def run_insert_data_warehouse():
    print("Running insert data warehouse...")
    warehouse_dir = os.path.join(BASE_DIR, "data_warehouse")
    subprocess.Popen(["python", "insert.py"], cwd=warehouse_dir).wait()

def run_dashboard():
    print("Running dashboard...")
    dashboard_dir = os.path.join(BASE_DIR, "dashboard")
    process = subprocess.Popen(["streamlit", "run", "app.py"], cwd=dashboard_dir)
    processes.append(process)

def run_api():
    print("Running API...")
    api_dir = os.path.join(BASE_DIR, "api")
    process = subprocess.Popen(["fastapi", "run", "app.py"], cwd=api_dir)
    processes.append(process)

def start_ngrok():
    global PUBLIC_URL_API, PUBLIC_URL_DASHBOARD
    PUBLIC_URL_API = ngrok.connect(8000)
    PUBLIC_URL_DASHBOARD = ngrok.connect(8501)
    print("Public URL API: ", PUBLIC_URL_API)
    print("Public URL Dashboard: ", PUBLIC_URL_DASHBOARD)

def run_job():
    print("Running pipeline...")
    
    run_scraping()
    run_processing_data()
    run_insert_data_warehouse()
    
    start_ngrok()
    
    # Iniciar o dashboard e a API em threads separadas
    dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
    api_fastapi_thread = threading.Thread(target=run_api, daemon=True)
    
    api_fastapi_thread.start()
    dashboard_thread.start()
    
    print("Dashboard running in url: ", PUBLIC_URL_DASHBOARD)
    print("API running in url: ", PUBLIC_URL_API) 
    
    dashboard_thread.join()
    api_fastapi_thread.join()
    
    print("Pipeline finished.")

if __name__ == "__main__":    
    scheduler = BlockingScheduler()
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    
    run_job()
        
    scheduler.add_job(
        run_job,
        'cron',
        day='*/10',
        hour=2,
        minute=0,
        second=0,
        timezone=brasilia_tz
    )
    
    print("Starting scheduler to run pipeline...")
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        print("Stopping scheduler...")
        scheduler.shutdown()