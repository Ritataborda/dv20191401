import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

#import the dataset
path_datasets = ''
path_lesson = path_datasets
df = pd.read_excel(path_datasets + 'dataset.xlsx')

#option labels
procedimento_options = [
    dict(label='Tipo ' + procedimento, value=procedimento)
    for procedimento in df['Tipo de Procedimento'].unique()]

categoria_options = [
    dict(label='Cat ' + categoria, value=categoria)
    for categoria in df['Categoria'].unique()]

distrito_options = [
    dict(label="Reg " + distrito, value=distrito)
    for distrito in df['Distrito'].unique()]

entidade_radio = dcc.RadioItems(
                            id="entidade_radio",
                            options=[
                                {"label": "Entidade(s) Adjudicante(s)", "value": "Entidade(s) Adjudicante(s)"},
                                {"label": "Entidade(s) Adjudicatária(s)", "value": "Entidade(s) Adjudicatária(s)"},
                            ],
                            value="Entidade(s) Adjudicante(s)",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        )

dropdown_procedimento = dcc.Dropdown(
        id='procedimento_drop',
        options=procedimento_options,
        value=[],
        multi=True,
        className="dcc_control",)

dropdown_categoria = dcc.Dropdown(
        id='categoria_drop',
        options=categoria_options,
        value=[],
        multi=True,
        className="dcc_control",)

dropdown_distrito = dcc.Dropdown(
        id='distrito_drop',
        options=distrito_options,
        value=[],
        multi=True,
        className="dcc_control",)

date_picker = dcc.DatePickerRange(
            id='date_picker',
            start_date_placeholder_text='Select a date!',
            end_date_placeholder_text='Select a date!',
            min_date_allowed=pd.to_datetime('2019-01-01'),
            max_date_allowed=pd.to_datetime('2021-01-01'),
            initial_visible_month=pd.to_datetime('2019-01-01'),
            start_date=pd.to_datetime('2019-01-01'),
            end_date=pd.to_datetime('2021-01-01'),
            className="dcc_control",
        )

month_slider = dcc.RangeSlider(
        id='month_slider',
        min=1,
        max=12,
        value=[1, 12],
    marks={'1': 'jan',
           '2': 'fev',
           '3': 'mar',
           '4': 'apr',
           '5': 'may',
           '6': 'jun',
           '7': 'jul',
           '8': 'aug',
           '9': 'sep',
           '10': 'oct',
           '11': 'nov',
           '12': 'dec'},
    step=1
    )

#the application code
app = dash.Dash(__name__, external_stylesheets='')

