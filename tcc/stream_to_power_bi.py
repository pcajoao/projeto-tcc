from time import sleep
import requests
from typing import Dict
from dataclasses import dataclass

@dataclass

class StreamToPowerBI:
    
    """

    Classe para transmitir dados para o modelo semantico de streaming do Power BI
    --------------------------------------------------
    Exemplo:

     - endpoint :  ednpoint da API, ex. "https://api.powerbi.com/beta/<ws_id>/datasets/<dataset_id>/rows?key=<___key___>"
     - data     :  formato da linha de dados seguindo o dicionario ex. {"id":1, "Value":2.33, "Color":"Red"} 
                   Numero de colunas, nome das colunas e os tipos das colunas devem corresponder ao previamente configurado no Power BI
     - delay    :  Atraso em segundos ao mandar dados para o Power BI. ex. se o atraso for 3, a linha de dado será enviada a cada 3 segundos
                   Valor padrão será 2 segundos, para passar por cima dessa regra, utilize o metodo .wait()              
 
    """
    endpoint: str
    data: Dict 
    delay: int=2  
        
    def wait(self, other=None):
        ''' Atraso em segundos para enviar os dados '''
        if other==None:
            # default value is 2 seconds
            other = 2 
        sleep(other)    
        return self
    
    def post_data(self):
        ''' metodo post usado para enviar os dados'''
        if isinstance(self.data, dict):
            endpoint  = self.endpoint
            payload = [self.data]

            x = requests.post(endpoint, json = payload)
            if x.status_code==200:
                x=x
            else:
                print("Algo deu errado ! cheque o endpoint ou os dados")
        else:
            print("dado passado foge do dicionario.")
        return x