import pandas as pd
import os
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np

# Diretório onde os arquivos CSV estão localizados
diretorio = r'C:\Users\F3OO\Python_OCNPy3\Natalia_scripts\LH_AD_NATALIASILVA\banvic_data'

# Filtrar apenas arquivos com extensão .csv
arquivos_csv = [f for f in os.listdir(diretorio) if f.endswith('.csv')]

# Dicionário para armazenar DataFrames
dataframes = {}

# Iterar sobre os arquivos e ler cada um em um DataFrame
for arquivo in arquivos_csv:
    caminho_completo = os.path.join(diretorio, arquivo)
    nome_df = os.path.splitext(arquivo)[0]  # Nome do DataFrame será o nome do arquivo sem extensão
    dataframes[nome_df] = pd.read_csv(caminho_completo)


# Preparação dos Dados de Transações
transacoes = dataframes['transacoes']
transacoes['data_transacao'] = pd.to_datetime(transacoes['data_transacao'], errors='coerce')
transacoes = transacoes.dropna(subset=['data_transacao', 'valor_transacao'])
# Preparação dos Dados de Clientes
clientes = dataframes['clientes']
# Preparação dos Dados de Contas
contas = dataframes['contas']
# Preparação dos Dados de Agências
agencias = dataframes['agencias']
# Mesclar os dados de transações com clientes e agências
# Mesclar os dados de transações com contas, clientes e agências
transacoes_completas = transacoes.merge(contas, on='num_conta', how='left').merge(clientes, on='cod_cliente', how='left').merge(agencias, on='cod_agencia', how='left')
# Exibir os primeiros registros das transações completas
#print(transacoes_completas.head())

#############################################################

# VISUALIZAÇÃO

#############################################################


# Criação das Visualizações

# Gráfico de Barras: Volume de Transações por Agência
# PLOT 1
fig_agencias = px.bar(transacoes_completas, x='nome', y='valor_transacao', title='Volume de Transações por Agência')

# Gráfico de Linha: Receita Mensal
transacoes_completas['month_year'] = transacoes_completas['data_transacao'].dt.to_period('M').astype(str)
receita_mensal = transacoes_completas.groupby('month_year')['valor_transacao'].sum().reset_index()
# PLOT 2
fig_receita_mensal = px.line(receita_mensal, x='month_year', y='valor_transacao', title='Receita Mensal')


# Análise do Dia da Semana com Maior Volume de Transações e Maior Valor Movimentado
transacoes_completas['weekday'] = transacoes_completas['data_transacao'].dt.weekday + 1
volume_transacoes_dia_semana = transacoes_completas.groupby('weekday')['cod_transacao'].count().reset_index()
volume_transacoes_dia_semana.columns = ['weekday', 'volume_transacoes']
valor_medio_dia_semana = transacoes_completas.groupby('weekday')['valor_transacao'].mean().reset_index()
valor_medio_dia_semana.columns = ['weekday', 'valor_medio']

dias_semana = {1: 'Segunda-feira', 2: 'Terça-feira', 3: 'Quarta-feira', 4: 'Quinta-feira', 5: 'Sexta-feira', 6: 'Sábado', 7: 'Domingo'}
volume_transacoes_dia_semana['weekday'] = volume_transacoes_dia_semana['weekday'].map(dias_semana)
valor_medio_dia_semana['weekday'] = valor_medio_dia_semana['weekday'].map(dias_semana)

# PLOT 3
fig_volume_transacoes_dia_semana = px.pie(volume_transacoes_dia_semana, names='weekday', values='volume_transacoes', title='Volume de Transações por Dia da Semana')
# PLOT 4
fig_valor_medio_dia_semana = px.pie(valor_medio_dia_semana, names='weekday', values='valor_medio', title='Valor Médio Movimentado por Dia da Semana')

# Análise de Valores Movimentados no Início e no Final do Mês
transacoes_completas['part_of_month'] = np.where(transacoes_completas['data_transacao'].dt.day <= 15, 'Início do Mês', 'Final do Mês')
valor_medio_part_of_month = transacoes_completas.groupby('part_of_month')['valor_transacao'].mean().reset_index()
# PLOT 5
fig_valor_medio_part_of_month = px.pie(valor_medio_part_of_month, names='part_of_month', values='valor_transacao', title='Valores Movimentados no Início e no Final do Mês')


# Inicializar o aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div([
    html.H1("Dashboard de KPIs do BanVic"),

    dcc.Graph(id='graph-agencias', figure=fig_agencias),
    dcc.Graph(id='graph-receita-mensal', figure=fig_receita_mensal),
    dcc.Graph(id='graph-volume-dia-semana', figure=fig_volume_transacoes_dia_semana),
    dcc.Graph(id='graph-valor-medio-dia-semana', figure=fig_valor_medio_dia_semana),
    dcc.Graph(id='graph-valor-medio-part-mes', figure=fig_valor_medio_part_of_month),

    html.Label('Selecione uma Agência:'),
    dcc.Dropdown(
        id='dropdown-agencia',
        options=[{'label': agencia, 'value': agencia} for agencia in transacoes_completas['nome'].unique()],
        value=transacoes_completas['nome'].unique()[0]
    ),

    dcc.Graph(id='graph-detalhamento-agencia')
])

# Atualizar gráficos com base na seleção do dropdown
@app.callback(
    Output('graph-detalhamento-agencia', 'figure'),
    [Input('dropdown-agencia', 'value')]
)
def atualizar_grafico_agencia(agencia_selecionada):
    df_filtrado = transacoes_completas[transacoes_completas['nome'] == agencia_selecionada]
    fig = px.bar(df_filtrado, x='data_transacao', y='valor_transacao', title=f'Detalhamento de Transações para a Agência: {agencia_selecionada}')
    return fig

# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)