import pandas as pd
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np


# Diretório onde os arquivos CSV estão localizados
diretorio = r'C:\Users\F3OO\Python_OCNPy3\Natalia_scripts\LH_AD_NATALIASILVA\banvic_data'

# Dicionário para armazenar os DataFrames
dataframes = {}

# Listando todos os arquivos .csv no diretório
arquivos_csv = [f for f in os.listdir(diretorio) if f.endswith('.csv')]

# Lendo cada arquivo .csv e armazenando no dicionário de DataFrames
for arquivo in arquivos_csv:
    caminho_completo = os.path.join(diretorio, arquivo)
    nome_df = os.path.splitext(arquivo)[0]  # Nome do DataFrame será o nome do arquivo sem extensão
    dataframes[nome_df] = pd.read_csv(caminho_completo)
    print(f"Lido {arquivo} e armazenado no DataFrame '{nome_df}'.")

# Exibindo as primeiras linhas de cada DataFrame para verificar
for nome_df, df in dataframes.items():
    print(f"\nDataFrame '{nome_df}':")
    print(df.head())

#####################################################################
# TIPO DE CLIENTE MAIS RENTÁVEL

# Unindo os DataFrames relevantes
clientes = dataframes['clientes']
contas = dataframes['contas']
transacoes = dataframes['transacoes']

print("Colunas de 'clientes':", clientes.columns)
print("Colunas de 'contas':", contas.columns)
print("Colunas de 'transacoes':", transacoes.columns)

# Renomeando colunas para manter consistência (se necessário)
clientes.columns = [col.lower() for col in clientes.columns]
contas.columns = [col.lower() for col in contas.columns]
transacoes.columns = [col.lower() for col in transacoes.columns]

# Mesclando DataFrames para relacionar clientes, contas e transações
contas_clientes = pd.merge(contas, clientes, left_on='cod_cliente', right_on='cod_cliente', how='left')
contas_clientes_transacoes = pd.merge(transacoes, contas_clientes, left_on='num_conta', right_on='num_conta', how='left')

# Calculando a receita total por tipo de cliente (CPF ou CNPJ)
receita_por_tipo_cliente = contas_clientes_transacoes.groupby('tipo_cliente')['valor_transacao'].sum()

# Exibindo o resultado
print("\nReceita total por tipo de cliente:")
print(receita_por_tipo_cliente)

# Determinando qual tipo de cliente gera mais receita
tipo_cliente_mais_receita = receita_por_tipo_cliente.idxmax()
valor_mais_receita = receita_por_tipo_cliente.max()

print(f"\nO tipo de cliente que gera mais receita é: {tipo_cliente_mais_receita} com um total de receita de {valor_mais_receita:.2f}")


#####################################################################
# TAXA DE RETENÇÃO

# Convertendo a coluna 'data_transacao' para datetime
transacoes['data_transacao'] = pd.to_datetime(transacoes['data_transacao'])

# Mesclando 'transacoes' com 'contas' para adicionar 'cod_cliente' ao DataFrame de transações
transacoes = pd.merge(transacoes, contas[['num_conta', 'cod_cliente']], on='num_conta', how='left')

# Filtrando transações para os anos 2021 e 2022
transacoes_2021 = transacoes[transacoes['data_transacao'].dt.year == 2021]
transacoes_2022 = transacoes[transacoes['data_transacao'].dt.year == 2022]

# Obtendo os códigos dos clientes que fizeram transações em 2021 e 2022
clientes_2021 = transacoes_2021['cod_cliente'].unique()
clientes_2022 = transacoes_2022['cod_cliente'].unique()

# Calculando a quantidade de clientes que fizeram transações em ambos os períodos
clientes_retidos = len(set(clientes_2021) & set(clientes_2022))

# Calculando a quantidade de clientes que fizeram transações no período inicial (2021)
clientes_inicial = len(clientes_2021)

# Calculando a Taxa de Retenção de Clientes
if clientes_inicial > 0:
    taxa_retencao = (clientes_retidos / clientes_inicial) * 100
else:
    taxa_retencao = 0

# Exibindo o resultado
print(f"\nA Taxa de Retenção de Clientes é: {taxa_retencao:.2f}%")

#####################################################################
# CUSTO MEDIO DO CLIENTE

transacoes = pd.merge(transacoes, contas[['num_conta', 'cod_cliente']], on='num_conta', how='left')

# Mesclando 'transacoes' com 'contas' para adicionar 'cod_cliente' ao DataFrame de transações
transacoes = pd.merge(transacoes, contas[['num_conta', 'cod_cliente']], on='num_conta', how='left')

