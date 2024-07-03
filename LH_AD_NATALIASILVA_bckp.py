import pandas as pd
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# Diretório onde os arquivos CSV estão localizados
diretorio = r'C:\Users\F3OO\Python_OCNPy3\Natalia_scripts\LH_AD_NATALIASILVA\banvic_data'

todos_arquivos = os.listdir(diretorio)
print("Arquivos no diretório:", todos_arquivos)

# Filtrar apenas arquivos com extensão .csv
arquivos_csv = [f for f in todos_arquivos if f.lower().endswith('.csv')]
print("Arquivos CSV encontrados:", arquivos_csv)

# Dicionário para armazenar DataFrames
dataframes = {}

# Iterar sobre os arquivos e ler cada um em um DataFrame
for arquivo in arquivos_csv:
    caminho_completo = os.path.join(diretorio, arquivo)
    # Nome da aba será o nome do arquivo sem extensão
    nome_aba = os.path.splitext(arquivo)[0]
    dataframes[nome_aba] = pd.read_csv(caminho_completo)

# Exibir os nomes das abas e o cabeçalho dos DataFrames
for nome_aba, df in dataframes.items():
    print(f"Aba: {nome_aba}")
    print(df.head())

# Concatenar todos os DataFrames em um único DataFrame
df = pd.concat(dataframes.values(), ignore_index=True, sort=True)

# Exibir o DataFrame combinado
print(df)



# _______________________________________________________________
#
# Dado o cenário descrito, onde diferentes personagens da empresa têm 
# perspectivas variadas sobre o uso da análise de dados, é importante desenvolver 
# uma estratégia de KPIs (Key Performance Indicators) que possa alinhar essas 
# diferentes visões e demonstrar o valor da análise de dados para todos os 
# stakeholders. Vamos definir alguns KPIs que podem atender às necessidades de 
# cada personagem e ajudar a amadurecer a cultura e o uso de dados dentro da 
# organização.
# _______________________________________________________________

# KPIs para Sofia Oliveira (CEO)
# Objetivo: Elevar o banco a novos patamares através da análise de dados.


# 1. Crescimento da Receita: Medir o aumento da receita decorrente de decisões informadas por análises de dados.
# Primeiramente, preciso encontrar o valor da receita, que pode ser calculada com
# base no valor das transações financeiras (valor_transacao), ou na propostas de 
# crédito, derivada de valores de financiamento (valor_financiamento), valores de 
# entrada (valor_entrada) ou valores de propostas (valor_proposta).
# Vamos calcular a receita a partir do valor das transações financeiras
# Converter a coluna de data de transação para datetime
df['data_transacao'] = pd.to_datetime(df['data_transacao'])

# Definir o período de tempo para análise (por exemplo, mensal)
df['mes_ano'] = df['data_transacao'].dt.to_period('M')

# Calcular a receita total para cada período
receita_por_mes = df.groupby('mes_ano')['valor_transacao'].sum().reset_index()
receita_por_mes.columns = ['mes_ano', 'receita']

# Exibir a receita por mês
print(receita_por_mes)

# Calcular o aumento da receita em relação ao mês anterior
receita_por_mes['aumento_receita'] = receita_por_mes['receita'].pct_change() * 100

# Exibir a receita por mês com o aumento percentual
print(receita_por_mes)

receita_por_mes['mes_ano'] = receita_por_mes['mes_ano'].astype(str)

# Calcular a média móvel da receita (por exemplo, média móvel de 3 meses)
receita_por_mes['tendencia'] = receita_por_mes['receita'].rolling(window=3).mean()

# Plotar o gráfico de linha mostrando a receita e a tendência
plt.figure(figsize=(12, 6))
sns.lineplot(x='mes_ano', y='receita', data=receita_por_mes, label='Receita')
sns.lineplot(x='mes_ano', y='tendencia', data=receita_por_mes, label='Tendência', color='red')
plt.title('Tendência da Receita Mensal')
plt.xlabel('Mês/Ano')
plt.ylabel('Receita')
plt.xticks(ticks=receita_por_mes['mes_ano'][::5], rotation=45)  # Exibe rótulos a cada 2 meses
plt.legend()
plt.show()



# 2. Retorno sobre o Investimento (ROI) em Análise de Dados
# Avaliar o retorno financeiro em comparação com o investimento em tecnologias de análise de dados.
investimento = 100000  # Exemplo de valor investido
df['ano'] = df['data_transacao'].dt.to_period('Y')

