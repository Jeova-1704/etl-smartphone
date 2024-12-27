import pandas as pd 
import sqlite3
import os
from dotenv import load_dotenv
from supabase import create_client, Client

class DataBase:
    def __init__(self):
        load_dotenv()
        self.data = pd.read_sql_query("SELECT * FROM products", sqlite3.connect('../../processed_data/database.db'))
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_KEY')
        self.client = create_client(self.url, self.key)
        
    def insertData(self):
        self.client.table('products').delete().neq('id', 0).execute()
        print('Dados deletados e ambiente limpo e preparado para inserção de novos dados')
        self.client.table('products').insert(self.data.to_dict(orient='records')).execute()
        print('Dados inseridos com sucesso')
        
        

if __name__ == '__main__':
    db = DataBase()
    db.insertData()
        
