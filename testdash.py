import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import pandas_datareader.data as web
import pandas_datareader as pdr
import datetime

app = dash.Dash()

app.layout = html.Div(children=[
    html.Div(children='''
        Stock Symbol: '''),
    dcc.Input(id='input', value='', type='text'),
    html.Div(id='output-graph'),
])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
    )

def update_value(input_data):
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime.now()
    df = pdr.get_data_yahoo(input_data, start, end)
    df.reset_index(inplace=True)
    df['Date'] = df['Date'].dt.date

    return dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df.Date, 'y': df.Close, 'type': 'line', 'name': input_data},
            ],
            'layout': {
                'title': input_data
            }
        }
    )

if __name__ == '__main__':
    app.run_server(debug=True)