# Calcular a receita anual
receita_an = df.groupby('ano')['valor_transacao'].sum().reset_index()
receita_an.columns = ['ano', 'receita']
receita_an['ano'] = receita_an['ano'].astype(str)


# Supondo que o investimento foi feito nos últimos 2 anos:
retorno = receita_an.iloc[-2:]['receita'].sum() - investimento
roi = retorno / investimento
print(f"Retorno sobre o Investimento (ROI): {roi:.2f} %")


#KPIs para André Tech (Especialista em Tecnologia)
#Objetivo: Implementar técnicas avançadas de análise de dados para otimizar operações.

# 1. Eficiência Operacional
# Medir a redução de custos operacionais devido à automação e otimização de processos.
custo_operacional_inicial = 500000  # Exemplo de custo inicial
custo_operacional_atual = 450000  # Exemplo de custo após otimização
reducao_custo = (custo_operacional_inicial - custo_operacional_atual) / custo_operacional_inicial
print(f"Redução de Custo Operacional: {reducao_custo:.2%}")


# 2. Tempo de Processamento de Transações
# Monitorar a redução do tempo médio de processamento de transações.
# Não consigo calcular pois não tenho a data de aprovação das transações
tempo_medio_transacao = df['tempo_processamento_transacao'].mean()
print(f"Tempo Médio de Processamento de Transações: {tempo_medio_transacao:.2f} segundos")

# KPIs para Camila Diniz (Marketing)
# Objetivo: Melhorar a segmentação dos clientes e aumentar o investimento em marketing.

# 1. Taxa de Conversão de Campanhas de Marketing
# Medir a eficácia das campanhas de marketing em termos de conversão de leads.
leads_gerados = 1000  # Exemplo de leads gerados
conversoes = 150  # Exemplo de conversões
taxa_conversao_marketing = conversoes / leads_gerados
print(f"Taxa de Conversão de Campanhas de Marketing: {taxa_conversao_marketing:.2%}")

# 2. Taxa de Retenção de Clientes
#A taxa de retenção de clientes mede a porcentagem de clientes que continuam 
# ativos em um determinado período.
# Definir um período de tempo para análise, por exemplo, um ano
periodo_analise = '2015'

# Filtrar clientes que realizaram transações no período de análise
clientes_ativos_periodo = df[df['ano'] == int(periodo_analise)]['cod_cliente'].nunique()

# Filtrar clientes que realizaram transações no período anterior
clientes_ativos_anterior = df[df['data_transacao'].dt.year == int(periodo_analise) - 1]['cod_cliente'].nunique()

# Calcular a taxa de retenção
taxa_retencao = clientes_ativos_periodo / clientes_ativos_anterior
print(f"Taxa de Retenção de Clientes: {taxa_retencao:.2%}")

# 3. Valor Médio do Cliente (Customer Lifetime Value - CLV)
# O CLV estima o valor total que um cliente traz para a empresa ao longo de seu
# relacionamento.
# Calcular o valor médio das transações por cliente
valor_medio_transacao_por_cliente = df.groupby('cod_cliente')['valor_transacao'].mean(dropna='True')

# Estimar a duração média do relacionamento com o cliente (em anos)
duracao_media_cliente = 3  # Exemplo de duração média em anos

# Calcular o CLV
clv = valor_medio_transacao_por_cliente.mean() * duracao_media_cliente
print(f"Valor Médio do Cliente (CLV): R$ {clv:.2f}")


#3. Taxa de Churn (Cancelamento)
#A taxa de churn mede a porcentagem de clientes que deixaram de usar os serviços
# da empresa em um determinado período de tempo.
# Definir um período de tempo para análise, por exemplo, um ano
periodo_analise = '2022'

# Filtrar clientes que realizaram transações no período de análise
clientes_ativos_periodo = df[df['data_transacao'].dt.year == int(periodo_analise)]['cod_cliente'].unique()

# Filtrar clientes que realizaram transações no período anterior
clientes_ativos_anterior = df[df['data_transacao'].dt.year == int(periodo_analise) - 1]['cod_cliente'].unique()

# Calcular a taxa de churn
clientes_perdidos = len(set(clientes_ativos_anterior) - set(clientes_ativos_periodo))
taxa_churn = clientes_perdidos / len(clientes_ativos_anterior)
print(f"Taxa de Churn: {taxa_churn:.2%}")

# 4. Engajamento do Cliente
# O engajamento do cliente pode ser medido pelo número médio de transações por 
# cliente em um determinado período de tempo.
# Definir um período de tempo para análise, por exemplo, um ano
periodo_analise = '2022'

