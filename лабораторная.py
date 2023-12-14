import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_table
# Загрузка данных из файла
file_path = 'C:/Users/xttna/PycharmProjects/pythonProject2/12.csv' # Замените
на путь к вашему файлу
df = pd.read_csv(file_path)
# Преобразование столбцов с датами
df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])
df['Delivery Date'] = pd.to_datetime(df['Delivery Date'], errors='coerce')
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
# Создание экземпляра приложения
app = dash.Dash(__name__)
# Определение структуры дашборда
app.layout = html.Div([
html.H1('Данные транзакции', style={'textAlign': 'center'}),
dcc.Dropdown(
id='time-period-dropdown',
options=[
{'label': 'Месяц', 'value': 'M'},
{'label': 'Квартал', 'value': 'Q'},
{'label': 'Год', 'value': 'Y'}
],
value='M',
clearable=False,
style={'width': '50%', 'margin': '0 auto'}
),
dcc.Graph(id='time-series-chart'),
dcc.Graph(id='pie-chart'),
dcc.Graph(id='histogram'),
dcc.Graph(id='scatter-plot'),
html.Div(id='data-table')
], style={'padding': '20px'})
# Определение логики дашборда
@app.callback(
Output('time-series-chart', 'figure'),
Output('pie-chart', 'figure'),
Output('histogram', 'figure'),
Output('scatter-plot', 'figure'),
Output('data-table', 'children'),
[Input('time-period-dropdown', 'value')]
)
def update_charts(selected_time_period):
# Фильтрация и агрегация данных в соответствии с выбранным периодом
filtered_df = df.resample(selected_time_period, on='Transaction 
Date')['Quantity'].sum().reset_index()
# Проверка наличия данных после агрегации
if filtered_df.empty:
return dash.no_update # Возвращает текущее состояние, если данные отсутствуют
# Линейный график
time_series_chart = px.line(filtered_df, x='Transaction Date', y='Quantity', title='Временной ряд')
# Круговая диаграмма
pie_chart = px.pie(df, names='Transaction Type', title='Распределение типов сделок')
# Гистограмма
histogram = px.histogram(df, x='Unit Price', title='Распределение цен за
единицу')
# Точечный график
scatter_plot = px.scatter(df, x='Quantity', y='Unit Price', title='Корреляция между Количеством и Ценой за Единицу')
# Таблица с данными, используя dash_table.DataTable
data_table = dash_table.DataTable(
columns=[{"name": i, "id": i} for i in df.columns],
data=df.to_dict('records'),
page_size=10, # Количество строк на странице
style_table={'height': '300px', 'overflowY': 'auto'},
style_cell={
'textAlign': 'left',
'padding': '10px',
'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
'whiteSpace': 'normal'
},
style_header={
'backgroundColor': 'rgb(230, 230, 230)',
'fontWeight': 'bold'
}
)
return time_series_chart, pie_chart, histogram, scatter_plot, data_table
# Запуск приложения
if __name__ == '__main__':
app.run_server(debug=True)
