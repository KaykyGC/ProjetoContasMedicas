import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- CONFIGURAÇÃO DE CAMINHOS ---
# Garante que o script encontre os arquivos na pasta 'BaseDados' relativa ao script
diretorio_script = os.path.dirname(os.path.abspath(__file__))
nomes_path = os.path.join(diretorio_script, 'BaseDados', 'nomes.txt')
convenios_path = os.path.join(diretorio_script, 'BaseDados', 'convenios.txt')

# --- CONFIGURAÇÕES GERAIS ---
start_date = pd.to_datetime('01-01-2025', format='%d-%m-%Y')
end_date = pd.to_datetime('31-12-2025', format='%d-%m-%Y')
num_datas = 500  # Quantidade de linhas a gerar

# --- 1. TABELA DE PREÇOS E PROCEDIMENTOS ---
# Valores baseados em pesquisa de mercado 2024/2025 (Médias Particulares e CBHPM)
# Valores quebrados para simular taxas reais e impostos
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

# --- 2. BANCO DE DADOS DE MÉDICOS ---
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

# --- 3. FUNÇÃO: ESTIMAR SEXO PELO NOME (ATUALIZADA COM A LISTA) ---
def estimar_sexo(nome_completo):
    """Tenta adivinhar o sexo baseado no primeiro nome para manter consistência"""
    # Se for nome genérico tipo "Paciente 1", sorteia
    if "Paciente" in nome_completo:
        return np.random.choice(['M', 'F'])
    
    primeiro_nome = nome_completo.split()[0].lower()
    
    # Lista de exceções femininas que NÃO terminam em 'a' (Baseado no seu arquivo nomes.txt)
    femininos_excecao = [
        'alice', 'aline', 'beatriz', 'caroline', 'cristiane', 'daiane', 'daniele', 
        'elaine', 'elis', 'ester', 'fabiane', 'ingrid', 'isabel', 'isabelle', 
        'jaqueline', 'liz', 'luciene', 'maite', 'marlene', 'marli', 'michele', 
        'michelle', 'monique', 'nicole', 'raquel', 'regiane', 'simone', 'solange', 
        'sueli', 'tais', 'tatiane', 'thaís', 'viviane', 'carmen', 'luz'
    ]
    
    # Lista de exceções masculinas que TERMINAM em 'a' (raros em PT, mas existem)
    masculinos_excecao = ['luca', 'gianluca', 'nicolas', 'lucas', 'cineas', 'andrea']

    if primeiro_nome in femininos_excecao:
        return 'F'
    if primeiro_nome in masculinos_excecao:
        return 'M'
    
    # Regra geral do Português: Termina em 'a' -> Feminino, caso contrário -> Masculino
    if primeiro_nome.endswith('a'):
        return 'F'
    return 'M'

# --- 4. FUNÇÃO: DATAS RESTRITAS (08h as 19h) ---
def random_dates_restricted(start, end, n):
    # Gera dias aleatórios dentro do ano
    date_range = (end - start).days
    random_days = np.random.randint(0, date_range, n)
    dates = start + pd.to_timedelta(random_days, unit='D')
    
    # Gera hora entre 8 e 18 (o range(8, 19) vai de 8 até 18)
    # Assim garantimos horários tipo 18:59:59, mas nunca 19:01 ou 07:59
    random_hours = np.random.randint(8, 19, n) 
    random_minutes = np.random.randint(0, 60, n)
    random_seconds = np.random.randint(0, 60, n)
    
    final_dates = dates + pd.to_timedelta(random_hours, unit='h') + \
                  pd.to_timedelta(random_minutes, unit='m') + \
                  pd.to_timedelta(random_seconds, unit='s')
    
    return final_dates

# --- 5. CARREGAMENTO DE ARQUIVOS ---
nomes = []
if not os.path.exists(nomes_path):
    # Fallback se o arquivo não existir
    nomes = [f"Paciente {i}" for i in range(100)]
else:
    with open(nomes_path, "r", encoding="utf-8", errors='replace') as arquivo:
        for linha in arquivo:
            nomes.append(linha.strip())

