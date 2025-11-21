import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

diretorio_script = os.path.dirname(os.path.abspath(__file__))
nomes_path = os.path.join(diretorio_script, 'BaseDados', 'nomes.txt')
convenios_path = os.path.join(diretorio_script, 'BaseDados', 'convenios.txt')

# Definição de Datas
start_date = pd.to_datetime('01-01-2025', format='%d-%m-%Y')
end_date = pd.to_datetime('31-12-2025', format='%d-%m-%Y')
num_datas = 50

# Dicionário de Preços e Procedimentos (A "Tabela de Preços")
# Valores baseados em médias particulares/convênios
tabela_precos = {
    'Oncologia':         {'cons': 500.00, 'trat_nome': 'Sessão de Quimioterapia', 'trat_valor': 1500.00},
    'Dermatologia':      {'cons': 350.00, 'trat_nome': 'Cauterização de Lesão',   'trat_valor': 600.00},
    'Pneumologia':       {'cons': 400.00, 'trat_nome': 'Espirometria Completa',   'trat_valor': 250.00},
    'Cardiologia':       {'cons': 450.00, 'trat_nome': 'Ecocardiograma',          'trat_valor': 580.00},
    'Neurologia':        {'cons': 600.00, 'trat_nome': 'Eletroencefalograma',     'trat_valor': 400.00},
    'Gastroenterologia': {'cons': 400.00, 'trat_nome': 'Endoscopia Digestiva',    'trat_valor': 950.00},
    'Ortopedia':         {'cons': 350.00, 'trat_nome': 'Infiltração Articular',   'trat_valor': 700.00},
    'Oftalmologia':      {'cons': 300.00, 'trat_nome': 'Mapeamento de Retina',    'trat_valor': 450.00},
    'Fisioterapia':      {'cons': 150.00, 'trat_nome': 'Sessão de Reabilitação',  'trat_valor': 120.00},
    'Psiquiatria':       {'cons': 500.00, 'trat_nome': 'Estimulação Magnética',   'trat_valor': 800.00},
    'pediatria':         {'cons': 350.00, 'trat_nome': 'Nebulização Assistida',   'trat_valor': 150.00}
}

# Dicionário de Médicos por Especialidade
medicos_db = {
    'Oncologia':         ['Dr. House', 'Dra. Wilson'],
    'Dermatologia':      ['Dra. Pimple', 'Dr. Skin'],
    'Pneumologia':       ['Dr. Ar', 'Dra. Pulmão'],
    'Cardiologia':       ['Dr. Coração', 'Dra. Veia'],
    'Neurologia':        ['Dr. Cérebro', 'Dra. Neuro'],
    'Gastroenterologia': ['Dr. Digest', 'Dra. Estômago'],
    'Ortopedia':         ['Dr. Osso', 'Dra. Joelho'],
    'Oftalmologia':      ['Dr. Olho', 'Dra. Visão'],
    'Fisioterapia':      ['Dr. Alonga', 'Dra. Move'],
    'Psiquiatria':       ['Dr. Freud', 'Dra. Jung'],
    'pediatria':         ['Dr. Kids', 'Dra. Baby']
}

# Função para gerar datas aleatórias com horário restrito
def random_dates_restricted(start, end, n):
    
    # Gera dias aleatórios
    date_range = (end - start).days
    random_days = np.random.randint(0, date_range, n)
    dates = start + pd.to_timedelta(random_days, unit='D')
    
    # Gera horas restritas (8h até 18h59)
    random_hours = np.random.randint(8, 19, n) 
    random_minutes = np.random.randint(0, 60, n)
    random_seconds = np.random.randint(0, 60, n)
    
    final_dates = dates + pd.to_timedelta(random_hours, unit='h') + \
                  pd.to_timedelta(random_minutes, unit='m') + \
                  pd.to_timedelta(random_seconds, unit='s')
    
    return final_dates

# Ler nomes
nomes = []
if not os.path.exists(nomes_path):
    # Cria dados fake se o arquivo não existir (para teste)
    nomes = [f"Paciente {i}" for i in range(100)]
    convenios = ["Unimed", "Bradesco", "Sulamerica", "Particular"]
else:
    with open(nomes_path, "r", encoding="utf-8", errors='replace') as arquivo:
        for linha in arquivo:
            nomes.append(linha.strip())