# Verificando as colunas após a mesclagem
print("Colunas de 'transacoes' após a mesclagem:", transacoes.columns)

# Escolhendo a coluna correta para 'cod_cliente'
transacoes['cod_cliente'] = transacoes['cod_cliente_x']

# Calculando o valor total das transações e o número de transações por cliente
transacoes_por_cliente = transacoes.groupby('cod_cliente').agg({'valor_transacao': 'sum', 'cod_transacao': 'count'}).rename(columns={'valor_transacao': 'valor_total', 'cod_transacao': 'num_transacoes'})

# Calculando o valor médio das transações por cliente
transacoes_por_cliente['valor_medio_transacao'] = transacoes_por_cliente['valor_total'] / transacoes_por_cliente['num_transacoes']

# Calculando a data da primeira e da última transação para cada cliente
data_transacoes_por_cliente = transacoes.groupby('cod_cliente')['data_transacao'].agg(['min', 'max']).rename(columns={'min': 'data_primeira_transacao', 'max': 'data_ultima_transacao'})

# Calculando a duração do relacionamento com o cliente em dias
data_transacoes_por_cliente['duracao_relacionamento'] = (data_transacoes_por_cliente['data_ultima_transacao'] - data_transacoes_por_cliente['data_primeira_transacao']).dt.days

# Calculando a duração média do relacionamento com o cliente
duracao_media_relacionamento = data_transacoes_por_cliente['duracao_relacionamento'].mean()

# Calculando o CLV como o produto entre o valor médio das transações e a duração média do relacionamento
transacoes_por_cliente['clv'] = transacoes_por_cliente['valor_medio_transacao'] * duracao_media_relacionamento

# Calculando o CLV médio
clv_medio = transacoes_por_cliente['clv'].mean()

# Exibindo o resultado
print(f"\nO Valor Médio do Cliente (Customer Lifetime Value - CLV) é: {clv_medio:.2f}")

#####################################################################
# TAXA DE CHURN

# Determinando os clientes que churnaram (estavam ativos em 2021, mas não em 2022)
clientes_2021 = set(transacoes_2021['cod_cliente'].unique())
clientes_2022 = set(transacoes_2022['cod_cliente'].unique())

clientes_churn = clientes_2021 - clientes_2022

# Calculando a quantidade de clientes que churnaram
num_clientes_churn = len(clientes_churn)

# Calculando a quantidade de clientes que estavam ativos no período inicial (2021)
num_clientes_inicial = len(clientes_2021)

# Calculando a Taxa de Churn
if num_clientes_inicial > 0:
    taxa_churn = (num_clientes_churn / num_clientes_inicial) * 100
else:
    taxa_churn = 0

# Exibindo o resultado
print(f"\nA Taxa de Churn é: {taxa_churn:.2f}%")

#####################################################################
# POPULARIDADE DE AGÊNCIA

# Obtendo os DataFrames relevantes
clientes = dataframes['clientes']
contas = dataframes['contas']
transacoes = dataframes['transacoes']
agencias = dataframes['agencias']

agencias.columns = [col.strip().lower() for col in agencias.columns]

# Convertendo a coluna 'data_abertura' e 'data_transacao' para datetime
agencias['data_abertura'] = pd.to_datetime(agencias['data_abertura'])
transacoes['data_transacao'] = pd.to_datetime(transacoes['data_transacao'])

# Filtrar colunas necessárias
agencias = agencias[['cod_agencia', 'tipo_agencia']]
contas = contas[['num_conta', 'cod_agencia']]
transacoes = transacoes[['cod_transacao', 'num_conta', 'data_transacao', 'nome_transacao', 'valor_transacao']]

# Verificando as colunas após a renomeação
print("Colunas de 'agencias' após a renomeação:", agencias.columns)

# Mesclando 'transacoes' com 'contas' para adicionar 'cod_agencia' ao DataFrame de transações
transacoes = pd.merge(transacoes, contas, on='num_conta', how='left')

# Mesclando o DataFrame resultante com 'agencias' para adicionar a coluna 'tipo_agencia'
transacoes = pd.merge(transacoes, agencias, on='cod_agencia', how='left')

# Verificando as colunas após as mesclagens
print("Colunas de 'transacoes' após as mesclagens:", transacoes.columns)

# Contando o número de transações realizadas em agências digitais e físicas
transacoes_por_tipo_agencia = transacoes['tipo_agencia'].value_counts()