convenios = []
if os.path.exists(convenios_path):
    with open(convenios_path, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            convenios.append(linha.strip())
else:
     convenios = ["Unimed", "Bradesco", "Sulamerica", "Particular"]

# --- 6. GERAÇÃO DE DADOS (Processamento) ---

# Gera datas e listas iniciais
datas = random_dates_restricted(start_date, end_date, n=num_datas)
ids = [str(num).zfill(5) for num in np.random.choice(range(1, 99999), num_datas, replace=False)]
nomes_unicos = np.random.choice(nomes, num_datas, replace=False)

# Listas vazias que serão preenchidas no loop
clinicas_finais = []
idades_finais = []
tipos_atendimento = []
procedimentos = []
valores = []
sexos_finais = []          
medicos_finais = []        
status_financeiros = []    
setores_finais = []        

lista_clinicas = list(tabela_precos.keys())

# LOOP PRINCIPAL
for i in range(num_datas):
    
    # A. Sexo vinculado ao Nome
    nome_atual = nomes_unicos[i]
    sexo = estimar_sexo(nome_atual)
    sexos_finais.append(sexo)

    # B. Clínica Aleatória
    clinica = np.random.choice(lista_clinicas)
    clinicas_finais.append(clinica)
    
    # C. Idade (Pediatria vs Outros)
    if clinica == 'pediatria':
        idades_finais.append(np.random.randint(0, 15))
    else:
        idades_finais.append(np.random.randint(15, 91))
    
    # D. Tipo (Consulta 70% / Tratamento 30%) e Preço
    tipo = np.random.choice(['Consulta', 'Tratamento'], p=[0.7, 0.3])
    tipos_atendimento.append(tipo)
    
    if tipo == 'Consulta':
        procedimentos.append('Consulta Eletiva')
        valores.append(tabela_precos[clinica]['cons'])
    else:
        procedimentos.append(tabela_precos[clinica]['trat_nome'])
        valores.append(tabela_precos[clinica]['trat_valor'])

    # E. Médico (Vinculado à Especialidade)
    medico = np.random.choice(medicos_db[clinica])
    medicos_finais.append(medico)

    # F. Setor (Probabilidade realista)
    opcoes_setor = ['Recepção', 'Atendimento', 'Faturamento', 'Em trânsito Fatur.', 'Em trânsito Atend.', 'Em trânsito Aut.']
    pesos_setor = [0.10, 0.30, 0.45, 0.05, 0.05, 0.05]
    setor_atual = np.random.choice(opcoes_setor, p=pesos_setor)
    setores_finais.append(setor_atual)

    # G. Status Financeiro (Vinculado ao Setor)
    if setor_atual in ['Recepção', 'Atendimento', 'Em trânsito Atend.', 'Em trânsito Aut.']:
        status_financeiros.append('Aberto')
    else:
        # Se já está no faturamento, sorteia se pagou ou glosou
        status = np.random.choice(['Pago', 'Glosa Parcial', 'Glosa Total', 'Auditoria'], p=[0.7, 0.15, 0.1, 0.05])
        status_financeiros.append(status)

# --- 7. CRIAÇÃO E EXPORTAÇÃO DO DATAFRAME ---
df = pd.DataFrame({
    'id_paciente': ids,
    'nome': nomes_unicos,
    'sexo': sexos_finais,
    'idade': idades_finais,
    'convenio': np.random.choice(convenios, num_datas),
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

print("Amostra dos dados gerados:")
print(df.head(10))

# Salvar CSV
df.to_csv('dados_pacientes_completo.csv', index=False)
print("\nArquivo CSV salvo com sucesso.")

# Salvar Excel
excel_path = os.path.join(diretorio_script, 'planilha_completa.xlsx')
df.to_excel(excel_path, sheet_name='Dados', index=False)
print("Arquivo Excel salvo com sucesso.")

# --- 8. GERAÇÃO DO GRÁFICO ---
convenio_counts = df['convenio'].value_counts().sort_values(ascending=True)

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

# Adiciona os números nas barras
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

print(f"Gráfico salvo em: {grafico_path}")