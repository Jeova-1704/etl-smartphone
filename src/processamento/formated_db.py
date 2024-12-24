import pandas as pd
import re
import os
import sqlite3


class FormatedDB:
    def __init__(self):
        self.data = None
        self.amazon_data = pd.read_sql('SELECT * FROM products', sqlite3.connect("../../processed_data/amazon.db"))
        self.magazine_luiza_data = pd.read_sql('SELECT * FROM products', sqlite3.connect("../../processed_data/magazine_luiza.db"))
        self.mercado_livre_data = pd.read_sql('SELECT * FROM products', sqlite3.connect("../../processed_data/mercado_livre.db"))
    
    def process(self):
        self.join_data()
        self.handle_price_zero()
        self.fix_storage_errors()
        self.handle_storage_zero()
        self.fix_rating()
        self.save()
        
    def join_data(self):
        self.data = pd.concat([self.amazon_data, self.magazine_luiza_data, self.mercado_livre_data])
        self.data.reset_index(drop=True, inplace=True)
        
    def fix_rating(self):
        self.data['rating_value'] = self.data['rating_value'].replace(',', '.', regex=True)
        self.data['rating_value'] = self.data['rating_value'].astype(float)
        
    def handle_price_zero(self):
        products_with_zero_price = self.data[self.data['price_whole'] == 0]
        
        for index, row in products_with_zero_price.iterrows():
            model = row['model']
            
            other_products = self.data[(self.data['model'] == model) & (self.data['price_whole'] != 0)]
            
            if not other_products.empty:
                average_price = other_products['price_whole'].mean()
                self.data.at[index, 'price_whole'] = average_price
            else:
                self.data.drop(index, inplace=True)
                
    def handle_storage_zero(self):
        mask = self.data['storage'] == 0
        
        for index, row in self.data[mask].iterrows():   
            model = row['model']
            
            other_products = self.data[(self.data['model'] == model) & (self.data['storage'] != 0)]
            
            if not other_products.empty:
                average_storage = other_products['storage'].mean()
                self.data.at[index, 'storage'] = average_storage
            else:
                self.data.drop(index, inplace=True)
        

    def fix_storage_errors(self):
        mask = self.data['storage'] <= 12
        self.data.loc[mask, 'ram'] = self.data.loc[mask, 'storage']
        self.data.loc[mask, 'storage'] = 0
                
    def save(self):
        output_dir = '../../processed_data'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        con = sqlite3.connect(f'{output_dir}/database.db')
        self.data.to_sql('products', con, if_exists='replace', index=False)
        con.close()
        self.data.to_json(f'{output_dir}/database.json', orient='records', lines=True)
        

if __name__ == "__main__":
    formated_db = FormatedDB()
    formated_db.process()
