import pandas as pd
import re
import os
import sqlite3


class FormatedDB:
    def __init__(self):
        self.data = None
        self.amazon_data = pd.read_json('../../raw_data/amazon_products.json')
        self.magazine_luiza_data = pd.read_json('../../raw_data/magazine_luiza_products.json')
        self.mercado_livre_data = pd.read_json('../../raw_data/mercadolivre_products.json') 
    
    def process(self):
        self.join_data()
        self.save()
        
    def join_data(self):
        self.data = pd.concat([self.amazon_data, self.magazine_luiza_data, self.mercado_livre_data])
        self.data.reset_index(drop=True, inplace=True)
        
    def save(self):
        output_dir = '../../processed_data'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        con = sqlite3.connect(f'{output_dir}/database.db')
        self.data.to_sql('products', con, if_exists='replace', index=False)
        con.close()
        

if __name__ == "__main__":
    formated_db = FormatedDB()
    formated_db.process()