# Exibindo o resultado
print("\nNúmero de transações por tipo de agência:")
print(transacoes_por_tipo_agencia)

# Criando um gráfico de pizza para comparar a popularidade das agências digitais e físicas
labels = transacoes_por_tipo_agencia.index
sizes = transacoes_por_tipo_agencia.values
colors = ['#ff9999','#66b3ff']
explode = (0.1, 0)  # destaca o primeiro pedaço (agência digital)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title('Popularidade da Agência Digital vs. Física')
plt.show()

# Calculando o valor total das transações por tipo de agência
valor_transacoes_por_tipo_agencia = transacoes.groupby('tipo_agencia')['valor_transacao'].sum()

# Exibindo o resultado
print("\nValor total das transações por tipo de agência:")
print(valor_transacoes_por_tipo_agencia)

# Calculando a diferença percentual entre as receitas das duas agências
digital_revenue = valor_transacoes_por_tipo_agencia.get('Digital', 0)
fisica_revenue = valor_transacoes_por_tipo_agencia.get('Física', 0)

if digital_revenue > fisica_revenue:
    percentual_diferenca = ((digital_revenue - fisica_revenue) / fisica_revenue) * 100
    print(f"\nA agência digital gera {percentual_diferenca:.2f}% mais receita do que a agência física.")
elif fisica_revenue > digital_revenue:
    percentual_diferenca = ((fisica_revenue - digital_revenue) / digital_revenue) * 100
    print(f"\nA agência física gera {percentual_diferenca:.2f}% mais receita do que a agência digital.")


###########################################################################
# TAXA DE CONVERSÃO DE PROPOSTA

# Obtendo o DataFrame relevante
propostas_credito = dataframes['propostas_credito']

# Renomeando colunas para manter consistência (se necessário)
propostas_credito.columns = [col.strip().lower() for col in propostas_credito.columns]

# Verificando as colunas do DataFrame de propostas de crédito
print("Colunas de 'proposta_credito':", propostas_credito.columns)

# Contando o número total de propostas submetidas
total_propostas = len(propostas_credito)

# Contando o número de propostas aprovadas
propostas_aprovadas = len(propostas_credito[propostas_credito['status_proposta'] == 'Aprovada'])

# Calculando a taxa de conversão
if total_propostas > 0:
    taxa_conversao = (propostas_aprovadas / total_propostas) * 100
else:
    taxa_conversao = 0

# Exibindo o resultado
print(f"\nA taxa de conversão de propostas de crédito é: {taxa_conversao:.2f}%")

# Identificando áreas para melhoria
# Podemos analisar os motivos de rejeição das propostas e outras métricas relevantes
propostas_rejeitadas = len(propostas_credito[propostas_credito['status_proposta'].str.lower().isin(['enviada', 'em análise', 'validação documentos'])])

# Exibindo as métricas adicionais
print(f"\nNúmero total de propostas submetidas: {total_propostas}")
print(f"Número de propostas aprovadas: {propostas_aprovadas}")
print(f"Número de propostas rejeitadas e pendentes: {propostas_rejeitadas}")

# Percentual de propostas rejeitadas e pendentes
if total_propostas > 0:
    percentual_rejeitadas = (propostas_rejeitadas / total_propostas) * 100
else:
    percentual_rejeitadas = 0

print(f"\nPercentual de propostas rejeitadas e pendentes: {percentual_rejeitadas:.2f}%")



########################################################################
# DIM_DATES

# Construir a Dimensão de Datas (dim_dates)
start_date = '2020-01-01'
end_date = '2030-12-31'
date_range = pd.date_range(start=start_date, end=end_date, freq='D')
dim_dates = pd.DataFrame(date_range, columns=['date'])
dim_dates['year'] = dim_dates['date'].dt.year
dim_dates['month'] = dim_dates['date'].dt.month
dim_dates['day'] = dim_dates['date'].dt.day
dim_dates['quarter'] = dim_dates['date'].dt.quarter
dim_dates['week'] = dim_dates['date'].dt.strftime('%U').astype(int)  # Alternativa para obter a semana do ano
dim_dates['weekday'] = dim_dates['date'].dt.weekday + 1  # +1 para que segunda-feira seja 1
dim_dates['is_weekend'] = dim_dates['weekday'] >= 6
dim_dates['day_of_year'] = dim_dates['date'].dt.dayofyear
dim_dates['is_holiday'] = False  # Placeholder, ajustar conforme a lista de feriados
dim_dates['is_business_day'] = ~dim_dates['is_weekend'] & ~dim_dates['is_holiday']
dim_dates['part_of_month'] = np.where(dim_dates['day'] <= 15, 'inicio', 'final')

