import pandas as pd
import pyarrow as pya
from time import sleep
from stream_to_power_bi import StreamToPowerBI

endpoint = "https://api.powerbi.com/beta/1c39c071-04ee-484a-9b5d-7f3bf3dfb998/datasets/f9f1f0aa-e120-4065-9c53-d5de9487be39/rows?experience=power-bi&key=%2BbAvXgH1UHpIjE4RkbZ847%2F80O0aNyKGioZFs08SivH%2F97GTUPsnzc3PAtTK0zDbanuRZGLufCVwF3piWU%2FsUw%3D%3D"

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

