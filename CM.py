import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

diretorio_script = os.path.dirname(os.path.abspath(__file__))
nomes_path = os.path.join(diretorio_script, 'BaseDados', 'nomes.txt')
convenios_path = os.path.join(diretorio_script, 'BaseDados', 'convenios.txt')

# Função para gerar datas aleatórias
def random_dates(start, end, n=10):
    start_u = start.value // 10**9
    end_u = end.value // 10**9
    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')

start_date = pd.to_datetime('01-01-2025', format='%d-%m-%Y')
end_date = pd.to_datetime('31-12-2025', format='%d-%m-%Y')
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

# Gerar clinica
tipo_clinica = ['Oncologia', 'Demartologia', 'Pneumologia', 'Cardiologia', 'Neurologia', 'Gastroenterologia', 'Ortopedia', 'Oftalmologia', 'Fisioterapia','Psiquiatria','pediatria']
clinicas_escolhidas = np.random.choice(tipo_clinica, num_datas)

idades_geradas = []
for clinica in clinicas_escolhidas:
    if clinica == 'pediatria':
        # Se for pediatria, idade entre 0 e 14 anos (o 15 é exclusivo)
        idades_geradas.append(np.random.randint(0, 15))
    else:
        # Para as outras clínicas, idade entre 15 e 90 anos
        idades_geradas.append(np.random.randint(15, 91))


# Criar DataFrame
df = pd.DataFrame({
    'id_paciente': ids,
    'nome': nomes_unicos,
    'convenio': np.random.choice(convenios, num_datas),
    'Clinica': clinicas_escolhidas, 
    'idade': idades_geradas,
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

grafico_path = os.path.join(diretorio_script, 'projeto_contas_grafico.png')
plt.savefig(grafico_path, dpi=150, bbox_inches='tight')

print(f"\nGráfico 'projeto_contas_grafico.png' salvo com sucesso!")

# Cria o caminho completo para o Excel
excel_path = os.path.join(diretorio_script, 'planilha2.xlsx')

# Salva usando o caminho completo
df.to_excel(excel_path, sheet_name='Dados', index=False)