# Exibir os primeiros registros da dimensão de datas
print(dim_dates.head())

# Salvar a dimensão de datas em um arquivo CSV, caso necessário
# dim_dates.to_csv('dim_dates.csv', index=False)

# Mesclar Transações com a Dimensão de Datas
transacoes = dataframes['transacoes']
transacoes['data_transacao'] = pd.to_datetime(transacoes['data_transacao'], errors='coerce')
transacoes = transacoes.dropna(subset=['data_transacao', 'valor_transacao'])

# Garantir que ambas as colunas de data estejam no formato de data (sem hora)
transacoes['data_transacao'] = transacoes['data_transacao'].dt.date
dim_dates['date'] = dim_dates['date'].dt.date

# Verificar se a coluna 'data_transacao' está no formato correto
print(transacoes['data_transacao'].head())
print(dim_dates['date'].head())

# Mesclar transações com a dimensão de datas
transacoes_com_datas = pd.merge(transacoes, dim_dates, left_on='data_transacao', right_on='date', how='left')
print(transacoes_com_datas.head())

# Pergunta 1: Qual dia da semana tem, em média, maior volume de transações e qual tem, também em média, maior valor movimentado?
# Calcular o volume de transações por dia da semana
volume_transacoes_dia_semana = transacoes_com_datas.groupby('weekday')['cod_transacao'].count().reset_index()
volume_transacoes_dia_semana.columns = ['weekday', 'volume_transacoes']
# Calcular o valor médio movimentado por dia da semana
valor_medio_dia_semana = transacoes_com_datas.groupby('weekday')['valor_transacao'].mean().reset_index()
valor_medio_dia_semana.columns = ['weekday', 'valor_medio']
# Mesclar os dois DataFrames
analise_dia_semana = pd.merge(volume_transacoes_dia_semana, valor_medio_dia_semana, on='weekday')
# Mapear os números dos dias da semana para nomes
dias_semana = {1: 'Segunda-feira', 2: 'Terça-feira', 3: 'Quarta-feira', 4: 'Quinta-feira', 5: 'Sexta-feira', 6: 'Sábado', 7: 'Domingo'}
analise_dia_semana['weekday'] = analise_dia_semana['weekday'].map(dias_semana)

# Exibir os resultados
print("Análise por Dia da Semana:")
print(analise_dia_semana)

# Identificar o dia da semana com maior volume de transações
dia_maior_volume = analise_dia_semana.loc[analise_dia_semana['volume_transacoes'].idxmax()]
print(f"Dia com Maior Volume de Transações: {dia_maior_volume['weekday']} com {dia_maior_volume['volume_transacoes']} transações")

# Identificar o dia da semana com maior valor médio movimentado
dia_maior_valor_medio = analise_dia_semana.loc[analise_dia_semana['valor_medio'].idxmax()]
print(f"Dia com Maior Valor Médio Movimentado: {dia_maior_valor_medio['weekday']} com R$ {dia_maior_valor_medio['valor_medio']:.2f}")

# Pergunta 2: O BanVic tem, em média, os maiores valores movimentados no início ou final de mês?

# Calcular o valor médio movimentado no início e no final do mês
valor_medio_part_of_month = transacoes_com_datas.groupby('part_of_month')['valor_transacao'].mean().reset_index()
valor_medio_part_of_month.columns = ['part_of_month', 'valor_medio']

# Exibir os resultados
print("Análise por Parte do Mês:")
print(valor_medio_part_of_month)

# Identificar a parte do mês com maior valor médio movimentado
parte_mes_maior_valor = valor_medio_part_of_month.loc[valor_medio_part_of_month['valor_medio'].idxmax()]
print(f"Parte do Mês com Maior Valor Médio Movimentado: {parte_mes_maior_valor['part_of_month']} com R$ {parte_mes_maior_valor['valor_medio']:.2f}")

################################################################
# Analisar Valores Movimentados no Início e no Final do Mês

# Calcular o valor médio movimentado no início e no final do mês
valor_medio_part_of_month = transacoes_com_datas.groupby('part_of_month')['valor_transacao'].mean().reset_index()
valor_medio_part_of_month.columns = ['part_of_month', 'valor_medio']

# Exibir os resultados
print("Análise por Parte do Mês:")
print(valor_medio_part_of_month)

