import plotly.graph_objects as go
import pandas as pd
import numpy as np
path_datasets = 'C:/Users/jrferro/Desktop/'
path_lesson = path_datasets + 'ex1/'
ex1 = pd.read_excel(path_datasets + 'ex1.xlsx', sheet_name='aux2020')
ex1_week = pd.read_excel(path_datasets + 'ex1.xlsx', sheet_name='aux2020', index_col=0)
entidade_list = ex1_week.columns
data_1 = [dict(type='scatter',
             x=ex1_week.index,
             y=ex1_week[entidade],
             name=entidade)
                            for entidade in entidade_list]
layout_1 = dict(title=dict(
                        text='Procedimentos Criados'
                  ),
                  xaxis=dict(title='Semana 2020'),
                  yaxis=dict(title='Procedimentos Criados'))
fig_1 = go.Figure(data=data_1, layout=layout_1)

fig_1.show()



# The App itself

app = dash.Dash(__name__)

server = app.server




app.layout = html.Div(children=[
    html.H1(children='Procedimentos SaphetyGov'),

    html.Div(children='''
        Avaliação Semanal
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])




if __name__ == '__main__':
    app.run_server(debug=True)