app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src="assets/dash-logo.png",
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Portuguese Public Procurement",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Dashboard", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Filtro Temporal:",
                            className="control_label",
                        ),
                        date_picker,
                        html.P(
                            "Escolha o Tipo de Contratação:",
                            className="control_label",
                        ),
                        dropdown_procedimento,
                        html.P("Filtre por CPV do Procedimento:", className="control_label"),
                        dropdown_categoria,
                        html.P("Filtre por Distrito:", className="control_label"),
                        dropdown_distrito,
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6("Nr total de contratos"), dcc.Loading(html.Div([html.H6("...")],
                                    id="numero_contratos",
                                    style={"font-size":20, "font-weight":"bold"}))],
                                    className="mini_container",),

                                html.Div(
                                    [html.H6("Valor total gasto"), dcc.Loading(html.Div([html.H6("...")],
                                    id="valor_contratos",
                                    style={"font-size":20, "font-weight":"bold"}))],
                                    className="mini_container",),

                                html.Div(
                                    [html.H6("Valor médio por contrato"), dcc.Loading(html.Div([html.H6("...")],
                                    id="mean_contratos",
                                    style={"font-size":20, "font-weight":"bold"}))],
                                    className="mini_container",),

                                html.Div(
                                    [html.H6("Número de clientes"), dcc.Loading(html.Div([html.H6("...")],
                                    id="num_clientes",
                                    style={"font-size": 20, "font-weight": "bold"}))],
                                    className="mini_container",),],id="info-container",
                                    className="row container-display",),

                        html.Div(
                            [
                                html.P(
                                    "Escolha o Tipo de Entidade:",
                                    className="control_label",
                                ),
                                entidade_radio,
                                dcc.Graph(id='bar_graph')],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div([
            html.Div(
                [dcc.Graph(id="scatter_graph")],
                className="pretty_container seven columns",
            ),
            html.Div(
                [dcc.Graph(id="pie_graph")],
                className="pretty_container five columns",
            ),
        ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

@app.callback(
    [Output('numero_contratos', 'children'),
     Output('valor_contratos', 'children'),
     Output('mean_contratos', 'children'),
     Output('num_clientes', 'children'),
     Output('bar_graph', 'figure'),
     Output('pie_graph', 'figure'),
     Output('scatter_graph', 'figure')],
    [Input('procedimento_drop', 'value'),
     Input('categoria_drop', 'value'),
     Input('distrito_drop', 'value'),
     Input('date_picker', 'start_date'),
     Input('date_picker', 'end_date'),
     Input('entidade_radio', 'value')]
)
def update_graph(procedimentos, categorias, distritos, start_date, end_date, entidade):

    # converter colunas para formato desejado
    df['Data de Publicação'] = pd.to_datetime(df['Data de Publicação'])
    df['Preço Contratual'] = pd.to_numeric(df['Preço Contratual'])

    # filtrar df pelas datas selecionadas
    filtered_by_dates_df = df[(df['Data de Publicação'] >= start_date) & (df['Data de Publicação'] <= end_date)]

    # filtrar df pelas colunas necessárias
    filtered_df = filtered_by_dates_df[['Data de Publicação', 'Entidade(s) Adjudicante(s)', 'Entidade(s) Adjudicatária(s)',
                                        'Tipo de Procedimento', 'Categoria', 'Distrito', 'Preço Contratual']]

    # filtrar df pela lista de procedimentos
    if procedimentos:
        filtered_df = filtered_df.loc[filtered_df['Tipo de Procedimento'].isin(procedimentos)]

    # filtrar df pela lista de categorias
    if categorias:
        filtered_df = filtered_df.loc[filtered_df['Categoria'].isin(categorias)]

    # filtrar df pela lista de distritos
    if distritos:
        filtered_df = filtered_df.loc[filtered_df['Distrito'].isin(distritos)]

    # Numero de contratos
    num_con = filtered_df.shape[0]

    # Valor total dos contratos
    total_value = filtered_df['Preço Contratual'].sum()
    total_value = str(f"{int(total_value):,}") + str(" €")

    # Valor médio dos contratos
    mean_value = filtered_df['Preço Contratual'].mean()
    mean_value = str(f"{int(mean_value):,}") + str(" €")

    # Número de entidades, dependendo da escolha no radio button (Adjudicatárias ou Adjudicantes)
    numero_de_clientes = filtered_df[entidade].unique()
    numero_de_clientes = numero_de_clientes.shape[0]
    numero_de_clientes = str(f"{numero_de_clientes:,}")

    # BAR CHART - Preço contratual por entidade
    bar_series = filtered_df.groupby([entidade])['Preço Contratual'].sum()
    bar_series = bar_series.sort_values(ascending=False).head(10)

    bar_data = [dict(
        type='bar',
        x=bar_series,
        y=bar_series.index,
        name='bar_graph',
        orientation='h',
        text=bar_series.index,
        textposition='auto',
        insidetextanchor='start',
    )]

    bar_layout = dict(
        yaxis=dict(showticklabels=False),
        xaxis=dict(showgrid=False, zeroline=False, title='€'),
        margin=dict(l=30, r=30, b=20, t=40),
        hovermode="closest",
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        dragmode="select",
    )

    bar_fig = go.Figure(data=bar_data, layout=bar_layout)

    # PIE CHART - Preço contratual por tipo de procedimento
    pie_series = filtered_df.groupby(['Tipo de Procedimento'])['Preço Contratual'].sum()

    pie_data = [dict(
        type='pie',
        values=pie_series,
        labels=pie_series.index,
        name='pie_graph',
        hoverinfo="text+value+percent",
        textinfo="label+percent+name",
        hole=0.5,
        marker=dict(colors=["#fac1b7", "#a9bb95", "#92d8d8"]),
        domain={"x": [0, 0.45], "y": [0.2, 0.8]},
    )]

    pie_layout = dict(
        hovermode="closest",
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        font=dict(color="777777"),
        legend=dict(font=dict(color="#CCCCCC", size="10"), orientation="h", bgcolor="rgba(0,0,0,0)"),
        title="Tipo de Procedimento",
    )

    pie_fig = dict(data=pie_data, layout=pie_layout)

    # SCATTER CHART - Preço contratual por data
    scatter_series = filtered_df.groupby(['Data de Publicação'])['Preço Contratual'].sum()

    scatter_data = [
        dict(
            type="scatter",
            mode="lines+markers",
            name="Preço Contratual",
            x=scatter_series.index,
            y=scatter_series,
            line=dict(shape="linear", color="#F9ADA0"),
        )]

    scatter_layout = dict(
        margin=dict(l=30, r=30, b=20, t=40),
        hovermode="closest",
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        title="Preço Contratual",
    )
    scatter_fig = dict(data=scatter_data, layout=scatter_layout)

    return num_con, total_value, mean_value, numero_de_clientes, bar_fig, pie_fig, scatter_fig

if __name__ == '__main__':
    app.run_server(debug=True)
