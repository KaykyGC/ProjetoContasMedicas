Gerador de Dados Hospitalares (Fake Data)

Este projeto consiste em um script Python desenvolvido para gerar dados fictícios realistas focados na área da saúde e gestão hospitalar. O objetivo é criar bases de dados ricas para estudos de Data Science, criação de Dashboards (Power BI, Tableau) e simulação de sistemas de gestão (como Tasy ou MV).

Funcionalidades

O script gera automaticamente arquivos Excel (.xlsx) e CSV contendo:

Dados Demográficos: ID do paciente, Nome, Idade (com lógica específica para Pediatria) e Sexo (estimado automaticamente pelo primeiro nome).

Dados Clínicos: Especialidade (Oncologia, Cardiologia, etc.), Médico Responsável, Diagnóstico (CID-10) e Procedimento Realizado.

Dados Financeiros: Valor do procedimento (baseado em média de mercado), Convênio e Status da Conta (Aberto, Pago, Glosado, Auditoria).

Indicadores de Qualidade: NPS (Net Promoter Score) e Tempo de Espera.

Tecnologias Utilizadas

Python 3.x

Pandas: Manipulação e estruturação dos dados.

Numpy: Geração de dados aleatórios e probabilísticos.

Matplotlib: Geração automática de gráficos analíticos.

OpenPyXL: Exportação otimizada para Excel.

Como usar

1. Instalação das dependências

Certifique-se de ter o Python instalado. No terminal, execute:

pip install -r requirements.txt


2. Execução do script

Rode o arquivo principal para gerar os dados:

python hospital_data_generator.py


3. Resultado

Após a execução, os seguintes arquivos serão criados na pasta do projeto:

dados_pacientes_completo.csv: Base de dados bruta.

planilha_completa.xlsx: Base de dados formatada para Excel.

projeto_contas_grafico.png: Gráfico de visualização rápida dos convênios.

Estrutura e Regras de Negócio

O script aplica regras lógicas para garantir a consistência dos dados gerados:

Campo

Regra de Negócio Aplicada

Idade

Pacientes da especialidade Pediatria têm sempre entre 0 e 14 anos. Outras clínicas atendem de 15 a 90 anos.

Sexo

O gênero (M/F) é atribuído verificando o primeiro nome do paciente (ex: "Maria" -> F, "João" -> M).

Valores

Cada procedimento tem um custo fixo baseado em tabelas particulares reais (ex: Quimioterapia custa mais que uma Consulta).

Status Financeiro

Contas nos setores "Recepção" ou "Atendimento" ficam sempre como "Aberto". Apenas no "Faturamento" podem estar "Pagas" ou "Glosadas".

Médico

Cada especialidade possui um corpo clínico específico (ex: Cardiologistas só atendem na Cardiologia).

Desenvolvido para fins de estudo e portfólio em Análise de Dados.
