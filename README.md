# Projeto de Engenharia de Dados - Pipeline de Coleta e Processamento
Este projeto é um pipeline de engenharia de dados desenvolvido para coletar, processar e analisar dados de smartphones disponíveis em e-commerces como Amazon, Mercado Livre, e Magazine Luiza. O pipeline inclui uma etapa de coleta de dados usando Scrapy, processamento e armazenamento em um banco de dados, e visualização interativa com Streamlit.

## Índice
1. [Visão Geral](#visão-geral)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Funcionamento do Scrapy e Coleta de Dados](#funcionamento-do-scrapy-e-coleta-de-dados)
4. [Configuração do Ambiente](#configuração-do-ambiente)
5. [Execução do Pipeline](#execução-do-pipeline-e-visualização-interativa)
7. [Considerações Finais](#considerações-finais)


## Visão Geral
O objetivo deste projeto é criar uma solução escalável para coletar dados de preços, avaliações e especificações técnicas de smartphones, processá-los para insights e fornecer uma interface interativa para análise. Os principais componentes são:

- Coleta de dados: Utilizando Scrapy para realizar scraping de sites como Amazon, Mercado Livre e Magazine Luiza.
- Processamento de dados: Transformação dos dados brutos em um formato estruturado e limpo.
- Armazenamento: Banco de dados SQLite para armazenar tanto os dados brutos quanto os processados.
- Visualização: Dashboard interativo em Streamlit.

## Estrutura do Projeto
A estrutura do projeto foi organizada em diretórios para separar responsabilidades. Veja abaixo a hierarquia principal:
```bash 
├── .venv/                    
├── processed_data/           
│   ├── amazon.db          
│   ├── database.db
│   ├── magazine_luiza.db
│   ├── mercado_livre.db
├── raw_data/
│   ├── amazon_products.json
│   ├── magazine_luiza_products.json
│   ├── mercadolivre_products.json
├── src/
│   ├── dashboard/
│   │   ├── app.py
│   ├── processamento/
│   │   ├── amazon_processing.py
│   │   ├── formated_db.py
│   │   ├── magazine_luiza_processing.py
│   │   ├── main.py
│   │   ├── mercado_livre_processing.py
│   ├── Smartphones_etl/
│   │   ├── spiders/
│   │   │   ├── __init__.py
│   │   │   ├── amazon_spider.py
│   │   │   ├── magazine_luiza_spider.py
│   │   │   ├── mercado_livre_spider.py
│   │   ├── __init__.py
│   │   ├── items.py
│   │   ├── middlewares.py
│   │   ├── settings.py
│   ├── run_spiders.py
│   ├── scrapy.cfg
├── .env
├── .env.example
├── .gitignore
├── README.md
├── requirements-dev.txt
├── requirements.in
├── requirements.txt
```
### Componentes principais:
- scraper/: Contém spiders para coletar dados de diferentes fontes de e-commerce.
- processamento/: Responsável pela transformação e limpeza dos dados brutos.
- dashboard/: Aplicação para análise interativa dos dados processados.

## Funcionamento do Scrapy e Coleta de Dados
### O que é Scrapy?
Scrapy é um framework de scraping em Python, amplamente utilizado para extrair dados de websites. Ele permite:

- Definir regras para navegar em páginas web.
- Selecionar os dados desejados com seletores CSS ou XPath.
- Exportar os dados em diversos formatos, como JSON, CSV, ou armazená-los diretamente em um banco de dados.

### Coleta de dados neste projeto 
1. Amazon Spider:
    - Navega pela seção de smartphones da Amazon.
    - Coleta informações como modelo, preço, avaliações, armazenamento e RAM.
    - Utiliza a API do ScraperAPI para evitar bloqueios e superar CAPTCHAs.

Mercado Livre Spider:
    - Extrai informações diretamente das páginas de produtos e resultados de busca.
    - Os dados coletados incluem modelo, preço, e se o smartphone suporta 5G.

Magazine Luiza Spider:
    - Acessa a categoria de smartphones no site.
    - Coleta dados semelhantes aos outros spiders.

### Execução dos Spiders
Todos os spiders podem ser executados individualmente ou em conjunto através do script principal:

```bash
cd src
python run_spiders.py
```
Os dados brutos são armazenados localmente em um banco de dados SQLite ou na pasta raw_data/ (caso prefira usar armazenamento de arquivos).


## Configuração do Ambiente

1. Clone o repositório:
```bash
git clone https://github.com/Jeova-1704/etl-smartphone.git
cd etl-smartphone
```
2. Crie um ambiente virtual e instale as dependências:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -r requirements.txt
```
3. Configure as variáveis de ambiente:
No diretório raiz do projeto, renomeie o arquivo .env.example para .env e preencha as variáveis de acordo com suas credenciais do ScraperAPI e do seu user-agent respectivo.
```bash
USER_AGENT="adicione o user-agent do google aqui"
SCRAPERAPI_KEY="adicione a chave do scraperapi aqui"
```
- Para obter o seu user agent, basta pesquisar no google "my user agent" e copiar o valor que aparecer completo e adicionar no arquivo .env.
- Para obter a chave do ScraperAPI, acesse o site https://www.scraperapi.com/ e crie uma conta gratuita. Após a criação da conta, você copia a chave e adiciona no arquivo .env.

## Execução do Pipeline e Visualização Interativa

1. Coleta de dados:
```bash
cd src
python run_spiders.py
```
2. Processamento dos dados:
```bash
cd src/processamento
python main.py
```
3. Visualização interativa:
```bash
cd src/dashboard
streamlit run app.py
```

### Detalhes da execução:
#### 1. Coleta de dados:
    - Quando executado o script run_spiders.py, os spiders de Amazon, Mercado Livre e Magazine Luiza são acionados para coletar dados de smartphones automaticamente.
    - Os dados brutos são armazenados em arquivos JSON na pasta raw_data/
    - Caso ocorra algum erro durante a execução, verifique as mensagens de log no terminal, possa ser que algum elemento da página tenha sido alterado ou o site esteja bloqueando o acesso.

#### 2. Processamento dos dados:
    - Quando executado o script main.py, ele gerencia o processamento de cada um respectivo arquivo JSON e armazena os dados processados em um banco de dados SQLite na pasta processed_data/.
    - O banco de dados é criado automaticamente e contém tabelas para cada fonte de dados (Amazon, Mercado Livre, Magazine Luiza).
    - Os dados são procesados e limpos para facilitar a análise e visualização.
    - Os valores são tratados para remover caracteres especiais, converter preços para float, e extrair informações adicionais.
    - O meu formated_db.py é responsável unir os dados processados em um único banco de dados e fazer a ultima limpeza dos dados.
    - Todo o processor é gerenciado pelo main.py.

#### 3. Visualização interativa:
    - O dashboard é uma aplicação Streamlit que permite visualizar os dados processados de forma interativa.
    - Ele exibe gráficos de preços, avaliações, e especificações técnicas de smartphones.
    - A interface é simples e intuitiva, permitindo filtrar e ordenar os dados conforme necessário.

## Considerações Finais

#### Limitações 
- O projeto foi desenvolvido para fins educacionais e pode não ser adequado para uso em produção.
- O scraping de sites é uma prática legalmente questionável e pode violar os termos de serviço de alguns sites.
- O limite de requisições do ScraperAPI é de 5000 créditos mensais para a conta gratuita, o que pode limitar a quantidade de dados que podem ser coletados.

#### Futuras implementações 
- Adicionar mais fontes de dados e spiders para coletar informações de outros sites.
- Melhorar o processamento dos dados para extrair mais informações e insights.
- Implementar um pipeline de dados mais robusto e escalável, utilizando ferramentas da nuvem como AWS ou GCP.

### AWS  
Para um projeto mais robusto e escalável, você pode utilizar os serviços da AWS para hospedar o pipeline de coleta e processamento de dados. 

#### Etapas do pipeline na AWS:
1. Armazenamento de Dados Brutos (Data Lake)
Serviço: Amazon S3
O Amazon S3 pode ser usado como um data lake, que armazena os dados brutos coletados pelos spiders em um formato estruturado ou semiestruturado, como JSON, CSV ou Parquet.

- Quando os spiders coletam os dados, eles podem ser enviados diretamente para um bucket do S3.
- O S3 permite armazenar grandes volumes de dados a baixo custo e é altamente escalável.
- O S3 pode armazenar grandes volumes de dados a baixo custo e é altamente escalável.
- Os dados brutos ficam disponíveis e visiveis para serem processados por outras ferramentas e serviços da AWS.

2. Processamento de Dados brutos (ETL)
O processamento dos dados brutos pode ser automatizado utilizando o AWS Glue (um serviço de ETL gerenciado) ou funções serverless com o AWS Lambda.
- Com AWS Glue:
    - Crie um job ETL para ler os dados do bucket S3 e transformá-los (limpeza, agregação, deduplicação).
    - Os dados tratados podem ser exportados diretamente para outro bucket ou para um Data Warehouse.
- Com AWS Lambda:
    - Configure uma função Lambda acionada sempre que um novo arquivo é enviado ao bucket S3.
    - A função processa os dados em tempo real e grava o resultado em outro bucket ou banco.


3. Armazenamento de Dados Processados (Data Warehouse)
Serviço: Amazon Redshift
O Amazon Redshift é um banco de dados de data warehouse totalmente gerenciado, otimizado para análise de dados em grande escala.
- Como funciona:
    - Os dados tratados são carregados para o Redshift usando ferramentas como AWS Glue, COPY SQL ou Redshift Data API.
    - A estrutura do banco pode ser modelada em um esquema Star ou Snowflake, dependendo das necessidades analíticas.
    - Por exemplo, você pode ter uma tabela de fatos (dados de smartphones) e tabelas de dimensões (informações das lojas, marcas etc.).

4. Visualização e Análise de Dados
Serviço: Amazon QuickSight
O Amazon QuickSight é uma ferramenta de visualização de dados e business intelligence que permite criar dashboards interativos e relatórios.
- Com o QuickSight:
    - Conecte-se ao Redshift para importar os dados e criar visualizações.
    - Crie gráficos, tabelas e filtros interativos para analisar os dados de smartphones.
    - Compartilhe os dashboards com outras pessoas na organização.

5. Orquestração do Pipeline
Serviço: Apache Airflow 
O Apache Airflow é uma plataforma de orquestração de fluxo de trabalho que permite agendar, monitorar e executar tarefas de ETL e análise de dados.
- Com o Airflow:
    - Defina os fluxos de trabalho como DAGs (Directed Acyclic Graphs) para executar as etapas do pipeline em ordem.
    - Agende a exec
    - Configurar gatilhos e dependências entre as tarefas.


