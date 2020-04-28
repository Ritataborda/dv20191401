


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
