# Teste Estatístico para avaliação da probabilidade da variação dos valores de Sp02
import pandas as pd
from scipy.stats import kstest, lognorm
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np

# Abrir o excel
saturacao = pd.read_excel('sat_02.xlsx')
s = saturacao['sp02'].to_numpy()

# Ajusta os dados conforme uma distribuição log-normal e extrai os parâmetros
shape, loc, scale = lognorm.fit(s)

# Criar o histograma
plt.figure(figsize=(10, 6))
plt.hist(s, bins=30, color='purple', edgecolor='black', alpha=0.7)
plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=len(s)))

# Criação de um array de x-valores para fazer o gráfico da função de densidade de probabilidade log-normal
x = np.linspace(77, 100, 1000)



# Adicionar título e rótulos aos eixos
plt.title('Distribuição da Saturação do Oxigénio', fontsize=16)
plt.xlabel('Saturação do Oxigénio (%)', fontsize=14)
plt.ylabel('Frequência de Ocorrência', fontsize=14)
plt.legend()


# Exibir o gráfico
plt.show()