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



valores = {
    'Itens' : ['Static Maps','Dynamic Maps', 'Directions','Directions Advanced', 'Geocoding'],
    'valor1' : [13.20, 46.20, 33.00, 66.00, 33.00],
    'valor2' : [10.56, 36.96, 26.40, 52.80, 26.40 ],
    'valor3' : [7.92, 27.72, 19.80, 39.60, 19.80],
}

valores = pd.DataFrame(valores)

quantidade_uso1 = 100000
quantidade_uso2= 500000
quantidade_uso3 = 1000000




def calcula_valor(quantidade,valor1,valor2,valor3,quantidade_uso1,quantidade_uso2,quantidade_uso3):
    if quantidade <= quantidade_uso1:
        return quantidade * valor1
    elif quantidade <= quantidade_uso2:
        return (quantidade_uso1 * valor1) + (quantidade - quantidade_uso1) * valor2
    else:
        return quantidade_uso1 * valor1 + quantidade_uso2 * valor2 + (quantidade - quantidade_uso1 - quantidade_uso2) * valor3





colunas_requisitadas = dados[['Descrição da SKU', 'Quantidade de uso', 'Custo não arredondado (R$)']]
colunas_requisitadas = colunas_requisitadas.drop(index=11)


st.text('TABELA INICIAL')

if inserir_arquivo is not None:


  # CORREÇÃO DE PONTUAÇÃO, CRIAÇÃO COLUNA DESCONTO E REMOÇÃO DE COLUNA CUSTO NÃO ARREDONDADO
    colunas_requisitadas[['Quantidade de uso', 'Custo não arredondado (R$)']] = (
        colunas_requisitadas[['Quantidade de uso', 'Custo não arredondado (R$)']].apply(lambda col: col.astype(str)))


    colunas_requisitadas['Custo não arredondado (R$)'] = (
        colunas_requisitadas['Custo não arredondado (R$)'].str.replace(',','.', regex = True)
    )
    
    colunas_requisitadas['Quantidade de uso'] = (
        colunas_requisitadas['Quantidade de uso'].str.replace('.','',regex=False).replace('nan','0', regex=True).astype(int)
    )

    colunas_requisitadas['Custo não arredondado (R$)'] = colunas_requisitadas['Custo não arredondado (R$)'].str.replace('\xa0','',regex=False)

    colunas_requisitadas['Custo não arredondado (R$)'] = colunas_requisitadas['Custo não arredondado (R$)'].astype(float)

    colunas_requisitadas['Desconto'] = (
        colunas_requisitadas['Custo não arredondado (R$)'].where(colunas_requisitadas['Custo não arredondado (R$)'] <  0, other=0)
    )
    colunas_requisitadas['Desconto']=colunas_requisitadas['Desconto'].astype(str).str.replace(',','', regex= False).astype(float)

    colunas_requisitadas=colunas_requisitadas.drop(columns='Custo não arredondado (R$)', index=6)

    st.write(colunas_requisitadas)

    colunas_requisitadas['valor calculado'] = colunas_requisitadas.apply(lambda row: calcula_valor(
    row['Quantidade de uso'],
    valores.loc[valores['Itens'] == row['Descrição da SKU'], 'valor1'].values,
    valores.loc[valores['Itens'] == row['Descrição da SKU'], 'valor2'].values,
    valores.loc[valores['Itens'] == row['Descrição da SKU'], 'valor3'].values,
    quantidade_uso1,quantidade_uso2,quantidade_uso3), axis=1)
    
    colunas_requisitadas['valor calculado'] = colunas_requisitadas['valor calculado']
    
    

    st.text('TABELA ATUALIZADA')
    st.write(colunas_requisitadas)
    

else:
    'Adicione um arquivo CSV'


