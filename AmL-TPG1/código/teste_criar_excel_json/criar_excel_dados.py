import pandas as pd
import json

# Abrir o arquivo JSON
with open('dados.json', 'r') as arquivo:
    # Carregar os dados do arquivo JSON
    dados_json = json.load(arquivo)

# Extrair os dados da chave 'data'
data = dados_json['data']

# Inicializar listas vazias para cada coluna
tempos = []
spo2 = []
usuarios = []

# Iterar sobre os itens da lista 'data'
for item in data:
    # Verificar se 'Tempo(s)' está presente no item
    if 'Tempo(s)' in item:
        tempos.append(item['Tempo(s)'])
    else:
        tempos.append(None)  # Se 'Tempo(s)' não estiver presente, adicionar None
    
    # Verificar se 'SpO2 (%)' está presente no item
    if 'SpO2 (%)' in item:
        spo2.append(item['SpO2 (%)'])
    else:
        spo2.append(None)  # Se 'SpO2 (%)' não estiver presente, adicionar None
    
    # Verificar se 'username' está presente no item
    if 'username' in item:
        usuarios.append(item['username'])
    else:
        usuarios.append(None)  # Se 'username' não estiver presente, adicionar None

# Criar DataFrame pandas
df = pd.DataFrame({
    'Tempo(s)': tempos,
    'SpO2 (%)': spo2,
    'username': usuarios
})

# Escrever em um arquivo Excel
df.to_excel('dados_excel.xlsx', index=False)

