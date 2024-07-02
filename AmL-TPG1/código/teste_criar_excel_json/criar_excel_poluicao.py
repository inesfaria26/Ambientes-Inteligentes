import pandas as pd
import json

with open('poluicao_ar.json', 'r') as arquivo1:
    # Carregar os dados do arquivo JSON
    poluicao = json.load(arquivo1)

data1 = poluicao['dadosP']

users = []
cities = []
time = []
pollution_data = []

# Iterar sobre os itens da lista 'data'
for item in data1:
    # Verificar se 'users' está presente no item
    if 'users' in item:
        user = item['users'][0] if isinstance(item['users'], list) and len(item['users']) > 0 else None
        users.append(user)
    else:
        users.append(None)  # Se 'users' não estiver presente, adicionar None
    
    # Verificar se 'cities' está presente no item
    if 'cities' in item:
        cities.append(item['cities'])
    else:
        cities.append(None)  # Se 'cities' não estiver presente, adicionar None
    
    # Verificar se 'time' está presente no item
    if 'time' in item:
        time.append(item['time'])
    else:
        time.append(None)  # Se 'time' não estiver presente, adicionar None
    
    # Verificar se 'pollution_data' está presente no item
    if 'pollution_data' in item:
        pollution_data.append(item['pollution_data'])
    else:
        pollution_data.append(None)  # Se 'pollution_data' não estiver presente, adicionar None

# Criar DataFrame pandas
df = pd.DataFrame({
    'users': users,
    'cities': cities,
    'time': time,
    'pollution_data': pollution_data
})

# Escrever em um arquivo Excel
df.to_excel('dados_poluicao.xlsx', index=False)