# Filtrar transações no período de análise
transacoes_periodo = df[df['data_transacao'].dt.year == int(periodo_analise)]

# Calcular o número médio de transações por cliente
engajamento_cliente = transacoes_periodo.groupby('cod_cliente')['cod_transacao'].count().mean()
print(f"Engajamento do Cliente (Transações por Cliente): {engajamento_cliente:.2f}")

#____________________________________________________________________________
# KPIs para Lucas Johnson (Análise Comportamental)
# Objetivo: Compreender o comportamento dos clientes em diversos canais.
#____________________________________________________________________________

# 1. Uso do PIX: Avaliar a adoção do PIX e seu impacto nas transações.
uso_pix = df[df['nome_transacao'] == 'PIX']['cod_transacao'].count()
total_transacoes = df['cod_transacao'].count()
taxa_uso_pix = uso_pix / total_transacoes
print(f"Taxa de Uso do PIX: {taxa_uso_pix:.2%}")

# 2. Inatividade de Clientes
# Identificar padrões de inatividade entre clientes.
inatividade_cliente = df[df['data_ultimo_lancamento'] < '2022-01-01']['cod_cliente'].nunique()
total_clientes = df['cod_cliente'].nunique()
taxa_inatividade = inatividade_cliente / total_clientes
print(f"Taxa de Inatividade dos Clientes: {taxa_inatividade:.2%}")

# 3. Popularidade da Agência Digital vs. Física
# Comparar o uso da agência digital com a agência física.
uso_agencia_digital = df[df['tipo_agencia'] == 'Digital']['cod_agencia'].count()
uso_agencia_fisica = df[df['tipo_agencia'] == 'Física']['cod_agencia'].count()
print(f"Uso da Agência Digital: {uso_agencia_digital}")
print(f"Uso da Agência Física: {uso_agencia_fisica}")



# Análise exploratória dos dados
df['data_transacao'] = pd.to_datetime(df['data_transacao'])
periodo_analise_inicio = '2022-01-01'
periodo_analise_fim = '2022-12-31'

# Filtrar clientes que realizaram transações no período de análise
clientes_ativos_periodo = df[(df['data_transacao'] >= periodo_analise_inicio) & (df['data_transacao'] <= periodo_analise_fim)]['cod_cliente'].unique()

# Filtrar clientes que realizaram transações no período anterior
clientes_ativos_anterior = df[df['data_transacao'] < periodo_analise_inicio]['cod_cliente'].unique()

# Calcular a taxa de churn
clientes_perdidos = len(set(clientes_ativos_anterior) - set(clientes_ativos_periodo))
taxa_churn = clientes_perdidos / len(clientes_ativos_anterior)
print(f"Taxa de Churn: {taxa_churn:.2%}")
#
# Mais alguns exemplos gerais de cálculo de KPIs
# _______________________________________________________________

# 1. Taxa de Conversão de Propostas de Crédito
# Proporção de propostas aprovadas em relação ao total de propostas recebidas.
# Filtrar propostas aprovadas
propostas_aprovadas = df[df['status_proposta'] == 'Aprovada']
taxa_conversao = len(propostas_aprovadas) / len(df[df['cod_proposta'].notnull()])
print(f"Taxa de Conversão de Propostas de Crédito: {taxa_conversao:.2%}")

# Valor Médio das Transações
# Pode ser calculado dividindo o valor total das transações pelo número total de transações.
valor_medio_transacoes = df['valor_transacao'].mean()
print(f"Valor Médio das Transações: R$ {valor_medio_transacoes:.2f}")

# Número de Contas Ativas
num_contas_ativas = df['num_conta'].nunique()
print(f"Número de Contas Ativas: {num_contas_ativas}")

# Saldo Médio por Conta
# Pode ser calculado dividindo o saldo total pelo número de contas.
saldo_medio_por_conta = df.groupby('num_conta')['saldo_total'].mean().mean()
print(f"Saldo Médio por Conta: R$ {saldo_medio_por_conta:.2f}")

# 5. Número de Transações por Cliente
# Agrupando as transações por cliente e contando o número de transações.
num_transacoes_por_cliente = df.groupby('cod_cliente')['cod_transacao'].count().mean()
print(f"Número Médio de Transações por Cliente: {num_transacoes_por_cliente:.2f}")

# Calcular o tempo médio de resolução
tempo_medio_resolucao = df['tempo_resolucao'].mean()
print(f"Tempo Médio de Resolução de Propostas de Crédito: {tempo_medio_resolucao:.2f} dias")







