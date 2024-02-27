import pandas as pd
import pyarrow as pya
from time import sleep
from stream_to_power_bi import StreamToPowerBI

endpoint = ""

# montagem do dataframe usando pandas e formatação das colunas
df = (pd.read_csv("result.csv", 
                  index_col=None,
                  dtype={'ANO':float,
                         'FILTRO':str,
                         'CONTEUDO':str,
                         'CHAVE':str,
                         'VALOR':str
                         },
                  usecols=['ANO','FILTRO','CONTEUDO','CHAVE','VALOR'])
     ).dropna()

df["VALOR"] = df["VALOR"].str.replace('.','').astype({'VALOR': 'float'})

#montagem das listas com os filtros para enviar os dados
filters = df["FILTRO"].unique().tolist()
contents = df["CONTEUDO"].unique().tolist()
# loop de inserção dos dados
# isso é necessario pois o power bi não permite o uso continuo da url de inserção por muito tempo
# fazemos o uso do loop e de atrasos de 30 segundos entre a troca de filtros para contornar esse problema
for f in filters:
    for c in contents:

        sleep(30)

        filtered_df = df.query('FILTRO == "{}" & CONTEUDO == "{}"'.format(f, c))

        print(filtered_df)

        for record in range(0,len(filtered_df)):
            data = dict(filtered_df.iloc[record])
            # dados enviados linha a linha
            StreamToPowerBI(endpoint,data).wait(1).post_data()

