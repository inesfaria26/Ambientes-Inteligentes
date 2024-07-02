import random
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np
import time
import json
import os
import pandas as pd

# Autenticação e acesso ao Google Sheets e ao Google Drive
#scope = ['https://www.google.apis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
#creditos = ServiceAccountCredentials.from_json_keyfile_name('/Users/inesfaria/Desktop/AmL-TPG1/credenciais.json', scope)
#cliente = gspread.authorize(creditos)

# Abertura do documento do Google Sheets e respetiva worksheet 
#documento = cliente.open('sheets1234') # Nome do Documento 
#worksheet = documento.worksheet('dados_recolhidos') # Nome da Folha
import pandas as pd
import json
from datetime import datetime
import time

import pandas as pd
import os
import time

try:
    # Carregamento dos dados do arquivo Excel em um DataFrame
    df = pd.read_excel('dataset_asma.xlsx')
    df['Tempo(s)'] = df['Tempo(s)'].astype(str)
    print("Arquivo Excel carregado com sucesso!")
    print(df.head())  # Exibir as primeiras linhas do DataFrame
    
    # Conversão do DataFrame para JSON e salvamento em arquivo
    df.to_json('dados.json', orient='records')
    print("Arquivo JSON criado com sucesso!")

except FileNotFoundError:
    print("O arquivo especificado não foi encontrado.")
except Exception as e:
    print("Ocorreu um erro ao carregar o arquivo Excel:", e)

if os.path.exists('dados.json'):
    with open('dados.json', 'r') as f:
        dados = json.load(f)
    if isinstance(dados, list):
        dados = {'data': dados}
    print("Dados JSON carregados com sucesso!")
else:
    dados = {}

# Atualização dos dados 
if not dados or time.time() - dados.get('last_updated', 0) > 10:
    dados['last_updated'] = time.time()
    dados['data'] = df.to_dict(orient='records')
    with open('dados.json', 'w') as f:
        json.dump(dados, f)


# Extração dos dados, havendo a iteração dos mesmo conforme se vai percorrendo o ficheiro
valores = [float(row['SpO2 (%)']) for row in dados['data'][1:]]

# Datas de início e de fim para simular os novos valores de saturação de oxigénio no sangue para os utilizadores que até então temos

start_date_1 = datetime.strptime('2024-04-10 15:28:00', '%Y-%m-%d %H:%M:%S')
end_date_1 = datetime.now()


# Criação de um dicionário para armazenar a média e o desvio-padrão do logaritmo dos valores de ? para cada minuto
distribuicao = {}
for i in range(0, 24):
    values = [np.log(float(row['SpO2 (%)'])) for row in dados['data'] if datetime.strptime(row['Tempo(s)'], '%Y-%m-%d %H:%M:%S').minute == i]
    if values:    
        distribuicao[i] = {'media': np.mean(values), 'std': np.std(values)}


# Simulação dos novos valores de 02 pelo intervalo definido por nós de 5 minutos
def novos_dados_02(start_date, end_date, distribuicao, dados, patient_name):
    while start_date < end_date:
        minute = start_date.minute
        if minute in distribuicao:
            ln_mean = distribuicao[minute]['media']
            ln_std = distribuicao[minute]['std']
            valor = int(random.lognormvariate(ln_mean, ln_std))
            nova_linha = [start_date.strftime('%Y-%m-%d %H:%M:%S'), valor, patient_name]            
            if 'data' not in dados:
                dados['data'] = []
            dados['data'].append(nova_linha)
        start_date += timedelta(minutes=5)

        time.sleep(0.5)
        
        #  Atualização do dados armazenados em cache se mais que 1 segundo tenha passado desde a última atualização
        intervalo_atualizacao = 1  # 1 segundo
        tempo_atual = time.time()
        last_updated = dados.get('last_updated')

        if last_updated is None or tempo_atual - last_updated > intervalo_atualizacao:
            dados['last_updated'] = tempo_atual
            for name in patient_names:
                n = name
            novo_dado = {
        'Tempo(s)': datetime.now().strftime('%Y-%m-%d  %H:%M:%S'),  # Data e hora atual
        'SpO2 (%)': random.randint(90, 100),  # Valor aleatório de saturação de oxigênio
        'username':n  # Nome do novo usuário (apenas para exemplo)
    }
    # Adiciona o novo dado à lista de dados
            dados['data'].append(novo_dado)

            # Salve os dados atualizados no arquivo JSON
            with open('dados.json', 'w') as f:
                json.dump(dados, f)

# Os pacientes simulados por nós inicialmente e criação de uma função loop para chamar a função 
patient_names = ['antonio'] 

for patient_name in patient_names:
    if patient_name == 'antonio':
        novos_dados_02(start_date_1, end_date_1, distribuicao, dados, patient_name)
    else:
        print(f"Invalid patient name: {patient_name}")


