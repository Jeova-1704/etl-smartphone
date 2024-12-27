from fastapi import FastAPI, HTTPException
from supabase import create_client
from dotenv import load_dotenv
import os

class DataBaseSmartphone:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_KEY')
        self.client = create_client(self.url, self.key)
        
    def get_all(self):
        response = self.client.from_('products').select('*').execute()
        return response.data
    
    def get_product_model(self, model):
        response = self.client.from_('products').select('*').ilike('model', model).execute()
        return response.data
    
    def get_product_storage(self, storage):
        response = self.client.from_('products').select('*').eq('storage', storage).execute()
        return response.data
    
    def get_product_ram(self, ram):
        response = self.client.from_('products').select('*').eq('ram', ram).execute()
        return response.data
    
    def get_product_between_price(self, min_price, max_price):
        response = self.client.from_('products').select('*').gte('price_whole', min_price).lte('price_whole', max_price).execute()
        return response.data
    
    def get_product_is_5g(self):
        response = self.client.from_('products').select('*').eq('is_5g', 1).execute()
        return response.data
    
    def get_product_origin(self, origin):
        response = self.client.from_('products').select('*').ilike('origin', origin).execute()
        return response.data
    
    def get_product_complete_especific(self, storage, ram):
        response = self.client.from_('products').select('*').eq('storage', storage).eq('ram', ram).execute()
        return response.data
    
    


app = FastAPI()


@app.get("/products")
def read_all_products() -> dict:
    response = None
    try:
        db = DataBaseSmartphone()
        response = db.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"products": response}


@app.get("/products/model/{model}")
def read_product(model: str) -> dict:
    response = None
    try:
        db = DataBaseSmartphone()
        response = db.get_product_model(model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"product": response}
        
        
@app.get("/products/storage/{storage}")
def read_product(storage: int) -> dict:
    response = None
    try:
        db = DataBaseSmartphone()
        response = db.get_product_storage(storage)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"product": response}
    

@app.get("/products/ram/{ram}")
def read_product(ram: int) -> dict:
    response = None
    try:
        db = DataBaseSmartphone()
        response = db.get_product_ram(ram)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"product": response}

@app.get("/products/price/{min_price}/{max_price}")
def read_product(min_price: int, max_price: int) -> dict:
    response = None
    try:
        db = DataBaseSmartphone()
        response = db.get_product_between_price(min_price, max_price)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"product": response}

@app.get("/products/5g")
def read_product() -> dict:
    response = None
    try:
        db = DataBaseSmartphone()
        response = db.get_product_is_5g()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"product": response}

@app.get("/products/origin/{origin}")
def read_product(origin: str) -> dict:
    response = None
    try:
        db = DataBaseSmartphone()
        response = db.get_product_origin(origin)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"product": response}

@app.get("/products/{storage}/{ram}")
def read_product(storage: int, ram: int) -> dict:
    response = None
    try:
        db = DataBaseSmartphone()
        response = db.get_product_complete_especific(storage, ram)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"product": response}


