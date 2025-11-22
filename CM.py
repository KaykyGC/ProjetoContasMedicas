import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from faker import Faker 
import sqlite3

# CONFIGURAÇÃO INICIAL
fake = Faker('pt_BR') # Configura para gerar nomes em Português do Brasil
diretorio_script = os.path.dirname(os.path.abspath(__file__))

# CONFIGURAÇÕES GERAIS 
start_date = pd.to_datetime('01-01-2025', format='%d-%m-%Y')
end_date = pd.to_datetime('31-12-2025', format='%d-%m-%Y')
num_datas = 500  # Quantidade de linhas a gerar

# 1. TABELA DE PREÇOS E PROCEDIMENTOS
tabela_precos = {
    'Oncologia':         {'cons': 523.42, 'trat_nome': 'Sessão de Quimioterapia', 'trat_valor': 1856.32},
    'Dermatologia':      {'cons': 365.85, 'trat_nome': 'Cauterização de Lesão',   'trat_valor': 266.45},
    'Pneumologia':       {'cons': 412.30, 'trat_nome': 'Espirometria Completa',   'trat_valor': 245.88},
    'Cardiologia':       {'cons': 468.75, 'trat_nome': 'Ecocardiograma',          'trat_valor': 634.20},
    'Neurologia':        {'cons': 615.50, 'trat_nome': 'Eletroencefalograma',     'trat_valor': 328.90},
    'Gastroenterologia': {'cons': 425.60, 'trat_nome': 'Endoscopia Digestiva',    'trat_valor': 1344.92},
    'Ortopedia':         {'cons': 385.40, 'trat_nome': 'Infiltração Articular',   'trat_valor': 845.55},
    'Oftalmologia':      {'cons': 312.15, 'trat_nome': 'Mapeamento de Retina',    'trat_valor': 287.66},
    'Fisioterapia':      {'cons': 165.80, 'trat_nome': 'Sessão de Reabilitação',  'trat_valor': 118.45},
    'Psiquiatria':       {'cons': 532.10, 'trat_nome': 'Estimulação Magnética',   'trat_valor': 489.90},
    'pediatria':         {'cons': 345.50, 'trat_nome': 'Nebulização Assistida',   'trat_valor': 45.30}
}

# 2. BANCO DE DADOS DE MÉDICOS 
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

# 3. FUNÇÃO: DATAS RESTRITAS (Mantida pois é excelente para regra de negócio)
def random_dates_restricted(start, end, n):
    date_range = (end - start).days
    random_days = np.random.randint(0, date_range, n)
    dates = start + pd.to_timedelta(random_days, unit='D')
    
    # Gera hora entre 8 e 18
    random_hours = np.random.randint(8, 19, n) 
    random_minutes = np.random.randint(0, 60, n)
    random_seconds = np.random.randint(0, 60, n)
    
    final_dates = dates + pd.to_timedelta(random_hours, unit='h') + \
                  pd.to_timedelta(random_minutes, unit='m') + \
                  pd.to_timedelta(random_seconds, unit='s')
    return final_dates

# Lista de convênios (Podemos usar Faker para empresas ou manter fixo)
lista_convenios = ["Unimed", "Bradesco", "Sulamerica", "Amil", "Golden Cross", "Particular"]

# 4. GERAÇÃO DE DADOS (Processamento) 

# Gera datas iniciais (Vetorizado é mais rápido que loop)
datas = random_dates_restricted(start_date, end_date, n=num_datas)
ids = [str(fake.unique.random_int(min=1, max=99999)).zfill(5) for _ in range(num_datas)]

# Listas vazias
nomes_finais = []
clinicas_finais = []
idades_finais = []
tipos_atendimento = []
procedimentos = []
valores = []
sexos_finais = []          
medicos_finais = []        
status_financeiros = []    
setores_finais = []        
convenios_finais = []

lista_clinicas = list(tabela_precos.keys())

print("Gerando dados sintéticos com Faker...")

