from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc
import plotly
from .monitor import update_df, df, CPU_COUNT, conections
import psutil
# Определение интервала обноления данных
UPDATE_INTERVAL = 75

# Инициализация экземпляра Dash приложения
dash_app = Dash(__name__, requests_pathname_prefix="/dashboard/", title="Project_P", external_stylesheets=[dbc.themes.DARKLY])
#dash_app = Dash(__name__, title="Project_P", external_stylesheets=[dbc.themes.DARKLY])

# Определение заголовка приложения
header = dbc.Row(
    dbc.Col(
        [
            html.Div(style={"height": 30}),
            html.H1("Project_P", className="text-center"),
        ]
    ),
    className="mb-4",
)

#-----------
# Определение элементов управления
controls = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Settings", className="card-title"),
            html.Label("Update Interval (seconds):"),
            dcc.Slider(
                id="update-interval-slider",
                min=1,
                max=300,
                step=1,
                value=UPDATE_INTERVAL,
                marks={i: str(i) for i in range(1, 301, 30)},
            ),
            html.Label("Display Data:"),
            dcc.Checklist(
                id="display-data-checkbox",
                options=[
                    {"label": "CPU", "value": "cpu"},
                    {"label": "RAM", "value": "ram"},
                    {"label": "SWAP", "value": "swap"},
                ],
                value=["cpu", "ram", "swap"],
            ),
        ]
    ),
    className="mt-4",
)

#-------------

# Определение макета приложения
dash_app.layout = dbc.Container(
    [
        header,
        controls,#--------
        dbc.Accordion(
            [
                # dbc.AccordionItem(
                #     [
                #         dcc.Graph(id="graph_cpu"),
                #         dcc.Graph(id="graph_cpu_avg"),
                #         dbc.Card(
                #             dbc.CardBody(id="CPU_sent")
                #         ),
                        
                #     ],
                #     title="CPU"
                # ),
                dbc.AccordionItem(
                                    [
                                        dcc.Graph(id="graph_cpu"),
                                        dcc.Graph(id="graph_cpu_avg"),
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.H4("CPU Information", className="card-title"),
                                                    html.P("Number of CPU Cores: " + str(CPU_COUNT)),
                                                    #html.P("CPU Frequency: " + str(psutil.cpu_freq().current)),
                                                ]
                                            )
                                        ),
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.H4("CPU Average Load", className="card-title"),
                                                    html.P("CPU Average Load: " + str(psutil.cpu_percent())),
                                                ]
                                            )
                                        ),
                                    ],
                                    title="CPU"
                                ),
                #--------
                dbc.AccordionItem(
                    [
                        dcc.Graph(id="graph_ram"),
                        dcc.Graph(id="graph_swap"),
                    ],
                    title="RAM"
                ),
                dbc.AccordionItem(
                    [
                        dcc.Graph(id="graph_rom"),
                    ],
                    title="ROM"
                ),
                dbc.AccordionItem(
                    [
                        dcc.Graph(id="network"),
                        dbc.Card(
                            dbc.CardBody(id="net_sent")
                        ),
                        dcc.Graph(id="graph_connections"),
                    ],
                    title="Network"
                ),
                # dbc.AccordionItem(
                #     [
                #         dcc.Graph(id="system"),
                #     ],
                #     title="System"
                # ),
            ]
        ),
        dcc.Interval(id="timer", interval=UPDATE_INTERVAL),
    ],
    fluid=True,
    className='bg-dark',
)

# # Коллбэк для обновления графика CPU
# @callback(Output("graph_cpu", 'figure'), Input("timer", 'n_intervals'))
# def update_graph(n):
#     # Обновление данных в мониторе
#     update_df()
    
#     # Построение графика
#     traces = list()
#     for t in df.columns[:CPU_COUNT]:
#         traces.append(
#             plotly.graph_objs.Line(
#                 x=df.index,
#                 y=df[t],
#                 name=t
#             )
#         )
#     return {"data": traces, "layout": {"template": "plotly_dark"}}

# # Коллбэк для обновления графика средней загрузки CPU
# @callback(Output("graph_cpu_avg", 'figure'), Input("timer", 'n_intervals'))
# def update_cpu_avg_graph(n):
#     # Обновление данных в мониторе
#     update_df()
    
#     # Построение графика средней загрузки CPU
#     traces = list()
#     traces.append(
#         plotly.graph_objs.Line(
#             x=df.index,
#             y=df['cpu_avg'],
#             name='CPU Average'
#         )
#     )
#     return {"data": traces, "layout": {"template": "plotly_dark"}}, f"Total sent"
# Коллбэк для обновления графика CPU

#------
# Коллбэк для обновления интервала обновления
@dash_app.callback(
    Output("timer", "interval"),
    Input("update-interval-slider", "value")
)
def update_interval(value):
    return value   # Переводим значение в миллисекунды

