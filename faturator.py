import pandas as pd
import streamlit as st
import plotly as pl
import numpy as np



#importa o arquivo CSV
dados = None
inserir_arquivo = st.file_uploader('Insira o arquivo CSV')
if inserir_arquivo is not None:
    st.title('Faturator')
    dados = pd.read_csv(inserir_arquivo, delimiter=',')



valores = [ 

]


parametros = [
    100000, 500000, 1000000
]

# static maps = preco1 : 13.20, preco2 : 10.56, preco3: 7.92
# dynamic maps = preco1 : 46.20, preco2 : 36.96, preco3: 27.72
# directions = preco1: 33.00, preco2 : 26.40, preco3: 19.80
# Direction advanced = preco1: 66.00, preco2: 52.80, preco3: 39.60
# geocoding = preco1: 33.00, preco2: 26.40, preco3: 19.80





colunas_requisitadas = dados[['Descrição da SKU', 'Quantidade de uso', 'Custo não arredondado (R$)']]
colunas_requisitadas = colunas_requisitadas.drop(index=11)


st.text('TABELA INICIAL')
st.write(colunas_requisitadas)

if inserir_arquivo is not None:


  # CORREÇÃO DE PONTUAÇÃO, CRIAÇÃO COLUNA DESCONTO E REMOÇÃO DE COLUNA CUSTO NÃO ARREDONDADO
    colunas_requisitadas[['Quantidade de uso', 'Custo não arredondado (R$)']] = (
        colunas_requisitadas[['Quantidade de uso', 'Custo não arredondado (R$)']].apply(lambda col: col.astype(str)))


    colunas_requisitadas['Custo não arredondado (R$)'] = (
        colunas_requisitadas['Custo não arredondado (R$)'].str.replace(',','.', regex = True))
    
    colunas_requisitadas['Quantidade de uso'] = (
        colunas_requisitadas['Quantidade de uso'].str.replace('.','',regex=False).replace('nan','0',regex=True)
    )


    colunas_requisitadas['Custo não arredondado (R$)'] = colunas_requisitadas['Custo não arredondado (R$)'].str.replace('\xa0','',regex=False)

    colunas_requisitadas['Custo não arredondado (R$)'] = colunas_requisitadas['Custo não arredondado (R$)'].astype(float)

    
    colunas_requisitadas['Desconto'] = colunas_requisitadas['Custo não arredondado (R$)'].where(colunas_requisitadas['Custo não arredondado (R$)'] <  0, other=0)
   

    colunas_requisitadas['Desconto']=colunas_requisitadas['Desconto'].astype(str).str.replace(',','', regex= False).astype(float)


    colunas_requisitadas['Quantidade de uso'] = (
        colunas_requisitadas['Quantidade de uso'].str.replace(',','',regex=False)).astype(int)
 











    colunas_requisitadas=colunas_requisitadas.drop(columns='Custo não arredondado (R$)')
    st.text('TABELA ATUALIZADA')
    st.write(colunas_requisitadas)



else:
    'Adicione um arquivo CSV'


# colunas_requisitadas['Descontos'] = colunas_requisitadas['Custo não arredondado (R$)'].astype(float)


# st.write(colunas_requisitadas)

# desconto = colunas_requisitadas[colunas_requisitadas['Custo não arredondado (R$)'] < 0]

