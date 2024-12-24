import streamlit as st
import pandas as pd
import sqlite3


class Dashboard:
    def __init__(self):
        self.data = pd.read_sql_query("SELECT * FROM products", sqlite3.connect("../../processed_data/database.db"))
        
    def analise_all(self):
        st.subheader("Analise de todos os smartphones")
        col1, col2, col3 = st.columns(3)
        col1.metric("Quantidade de produtos", self.data.shape[0])
        col2.metric("Quantidade de lojas", len(self.data["origin"].unique()))
        col3.metric("Quantidade de produtos unicos", len(self.data["model"].unique()))
    
    def analise_avg(self):
        st.subheader("Analise de dados dos smartphones")
        total_smartphones = self.data.shape[0]
        mode_storage = self.data["storage"].mode()[0]
        mode_ram = self.data["ram"].mode()[0]
        tota_is_5g = self.data["is_5g"].sum()
        percentagem_is_5g = f"{(tota_is_5g/total_smartphones)*100:.2f}%"
        avg_price = self.data["price_whole"].mean()
        avg_rating = self.data["rating_value"].mean()
        quantity_origin_amazon = len(self.data[self.data["origin"] == "Amazon"])
        quantity_origin_magalu = len(self.data[self.data["origin"] == "Magazine Luiza"])
        quantity_origin_mercadolivre = len(self.data[self.data["origin"] == "Mercado Livre"])
        percentagem_origin_amazon = f"{(quantity_origin_amazon/total_smartphones)*100:.2f}%"
        percentagem_origin_magalu = f"{(quantity_origin_magalu/total_smartphones)*100:.2f}%"
        percentagem_origin_mercadolivre = f"{(quantity_origin_mercadolivre/total_smartphones)*100:.2f}%"
        avg_price_unique_model = self.data.groupby("model")["price_whole"].mean().mean()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Armagazenamento mais comum", mode_storage)
        col2.metric("RAM mais comum", mode_ram)
        col3.metric(
            label=f"Quantidade de smartphones 5G",
            value=f"{percentagem_is_5g}",
            delta=f"{tota_is_5g} smartphones",
        )        
        col1, col2, col3 = st.columns(3)
        col1.metric("Media de preço de todos os produtos", round(avg_price, 2))
        col2.metric("Media de avaliação de todos os produtos", round(avg_rating, 2))
        col3.metric("Media de preço dos modelos unicos", round(avg_price_unique_model, 2))
        
        col1, col2, col3 = st.columns(3)
        col1.metric(
            label="Quantidade de produtos na Amazon",
            value=f"{percentagem_origin_amazon}",
            delta=f"{quantity_origin_amazon} produtos",
        )
        col2.metric(
            label="Quantidade de produtos na Magazine Luiza",
            value=f"{percentagem_origin_magalu}",
            delta=f"{quantity_origin_magalu} produtos",
        )
        col3.metric(
            label="Quantidade de produtos no Mercado Livre",
            value=f"{percentagem_origin_mercadolivre}",
            delta=f"{quantity_origin_mercadolivre} produtos",
        )
        
    def analise_by_smartphone(self):
        st.subheader("Analise de cada smartphone")
        model = st.selectbox("Escolha um modelo de smartphone", self.data["model"].unique())
        data = self.data[self.data["model"] == model]
        
        col1, col2 = st.columns(2)        
        avg_price = data["price_whole"].mean()
        col1.metric(
            label=f"Media de preço do modelo {model}",
            value=f"R$ {avg_price:.2f}",
        )
        quantity = data.shape[0]
        col2.metric(
            label=f"Quantidade de produtos do modelo {model}",
            value=quantity,
        )
        
        # media de preço por loja
        col1, col2, col3 = st.columns(3)
        avg_price_amazon = data[data["origin"] == "Amazon"]["price_whole"].mean() if data[data["origin"] == "Amazon"].shape[0] > 0 else 0
        avg_price_magalu = data[data["origin"] == "Magazine Luiza"]["price_whole"].mean() if data[data["origin"] == "Magazine Luiza"].shape[0] > 0 else 0
        avg_price_mercadolivre = data[data["origin"] == "Mercado Livre"]["price_whole"].mean() if data[data["origin"] == "Mercado Livre"].shape[0] > 0 else 0
        col1.metric(
            label="Media de preço na Amazon",
            value=f"R$ {avg_price_amazon:.2f}",
        )
        col2.metric(
            label="Media de preço na Magazine Luiza",
            value=f"R$ {avg_price_magalu:.2f}",
        )
        col3.metric(
            label="Media de preço no Mercado Livre",
            value=f"R$ {avg_price_mercadolivre:.2f}",
        )
        st.subheader("Tabela com dados do modelo selecionado ", model)
        st.write(data)
        
    def run(self):
        st.image("https://www.databricks.com/sites/default/files/inline-images/etl-process-image.png", caption="Imagem temporaria, enquando não é feito o processo do meu sistema", use_container_width=True)
        st.title("Dashboard smartphones")
        st.subheader("Dashboard do resultado do etl de smartphones nas principais lojas online como Amazon, magazine luiza e mercado livre")
        self.analise_all()
        self.analise_avg()
        self.analise_by_smartphone()
        
        
if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.run()
    