# Коллбэк для обновления отображаемых данных
@dash_app.callback(
    Output("graph_cpu", "style"),
    Output("graph_ram", "style"),
    Output("graph_swap", "style"),
    Input("display-data-checkbox", "value")
)
def update_displayed_data(value):
    cpu_style = {} if "cpu" in value else {"display": "none"}
    ram_style = {} if "ram" in value else {"display": "none"}
    swap_style = {} if "swap" in value else {"display": "none"}
    return cpu_style, ram_style, swap_style
#------

@callback(Output("graph_cpu", 'figure'), Input("timer", 'n_intervals'))
def update_graph(n):
    # Обновление данных в мониторе
    update_df()
    
    # Построение графика
    traces = list()
    for t in df.columns[:CPU_COUNT]:
        traces.append(
            plotly.graph_objs.Line(
                x=df.index,
                y=df[t],
                name=t
            )
        )
    return {"data": traces, "layout": {"template": "plotly_dark"}}

# Коллбэк для обновления графика средней загрузки CPU
@callback(Output("graph_cpu_avg", 'figure'), Input("timer", 'n_intervals'))
def update_cpu_avg_graph(n):
    # Обновление данных в мониторе
    update_df()
    
    # Построение графика средней загрузки CPU
    traces = list()
    traces.append(
        plotly.graph_objs.Line(
            x=df.index,
            y=df['cpu_avg'],
            name='CPU Average'
        )
    )
    return {"data": traces, "layout": {"template": "plotly_dark"}}
#------------------------

# Коллбэк для обновления графика RAM
@callback(Output("graph_ram", 'figure'), Input("timer", 'n_intervals'))
def update_ram_graph(n):
    # Обновление данных в мониторе
    update_df()
    
    # Построение графика
    traces = list()
    traces.append(
        plotly.graph_objs.Line(
            x=df.index,
            y=df['ram'],
            name='RAM',
            yaxes_range=[0, 100]
        )
    )
    return {"data": traces, "layout": {"template": "plotly_dark", "yaxis": {"range": (0, 100)}}}# задаем размер 

# Коллбэк для обновления графика использования SWAP памяти
@callback(Output("graph_swap", 'figure'), Input("timer", 'n_intervals'))
def update_swap_graph(n):
    # Обновление данных в мониторе
    update_df()
    
    # Построение графика использования SWAP памяти
    traces = list()
    traces.append(
        plotly.graph_objs.Line(
            x=df.index,
            y=df['swap'],
            name='SWAP'
        )
    )
    return {"data": traces, "layout": {"template": "plotly_dark", "yaxis": {"range": (0, 100)}}}


# Коллбэк для обновления графика ROM
@callback(Output("graph_rom", 'figure'), Input("timer", 'n_intervals'))
def update_rom_graph(n):
    # Обновление данных в мониторе
    update_df()
    
    # Построение графика
    traces = list()
    traces.append(
        plotly.graph_objs.Line(
            x=df.index,
            y=df['disk_usage'],
            name='ROM'
        )
    )
    #return {"data": traces, "layout": {"template": "plotly_dark"}}
    return {"data": traces, "layout": {"template": "plotly_dark", "yaxis": {"range": (0, 100)}}}

# Коллбэк для обновления графика Network
@callback(Output("network", 'figure'), Output("net_sent", "children"), Input("timer", 'n_intervals'))
def update_network_graph(n):
    # Обновление данных в мониторе
    update_df()
    
    # Построение графика
    traces = list()
    traces.append(
        plotly.graph_objs.Line(
            x=df.index,
            y=df['network_sent'],
            name='Sent'
        )
    )

    traces.append(
        plotly.graph_objs.Line(
            x=df.index,
            y=df['network_received'],
            name='Received'
        )
    )

    return {"data": traces, "layout": {"template": "plotly_dark"}}, f"Total sent: {df.loc[299, 'network_sent'] / (2 ** 20):.2f}"

# Коллбэк для обновления графика сетевых подключений
@callback(Output("graph_connections", 'figure'), Input("timer", 'n_intervals'))
def update_connections_graph(n):
    # Обновление данных в мониторе
    update_df()
    
    # Построение графика сетевых подключений
    traces = list()
    # for conn in df['connections'][-1]:
    #     traces.append(
    #         plotly.graph_objs.Bar(
    #             x=conn.keys(),
    #             y=conn.values(),
    #             name=f"Connection {len(traces)+1}"
    #         )
    #     )
    traces.append(
        plotly.graph_objs.Bar(
            x=list(conections.keys()),
            y=list(conections.values()),
            name=f"Connection {len(traces)+1}"
        )
    )
    return {"data": traces, "layout": {"template": "plotly_dark"}}

if __name__ == "__main__":
    # Обновление данных в мониторе перед запуском приложения
    update_df()
    # Запуск приложения
    dash_app.run_server(debug=True)