# Identificar a parte do mês com maior valor médio movimentado
parte_mes_maior_valor = valor_medio_part_of_month.loc[valor_medio_part_of_month['valor_medio'].idxmax()]
print(f"Parte do Mês com Maior Valor Médio Movimentado: {parte_mes_maior_valor['part_of_month']} com R$ {parte_mes_maior_valor['valor_medio']:.2f}")

# Calcular a diferença percentual entre o início e o final do mês
valor_inicio = valor_medio_part_of_month.loc[valor_medio_part_of_month['part_of_month'] == 'inicio', 'valor_medio'].values[0]
valor_final = valor_medio_part_of_month.loc[valor_medio_part_of_month['part_of_month'] == 'final', 'valor_medio'].values[0]

# Calcular a diferença percentual
diferenca_percentual = ((valor_final - valor_inicio) / valor_inicio) * 100

# Exibir a diferença percentual
if diferenca_percentual > 0:
    print(f"O valor movimentado no final do mês é, em média, {diferenca_percentual:.2f}% maior do que no início do mês.")
else:
    print(f"O valor movimentado no início do mês é, em média, {abs(diferenca_percentual):.2f}% maior do que no final do mês.")

#############
# ANÁLISE SAZONAL
# Garantir que a coluna 'data_transacao' esteja no formato datetime
transacoes_com_datas['data_transacao'] = pd.to_datetime(transacoes_com_datas['data_transacao'])

# Criar uma nova coluna 'month_year' representando o período 'M' (ano e mês)
transacoes_com_datas['month_year'] = transacoes_com_datas['data_transacao'].dt.to_period('M')

# Calcular a receita mensal agrupando por 'month_year' e somando 'valor_transacao'
receita_mensal = transacoes_com_datas.groupby('month_year')['valor_transacao'].sum().reset_index()

# Exibir a receita mensal
print(receita_mensal)
import matplotlib.pyplot as plt

# Dados de exemplo fornecidos
# Criar DataFrame a partir dos dados
df = pd.DataFrame(data)
df['month_year'] = pd.PeriodIndex(df['month_year'], freq='M')

# Plotar gráfico de barras para a receita mensal
plt.figure(figsize=(12, 6))
plt.bar(receita_mensal['month_year'].astype(str), receita_mensal['valor_transacao'], color='blue')
plt.xlabel('Mês/Ano')
plt.ylabel('Valor da Transação (R$)')
plt.title('Análise Sazonal: Receita Mensal')
plt.xticks(rotation=90)
plt.tight_layout()

# Exibir o gráfico
plt.show()

# Filtrar os dados para o ano de 2022
df_2022 = receita_mensal[receita_mensal['month_year'].dt.year == 2022]

# Calcular a média mensal de valor_transacao para cada mês de 2022
media_mensal_2022 = df_2022.groupby('month_year')['valor_transacao'].mean().reset_index()

# Exibir a média mensal de 2022
print("Média Mensal para 2022:")
print(media_mensal_2022)

# Plotar gráfico de barras para a média mensal de 2022
plt.figure(figsize=(12, 6))
plt.bar(media_mensal_2022['month_year'].astype(str), media_mensal_2022['valor_transacao'], color='blue')
plt.xlabel('Mês/Ano')
plt.ylabel('Valor Médio da Transação (R$)')
plt.title('Análise Sazonal: Média Mensal para 2022')
plt.xticks(rotation=90)
plt.tight_layout()

# Exibir o gráfico
plt.show()

############################################
# Criar DataFrame a partir dos dados

# Calcular o volume de transações para cada mês de 2022
volume_transacoes_2022 = df_2022.groupby('month_year')['valor_transacao'].count().reset_index()
volume_transacoes_2022.columns = ['month_year', 'volume_transacoes']

# Exibir o volume de transações de 2022
print("Volume de Transações para 2022:")
print(volume_transacoes_2022)

# Identificar o mês com maior volume de transações
mes_maior_volume = volume_transacoes_2022.loc[volume_transacoes_2022['volume_transacoes'].idxmax()]
print(f"Mês com Maior Volume de Transações: {mes_maior_volume['month_year']} com {mes_maior_volume['volume_transacoes']} transações")

# Plotar gráfico de barras para o volume de transações de 2022
plt.figure(figsize=(12, 6))
plt.bar(volume_transacoes_2022['month_year'].astype(str), volume_transacoes_2022['volume_transacoes'], color='blue')
plt.xlabel('Mês/Ano')
plt.ylabel('Volume de Transações')