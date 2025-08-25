import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# data aleatória
def random_dates(start, end, n=10):
    start_u = start.value//10**9
    end_u = end.value//10**9
    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')

start_date = pd.to_datetime('2025-01-01')
end_date = pd.to_datetime('2025-12-31')
num_datas = 50 # quantidade de datas aleatórias

datas = random_dates(start_date, end_date, n=num_datas)

nomes = []
with open("nomes.txt", "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        nomes.append(linha.strip())

convenios = []
with open("convenios.txt", "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
       convenios.append(linha.strip())
       
idades = np.random.randint(18,60)


df = pd.DataFrame({
    'nome': np.random.choice(nomes, num_datas),
    'convenio': np.random.choice(convenios, num_datas),
    'idade': np.random.randint(18, 60, num_datas),
    'data': datas
})
print(df)
df.to_csv('dados_pacientes.csv', index=False)