import pandas as pd
import os

# Diretório onde os arquivos CSV estão localizados
diretorio = r'C:\Users\F3OO\Python_OCNPy3\Natalia_scripts\LH_AD_NATALIASILVA\banvic_data'

# Verificar se o diretório está correto
if not os.path.exists(diretorio):
    raise Exception(f"O diretório {diretorio} não existe. Verifique o caminho.")

# Listar todos os arquivos no diretório para diagnóstico
todos_arquivos = os.listdir(diretorio)
print("Arquivos no diretório:", todos_arquivos)

# Filtrar apenas arquivos com extensão .csv
arquivos_csv = [f for f in todos_arquivos if f.lower().endswith('.csv')]
print("Arquivos CSV encontrados:", arquivos_csv)

# Dicionário para armazenar DataFrames
dataframes = {}

# Iterar sobre os arquivos e ler cada um em um DataFrame
for arquivo in arquivos_csv:
    caminho_completo = os.path.join(diretorio, arquivo)
    # Nome da aba será o nome do arquivo sem extensão
    nome_aba = os.path.splitext(arquivo)[0]
    dataframes[nome_aba] = pd.read_csv(caminho_completo)

# Exibir os nomes das abas e o cabeçalho dos DataFrames
for nome_aba, df in dataframes.items():
    print(f"Aba: {nome_aba}")
    print(df.head())
    print(df.columns)

# Converter colunas de data para datetime e remover valores ausentes

# Exemplo para a planilha de transações
if 'transacoes' in dataframes:
    transacoes = dataframes['transacoes']
    transacoes['data_transacao'] = pd.to_datetime(transacoes['data_transacao'], errors='coerce')
    transacoes = transacoes.dropna(subset=['data_transacao', 'valor_transacao', 'cod_cliente'])
    dataframes['transacoes'] = transacoes

# Exemplo para a planilha de clientes
if 'clientes' in dataframes:
    clientes = dataframes['clientes']
    clientes['data_inclusao'] = pd.to_datetime(clientes['data_inclusao'], errors='coerce')
    clientes = clientes.dropna(subset=['data_inclusao', 'cod_cliente'])
    dataframes['clientes'] = clientes

# Calcular a taxa de churn

if 'transacoes' in dataframes and 'clientes' in dataframes:
    transacoes = dataframes['transacoes']
    clientes = dataframes['clientes']

    # Definir um período de tempo para análise, por exemplo, o ano de 2022
    periodo_analise_inicio = '2022-01-01'
    periodo_analise_fim = '2022-12-31'

    # Filtrar clientes que realizaram transações no período de análise
    clientes_ativos_periodo = transacoes[(transacoes['data_transacao'] >= periodo_analise_inicio) & (transacoes['data_transacao'] <= periodo_analise_fim)]['cod_cliente'].unique()

    # Filtrar clientes que realizaram transações no período anterior
    clientes_ativos_anterior = transacoes[transacoes['data_transacao'] < periodo_analise_inicio]['cod_cliente'].unique()

    # Calcular a taxa de churn
    clientes_perdidos = len(set(clientes_ativos_anterior) - set(clientes_ativos_periodo))
    taxa_churn = clientes_perdidos / len(clientes_ativos_anterior) if len(clientes_ativos_anterior) > 0 else 0
    print(f"Taxa de Churn: {taxa_churn:.2%}")

# Calcular a receita por tipo de agência
if 'transacoes' in dataframes and 'agencia' in dataframes:
    transacoes = dataframes['transacoes']
    agencia = dataframes['agencia']

    # Remover valores NaN nas colunas essenciais
    transacoes = transacoes.dropna(subset=['valor_transacao', 'cod_agencia'])
    agencia = agencia.dropna(subset=['tipo_agencia', 'cod_agencia'])

    # Mesclar transações com informações da agência
    transacoes_agencia = pd.merge(transacoes, agencia, on='cod_agencia', how='inner')

    # Agrupar os dados por tipo de agência e calcular a receita total para cada tipo
    receita_por_tipo_agencia = transacoes_agencia.groupby('tipo_agencia')['valor_transacao'].sum().reset_index()
    receita_por_tipo_agencia.columns = ['tipo_agencia', 'receita_total']

    # Exibir a receita total por tipo de agência
    print(receita_por_tipo_agencia)

    # Identificar qual tipo de agência é mais lucrativo
    tipo_agencia_mais_lucrativo = receita_por_tipo_agencia.loc[receita_por_tipo_agencia['receita_total'].idxmax