# Ler convênios
convenios = []
if os.path.exists(convenios_path):
    with open(convenios_path, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            convenios.append(linha.strip())
else:
     convenios = ["Unimed", "Bradesco", "Sulamerica", "Particular"]

# Garantir que temos nomes suficientes
# assert len(nomes) >= num_datas, "A lista de nomes deve ter pelo menos a quantidade de registros."

datas = random_dates_restricted(start_date, end_date, n=num_datas)

# Criar chave primária e nomes únicos
ids = [str(num).zfill(5) for num in np.random.choice(range(1, 99999), num_datas, replace=False)]
nomes_unicos = np.random.choice(nomes, num_datas, replace=False)

# Listas para armazenar os dados gerados no loop
clinicas_finais = []
idades_finais = []
tipos_atendimento = []
procedimentos = []
valores = []
sexos_finais = []          # Nova lista para Sexo
medicos_finais = []        # Nova lista para Médico
status_financeiros = []    # Nova lista para Status Financeiro
setores_finais = []        # Lista para Setor (movido para dentro do loop para alinhar com status)

lista_clinicas = list(tabela_precos.keys())

# Loop Principal de Geração Lógica
for _ in range(num_datas):
    # 1. Escolhe a Clínica
    clinica = np.random.choice(lista_clinicas)
    clinicas_finais.append(clinica)
    
    # 2. Regra da Idade (Pediatria vs Outros)
    if clinica == 'pediatria':
        idades_finais.append(np.random.randint(0, 15))
    else:
        idades_finais.append(np.random.randint(15, 91))
    
    # 3. Regra de Preço e Tipo (Consulta vs Tratamento)
    tipo = np.random.choice(['Consulta', 'Tratamento'], p=[0.7, 0.3])
    tipos_atendimento.append(tipo)
    
    if tipo == 'Consulta':
        procedimentos.append('Consulta Eletiva')
        valores.append(tabela_precos[clinica]['cons'])
    else:
        procedimentos.append(tabela_precos[clinica]['trat_nome'])
        valores.append(tabela_precos[clinica]['trat_valor'])

    # 4. NOVO: Escolhe o Médico baseado na Clínica (Especialidade)
    medico = np.random.choice(medicos_db[clinica])
    medicos_finais.append(medico)

    # 5. NOVO: Sorteia o Sexo
    sexo = np.random.choice(['M', 'F'], p=[0.48, 0.52])
    sexos_finais.append(sexo)

    # 6. Define o Setor (com pesos)
    opcoes_setor = ['Recepção', 'Atendimento', 'Faturamento', 'Em trânsito Fatur.', 'Em trânsito Atend.', 'Em trânsito Aut.']
    pesos_setor = [0.10, 0.30, 0.45, 0.05, 0.05, 0.05]
    setor_atual = np.random.choice(opcoes_setor, p=pesos_setor)
    setores_finais.append(setor_atual)

    # 7. NOVO: Define Status Financeiro baseado no Setor
    # Se estiver na recepção ou atendimento, a conta ainda está 'Aberta'
    if setor_atual in ['Recepção', 'Atendimento', 'Em trânsito Atend.', 'Em trânsito Aut.']:
        status_financeiros.append('Aberto')
    else:
        # Se já está no Faturamento ou indo pra lá, pode estar Paga, Glosada ou em Auditoria
        status = np.random.choice(['Pago', 'Glosa Parcial', 'Glosa Total', 'Auditoria'], p=[0.7, 0.15, 0.1, 0.05])
        status_financeiros.append(status)

# Criar DataFrame
df = pd.DataFrame({
    'id_paciente': ids,
    'nome': nomes_unicos,
    'sexo': sexos_finais,             # Nova Coluna
    'idade': idades_finais,
    'convenio': np.random.choice(convenios, num_datas),
    'Clinica': clinicas_finais,
    'Medico': medicos_finais,         # Nova Coluna
    'Setor': setores_finais,
    'Status_Fin': status_financeiros, # Nova Coluna
    'Tipo': tipos_atendimento,
    'Procedimento': procedimentos,
    'Valor_R$': valores,
    'data': pd.Series(datas).dt.strftime('%d/%m/%Y'), # Apenas Data
    'hora': pd.Series(datas).dt.strftime('%H:%M:%S')  # Apenas Hora
})

print(df.head(10))

# Exportar para CSV
df.to_csv('dados_pacientes_completo.csv', index=False)

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
excel_path = os.path.join(diretorio_script, 'planilha_completa.xlsx')

# Salva usando o caminho completo
df.to_excel(excel_path, sheet_name='Dados', index=False)