import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
nomes_path = os.path.join(script_dir, "nomes.txt")
convenios_path = os.path.join(script_dir, "convenios.txt")

# Função para gerar datas aleatórias
def random_dates(start, end, n=10):
    start_u = start.value // 10**9
    end_u = end.value // 10**9
    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')

start_date = pd.to_datetime('01-01-2025')
end_date = pd.to_datetime('31-12-2025')
num_datas = 50  # quantidade de datas aleatórias

datas = random_dates(start_date, end_date, n=num_datas)

# Ler nomes
nomes = []
with open(nomes_path, "r", encoding="utf-8", errors='replace') as arquivo:
    for linha in arquivo:
        nomes.append(linha.strip())

# Ler convênios
convenios = []
with open(convenios_path, "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        convenios.append(linha.strip())

# Garantir que temos nomes suficientes
assert len(nomes) >= num_datas, "A lista de nomes deve ter pelo menos a quantidade de registros."

# Criar chave primária e nomes únicos
ids = [str(num).zfill(5) for num in np.random.choice(range(1, 99999), num_datas, replace=False)]

nomes_unicos = np.random.choice(nomes, num_datas, replace=False)

tipo_clinica = ['Oncologia', 'Demartologia']

# Criar DataFrame
df = pd.DataFrame({
    'id_paciente': ids,
    'nome': nomes_unicos,
    'convenio': np.random.choice(convenios, num_datas),
    'Clinica': np.random.choice(tipo_clinica, num_datas), 
    'idade': np.random.randint(18, 60, num_datas),
    'data': pd.Series(datas).dt.strftime('%d/%m/%Y'), # Apenas Data
    'hora': pd.Series(datas).dt.strftime('%H:%M:%S') # Apenas Hora
})

print(df)

# Exportar para CSV
df.to_csv('dados_pacientes.csv', index=False)

# Contagem por convênio
convenio_counts = df['convenio'].value_counts().sort_values(ascending=True)

# Criar gráfico
plt.style.use('seaborn-v0_8-whitegrid')
plt.figure(figsize=(12, 14))

bars = plt.barh(convenio_counts.index, convenio_counts.values, color="#851D77", height=0.7)
plt.title('Total de Pacientes por Convênio', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Número de Pacientes', fontsize=12)
plt.ylabel('Convênio', fontsize=12)

ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.tick_params(axis='y', length=0)

for bar in bars:
    plt.text(
        bar.get_width() + 0.2,
        bar.get_y() + bar.get_height() / 2,
        f'{int(bar.get_width())}',
        va='center',
        ha='left',
        fontsize=10,
        color='black'
    )

plt.subplots_adjust(left=0.4)

grafico_path = os.path.join(script_dir, 'projeto_contas_grafico.png')
plt.savefig(grafico_path, dpi=150, bbox_inches='tight')

print(f"\nGráfico 'projeto_contas_grafico.png' salvo com sucesso!")

# Exportar para Excel
df.to_excel('planilha2.xlsx', sheet_name='Dados', index=False)