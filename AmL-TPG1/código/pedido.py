#from oauth2client.service_account import ServiceAccountCredentials
import requests
import time
#import gspread
import numpy as np
import json
import datetime
import os
import random
from datetime import datetime
import requests
from Adafruit_IO import Client, RequestError, Feed


#Credenciais de autenticação do Adafruit IO
ADAFRUIT_IO_KEY = 'aio_aXDy61WmRmy5LSH9cVJlFs3XCJrD'
ADAFRUIT_IO_USERNAME = 'ines_faria'

# Criação de uma instância do cliente Adafruit IO
cli = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Autenticação e acesso ao Google Sheets e ao Google Drive
#scope = ['https://www.google.apis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
#creditos = ServiceAccountCredentials.from_json_keyfile_name('credenciais.json', scope)
#cliente = gspread.authorize(creditos)

# Abertura do documento do Google Sheets e respetiva worksheet 
#documento = cliente.open('dataset_asma') # Nome do Documento 
#worksheet = documento.worksheet('dados_recolhidos') # Nome da Folha - dados 
#worksheet2 = documento.worsheet('dados_poluicao') # Nome da Folha - dados da poluição do ar


# API key para o OpenWeatherMap - Air Pollution 
api_key = 'e56a058a29d2855eb09daf3639552b97'

# API endpoint URL e API key para o sistema de autenticacão AuthPro
#api_url = ' https://www.authpro.com/api27list' # Dados acerca dos utilizadores
#api_key_2 = 'n6e8n8ee4m6jtapt'

# Parâmetros para o pedido ao AuthPro
parametros = {
    'user': 'ines_faria',
    'api_key': 'e56a058a29d2855eb09daf3639552b97',
    'record':'{login}{cidade}'
}
# Vamos carregar os dados do arquivo JSON para um dicionário
if os.path.exists('dados.json'):
    with open('dados.json', 'r') as f:
        dados = json.load(f)
    if isinstance(dados, list):
            dados = {'data': dados}
else:
    dados = {}

if os.path.exists('poluicao_ar.json'):
        with open('poluicao_ar.json', 'r') as f:
            data_to_save = json.load(f)
        if isinstance(dados, list):
            dados = {'dadosP': []}
        print("Dados JSON carregados com sucesso!")
else:
    data_to_save = {}



# Atualização dos dados 
if not dados or time.time() - dados.get('last_updated', 0) > 10:
    dados['last_updated'] = time.time()
    with open('dados.json', 'w') as f:
        json.dump(dados, f)

# Extração dos dados, havendo a iteração dos mesmo conforme se vai percorrendo o ficheiro

#for row in dados['data']:
    #print(row)

while True:


    # Verifica se o dado está dentro do limite desejado
    def is_valid(row, minute):
        return isinstance(row, dict) and 'Tempo(s)' in row and datetime.strptime(row['Tempo(s)'], '%Y-%m-%d %H:%M:%S').minute == minute

# Cria a distribuição de poluição
    distribuicao = {}
    for minute in range(60):
        values = [np.log(float(row['SpO2 (%)'])) for row in dados['data'] if is_valid(row, minute)]
        if values:
            distribuicao[minute] = {'media': np.mean(values), 'std': np.std(values)}
    # Efetuar API request do AuthPro
    #response = requests.post(api_url, data=parametros)

    # Verificar se a resposta foi bem sucedida
    #if response.status_code == 200:
        # Extração da lista de users e respetivas cidades
        #members = response.json()['members']
        #users = [member['login'] for member in members]
        #cities = [member['cidade'] for member in members]
    #else:
        #print(f'Request failed with status code {response.status_code}: {response.text}')
    
        # Loop sobre o user e respetiva cidade para obter uma descrição sobre a poluição do ar da localidade respetiva
   
    users = ['antonio']
            
        # Obtenção da descrição da poluição do ar do OpenWeatherMap API para esse exato momento
    base_url = "http://api.openweathermap.org/data/2.5/air_pollution?"
        #full_url = base_url + "appid=" + api_key + "&q=" + city_name 
        #full_url = base_url + "&appid=" + api_key + "city:" + city_name 
    full_url = f"{base_url}lat={38.7071}&lon={-9.13549}&appid={api_key}" # Substituir city_name pelos dados de latitude e longitude da cidade
    response = requests.get(full_url)
    data = response.json()
    current_time = datetime.now()
    minute = current_time.minute
    

    if response.status_code == 200 and minute in distribuicao:
        # Passar a descrição sobre a poluição do ar para o respetivo worksheet
        air_actual = data["list"][0]["main"]["aqi"]
        print(air_actual)
        data_to_save['dadosP'].append({'users': users, 'cities': 'Lisboa','time': current_time.strftime('%d/%m/%Y %H:%M:%S'), 'pollution_data': air_actual})
    else:
        print(f"Informações sobre a poluição do ar não encontradas para Lisboa")

    current_time = datetime.now()
    for user in users:
        minute = current_time.minute
        ln_mean = distribuicao[minute]['media']
        ln_std = distribuicao[minute]['std']
        valor = int(random.lognormvariate(ln_mean, ln_std))
        data_to_save['dadosP'].append({'users': users, 'cities': 'Lisboa','time': current_time.strftime('%d/%m/%Y %H:%M:%S'), 'pollution_data': air_actual})
    # Salvar o tempo atual
    data_to_save['dadosP'].append({'time': current_time.strftime('%d/%m/%Y %H:%M:%S')})    
    with open('poluicao_ar.json', 'w') as f:
        json.dump(data_to_save, f)

    pollution_level = air_actual
    if pollution_level >= 3 and pollution_level <= 5:  
        high_pollution_worksheet_name = f"alta-poluicao-{user.lower()}"
        try:
            # Verificar se o feed existe
            new_feed = cli.feeds(high_pollution_worksheet_name)
            try:
                # Enviar dados para o Adafruit IO
                cli.send_data(f'alta-poluicao-{user.lower()}', pollution_level)
            except RequestError as e:
                print(f'Erro ao enviar dados para o Adafruit IO: {e}')
        except RequestError:
            # Caso o feed não exista, criar um novo
            new_feed = Feed(name=high_pollution_worksheet_name)
            cli.create_feed(new_feed)
            try:
                # Enviar dados para o Adafruit IO
                cli.send_data(f'alta-poluicao-{user.lower()}', pollution_level)
            except RequestError as e:
                print(f'Erro ao enviar dados para o Adafruit IO: {e}')
    
    valor = np.exp(ln_mean)
        #Condições referentes às notificações que pretendemos obter usando o Adafruit IO e IFTTT
    print(valor)
    if valor < 90:
        print(valor)
        low_sat_worksheet_name = f"baixos-valores{user.lower()}"
        try:
                # Caso exista
            new_feed = cli.feeds(low_sat_worksheet_name)
            try:
                cli.send_data(f'baixos-valores{user.lower()}', valor)
            except RequestError as e:
                print(f'Erro ao enviar dados para o Adafruit IO: {e}')
        except RequestError:
                            # Caso não exista, cria
            new_feed = Feed(name= low_sat_worksheet_name)
            cli.create_feed(new_feed)
            try:
                cli.send_data(f'baixos-valores{user.lower()}', valor)
            except RequestError as e:
                print(f'Erro ao enviar dados para o Adafruit IO: {e}')
    
    time.sleep(10)