# LOOP PRINCIPAL
for i in range(num_datas):
    
    # A. Geração de Sexo e Nome (AGORA 100% COERENTE)
    sexo = np.random.choice(['M', 'F'])
    sexos_finais.append(sexo)
    
    if sexo == 'M':
        nomes_finais.append(fake.name_male())
    else:
        nomes_finais.append(fake.name_female())

    # B. Convênio
    convenios_finais.append(np.random.choice(lista_convenios))

    # C. Clínica Aleatória
    clinica = np.random.choice(lista_clinicas)
    clinicas_finais.append(clinica)
    
    # D. Idade (Lógica de Negócio: Pediatria)
    if clinica == 'pediatria':
        idades_finais.append(np.random.randint(0, 15))
    else:
        idades_finais.append(np.random.randint(15, 91))
    
    # E. Tipo e Preço
    tipo = np.random.choice(['Consulta', 'Tratamento'], p=[0.7, 0.3])
    tipos_atendimento.append(tipo)
    
    if tipo == 'Consulta':
        procedimentos.append('Consulta Eletiva')
        valores.append(tabela_precos[clinica]['cons'])
    else:
        procedimentos.append(tabela_precos[clinica]['trat_nome'])
        valores.append(tabela_precos[clinica]['trat_valor'])

    # F. Médico
    medico = np.random.choice(medicos_db[clinica])
    medicos_finais.append(medico)

    # G. Setor (Probabilidades)
    opcoes_setor = ['Recepção', 'Atendimento', 'Faturamento', 'Em trânsito Fatur.', 'Em trânsito Atend.', 'Em trânsito Aut.']
    pesos_setor = [0.10, 0.30, 0.45, 0.05, 0.05, 0.05]
    setor_atual = np.random.choice(opcoes_setor, p=pesos_setor)
    setores_finais.append(setor_atual)

    # H. Status Financeiro
    if setor_atual in ['Recepção', 'Atendimento', 'Em trânsito Atend.', 'Em trânsito Aut.']:
        status_financeiros.append('Aberto')
    else:
        status = np.random.choice(['Pago', 'Glosa Parcial', 'Glosa Total', 'Auditoria'], p=[0.7, 0.15, 0.1, 0.05])
        status_financeiros.append(status)

# 5. EXPORTAÇÃO 
df = pd.DataFrame({
    'id_paciente': ids,
    'nome': nomes_finais,
    'sexo': sexos_finais,
    'idade': idades_finais,
    'convenio': convenios_finais,
    'Clinica': clinicas_finais,
    'Medico': medicos_finais,
    'Setor': setores_finais,
    'Status_Fin': status_financeiros,
    'Tipo': tipos_atendimento,
    'Procedimento': procedimentos,
    'Valor_R$': valores,
    'data': pd.Series(datas).dt.strftime('%d/%m/%Y'),
    'hora': pd.Series(datas).dt.strftime('%H:%M:%S')
})

print(df.head(10))

# Salvar CSV
df.to_csv('dados_pacientes_faker.csv', index=False)
print("\nArquivo CSV salvo com sucesso.")

# Salvar Excel
excel_path = os.path.join(diretorio_script, 'planilha_faker.xlsx')
df.to_excel(excel_path, sheet_name='Dados', index=False)
print(f"Arquivo Excel salvo em: {excel_path}")



# 6. EXPORTAÇÃO PARA SQL (BANCO DE DADOS)
print("\nIniciando exportação para Banco de Dados SQL...")

# 6.1 Cria a conexão com um banco de dados local (cria o arquivo se não existir)
db_path = os.path.join(diretorio_script, 'hospital_db.db')
conexao = sqlite3.connect(db_path)

# 6.2 Envia os dados do DataFrame direto para uma tabela SQL
# 'tb_atendimentos' será o nome da tabela lá dentro
# if_exists='replace' substitui a tabela se ela já existir (bom para testes)
df.to_sql('tb_atendimentos', conexao, if_exists='replace', index=False)

print("Dados salvos na tabela 'tb_atendimentos' com sucesso!")

# 6.3 (BÔNUS) Prova Real: Vamos fazer uma consulta SQL via Python para testar
cursor = conexao.cursor()

# Query SQL real: Vamos contar quantos atendimentos existem por convênio via SQL
query = """
SELECT convenio, COUNT(*) as total 
FROM tb_atendimentos 
GROUP BY convenio 
ORDER BY total DESC
"""

print("\n--- RESULTADO DA CONSULTA SQL (TOP CONVÊNIOS) ---")
resultado = cursor.execute(query).fetchall()

for linha in resultado:
    print(f"Convênio: {linha[0]} | Total: {linha[1]}")

# Fecha a conexão para salvar tudo
conexao.close()
print("\nConexão com Banco de Dados encerrada.")