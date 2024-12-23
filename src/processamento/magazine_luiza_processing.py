import pandas as pd
import re
import os
import sqlite3

class MagazineLuizaProcessing:
    def __init__(self):
        self.data = pd.read_json('../../raw_data/magazine_luiza_products.json')
        
    def process(self):
        self.extract_specifications()
        self.fill_missing_values()
        self.drop_columns()
        self.order_columns()
        self.save()
    
    def order_columns(self):
        self.data = self.data[['model', 'storage', 'ram', 'is_5g', 'price_whole', 'rating_value']]
    
    def extract_specifications(self):
        
        def extract_ram(text):
            match = re.search(r'(\d+)\s?gb\s?ram|ram\s?boost\s?(\d+)\s?gb', text, re.IGNORECASE)
            return int(match.group(1) or match.group(2)) if match else None

        def extract_storage(text):
            match = re.search(r'(\d+)\s?gb(?!\s?ram|ram\s?boost)', text, re.IGNORECASE)  # Exclui casos de RAM
            return int(match.group(1)) if match else None

        def extract_model(text):
            match = re.search(
                r'(Moto\s?[A-Z]?\d+|Galaxy\s?[A-Z]?\d+|LG\s?K\d+|iPhone\s?(?:\d+|SE|Mini|Pro|Max|Plus)|Realme\s?[A-Za-z0-9]+|Xiaomi\s?[A-Za-z0-9]+|Poco\s?[A-Za-z0-9]+|Infinix\s?[A-Za-z0-9]+)',
                text,
                re.IGNORECASE
            )
            return match.group(0) if match else None
    
        self.data['ram'] = self.data['product_name'].apply(extract_ram)
        self.data['storage'] = self.data['product_name'].apply(extract_storage)
        self.data['model'] = self.data['product_name'].apply(extract_model)
        self.data['is_5g'] = self.data['product_name'].str.contains('5g', case=False)
        
    def fill_missing_values(self):
        self.data['ram'] = self.data['ram'].fillna(8)
        self.data['storage'] = self.data['storage'].fillna(128)
        self.data['model'] = self.data['model'].fillna("Não identificado")
        
    def drop_columns(self):
        self.data.drop(columns=['product_name'], inplace=True)
    
    def save(self):
        output_dir = '../../processed_data'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        con = sqlite3.connect(f'{output_dir}/magazine_luiza.db')
        self.data.to_sql('products', con, if_exists='replace', index=False)
        con.close()
    
if __name__ == "__main__":
    magazine_luiza_processing = MagazineLuizaProcessing()
    magazine_luiza_processing.process()

            