# Importing different DASH components
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# Make the 'app' local
from main import app

# Importing usual Python modules
import datetime as dt
import pandas as pd

# import Yahoo! Finance libraries
import yfinance as yf

# Local Modules
import plotsty as pls
import organizer as oz
from settings import GlobVars


# ---------------------------------- #
#         CONSTANT PARAMETERS        #
# ---------------------------------- #

myvars = GlobVars()
# Display data for this duration
DATA_WINDOW = str(myvars.datawindow) + 'y'
# Error when some information is not available
ERR = myvars.err
# Theme Colors
COLORS = myvars.colors
OCEAN_BOAT = myvars.oceanblue

# Customizing the search bar
searchStyle = {
    'height': '60px',
    'width': '160px',
    'text-align': 'center',
    'border': 'solid 4px',
    'border-radius': '50px',
    'display': 'flex',
    'align-items': 'center',
    'font-size': '35px',
    'font-weight': '600',
    'background-color': '#F4F6F6',
    'box-shadow': '2px 6px 10px #888888',
}

shadowStyle = {'box-shadow': '2px 6px 10px #888888'}

# ---------------------------------- #
#           PAGE COMPONENTS          #
# ---------------------------------- #

# Hidden div inside the app that stores some global variables
ghost_child = html.Div([
    html.Div(id='ticker-data', style={'display': 'none'}),
])

# The Heading
jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.H1("A L P H A D A S H", className="text-center",
                        style={'color': COLORS['success'],
                               'font-family': 'Copperplate',
                               'font-size': '75px'}),
                html.P(
                    "A Stock Research & Analytics Dashboard ",
                    className="text-center",
                    style={'color': '#5D6D7E'}
                ),
            ],
            fluid=True)
    ],
    fluid=True,
    style={'background-image': 'linear-gradient(#D5D8DC, #EAF2F8, white)'}
)

# The search bar
search_bar = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Input(
                type="search",
                id='symbol', name='search',
                placeholder='AAPL',
                value='aapl', bs_size="lg",
                style=searchStyle,
            ),
            width={'size': 'auto', 'offset': 5}
        ),
        dbc.Col(
            html.I(className="fas fa-search fa-1g",
                   style={'background-color': '#F4F6F6'}
                   ),
            style={'left': '-38px', 'top': '20px'}
        ),
    ],
        no_gutters=True,
        justify="center",
    ),
    html.Br(),
    html.Br(),
    html.Hr(),
])

# Company profile summary
website = "https://apple.com"
summary_card = dbc.Container(
    dbc.Card(
        dbc.CardBody([
            html.H4(
                html.A(id='short-name', className="card-title",
                       href=website)
            ),
            html.Hr(),
            html.P(id='sector', className="card-text"),
            html.P(id='industry', className="card-text"),
            html.P(id='summary', className="card-text"),
        ]),
        color="success",
        outline=True,
        style=shadowStyle
    )
)

# Basic information table
info_table = html.Div(
    [
        html.Br(),
        dbc.Table(
            html.Tbody([
                html.Tr([html.Td("Headquarter"), html.Td(id='headquarter')]),
                html.Tr([html.Td("IPO Date"), html.Td(id='ipo-date')]),
                html.Tr([html.Td("Employees"), html.Td(id='employees')]),
                html.Tr([html.Td(id='officer_title'), html.Td(id='officer_name')]),
                html.Tr([html.Td("Market Capital"), html.Td(id='mkt-cap')]),
                html.Tr([html.Td("Market Place"), html.Td(id='exchange')]),
                html.Tr([html.Td("Previous Close"), html.Td(id='prvs-close')]),
                html.Tr([html.Td("Avg Price (50d)"), html.Td(id='avg-price')]),
                html.Tr([html.Td("52 Week low/high"), html.Td(id='low-high')]),
                html.Tr([html.Td("Avg Vol (50d)"), html.Td(id='avg-vol')]),
                html.Tr([html.Td("Previous Vol"), html.Td(id='prvs-vol')]),
            ]),
            bordered=True,
            borderless=True,
            hover=True,
            responsive=True,
            striped=True,
        )]
)

# Dividend Information
divi_chart = dbc.Container(
    dbc.Row(dbc.Col(
        dcc.Loading(
            id="loading-2",
            type="default",
            children=html.Div(
                [dcc.Graph(id="dividend-chart",
                           config={'displayModeBar': False})])
        ),
    )),
    fluid=True,
)

# Configuring the control panel for price chart
# Time Interval Dropdown
interval_dropdown = dbc.FormGroup(
    [
        dbc.Label("Time Interval"),
        html.I(className="fas fa-info-circle fa-1x", id="interval_help",
               style={'color': OCEAN_BOAT, 'padding': '0px 3px'}
               ),
        dbc.Tooltip("Each point on the horizontal axis represents a"
                    " time unit-Day, Week, Month, etc."
                    " E.g., each point or bar in a Weekly chart has price"
                    " information from Monday through Friday.",
                    target="interval_help"),
        dcc.Dropdown(
            id='interval',
            options=[
                {'label': 'Daily', 'value': 'D'},
                {'label': 'Weekly', 'value': 'W'},
                {'label': 'Monthly', 'value': 'M'}],
            value='D',  # default value is 'D'
            clearable=False
        )
    ])

# Price Field Dropdown
ohlc_dropdown = dbc.FormGroup(
    [
        dbc.Label("Price Field"),
        html.I(className="fas fa-info-circle fa-1x", id="field_help",
               style={'color': OCEAN_BOAT, 'padding': '0px 3px'}
               ),
        dbc.Tooltip("A time interval (day, week etc.) or a bar has four"
                    "  price fields. Closing price is a typical representation "
                    "of the price corresponding to that interval or bar.",
                    target="field_help"),
        dcc.Dropdown(
            id='field',
            options=[
                {'label': 'CLOSE', 'value': 'Close'},
                {'label': 'OPEN', 'value': 'Open'},
                {'label': 'HIGH', 'value': 'High'},
                {'label': 'LOW', 'value': 'Low'}],
            value='Close',  # default value is 'Close'
            clearable=False)
    ])

# Benchmark Dropdown
bench_dropdown = dbc.FormGroup(
    [
        dbc.Label("Benchmark"),
        html.I(className="fas fa-info-circle fa-1x", id="bench_help",
               style={'color': OCEAN_BOAT, 'padding': '0px 3px'}
               ),
        dbc.Tooltip("A broad market index",
                    target="bench_help"),
        dcc.Dropdown(
            options=[
                {'label': 'S&P 500', 'value': '^GSPC'},
                {'label': 'Dow Jones', 'value': '^DJI'},
                {'label': 'NASDAQ', 'value': '^IXIC'},
                {'label': 'Russell', 'value': '^RUT'},
            ],
            clearable=True,
            id='benchmark')
    ])

# Chart Style Radioitems
plotype_radioitems = dbc.FormGroup(
    [
        dbc.Label("Chart Style"),
        html.I(className="fas fa-info-circle fa-1x", id="chartstyle_help",
               style={'color': OCEAN_BOAT, 'padding': '0px 3px'}
               ),
        dbc.Tooltip("'Line' chart plots a single field, such as closing price. "
                    "'Candles' compactify all four fields into one bar. "
                    "Red & Green color encode up & down price movement"
                    " for that time interval.",
                    target="chartstyle_help"),
        dbc.RadioItems(
            options=[
                {"label": "Lines", "value": True},
                {"label": "Candles", "value": False}
            ],
            value=True,
            id="plotype",
            inline=True,
        ),
    ]
)

# Moving Average checklist
sma_checklist = dbc.FormGroup(
    [
        dbc.Label("Moving Average"),
        html.I(className="fas fa-info-circle fa-1x", id="sma_help",
               style={'color': OCEAN_BOAT, 'padding': '0px 3px'}
               ),
        dbc.Tooltip("A smoother representation of the price movement."
                    " Obtained by averaging the price over 50 or 200 bars.",
                    target="sma_help"),
        dbc.Checklist(
            options=[
                {"label": "50", "value": 50},
                {"label": "200", "value": 200}
            ],
            value=[],
            id="sma",
            inline=True,
        ),
    ]
)

# Volume Switch
vol_switch = dbc.FormGroup([
    dbc.Row([
        dbc.Checklist(
            options=[
                {"label": "Volume", "value": 1}
            ],
            value=[0],
            id="volume",
            switch=True,
        ),
        html.I(className="fas fa-info-circle fa-1x", id="vol_help",
               style={'color': OCEAN_BOAT, 'padding': '3px 3px'}
               ),
        dbc.Tooltip("Total number of shares traded on a selected "
                    "time interval. A volume moving average over "
                    "50 bars is drawn as a line.",
                    target="vol_help"),
    ])
])

# Holiday switch
holiday_switch = dbc.FormGroup([
    dbc.Row([
        dbc.Checklist(
            options=[
                {"label": "Holidays", "value": 1, "disabled": True}
            ],
            value=[1],
            id="holiday",
            switch=True,
        )
    ])
])

# Putting all of them together to form the "control pane" for price chart
control_panel = dbc.Container([
    html.Br(),
    dbc.Row([
        dbc.Col(interval_dropdown, width=2, lg=2),
        dbc.Col(ohlc_dropdown, width=2, lg=2),
        dbc.Col(bench_dropdown, width=2, lg=2),
        dbc.Col(plotype_radioitems, width=2, lg=2),
        dbc.Col(sma_checklist, width=2, lg=2),
        dbc.Col([vol_switch, holiday_switch], width=2, lg=2),
    ], justify='between',
    ),
],
    style={
        'background-color': '#F8F9F9',
        'box-shadow': '2px 6px 10px #888888',
    }
)

# The price chart
price_chart = dbc.Container([
    dbc.Row(
        dbc.Col(
            dcc.Loading(
                id="loading-1",
                type="default",
                children=html.Div([
                    dcc.Graph(id="ohlc-chart",
                              config={'displayModeBar': False})
                ])
            ),
        ),
        style={'margin-top': '15px'},
    ),
],
    fluid=True
)

# Title and graph control tips
graph_controls = dbc.Row(
    dbc.DropdownMenu(
        label="Controls",
        children=[
            dbc.DropdownMenuItem("'select + drag' to zoom-in"),
            dbc.DropdownMenuItem("'shift + drag' to pan adjust"),
            dbc.DropdownMenuItem("'double-click' to zoom out"),
        ],
        direction="up",
        color="light",
        bs_size="sm",
        style={'border-radius': '0%'},
    ),
    justify='center',
    no_gutters=True,
)

# ---------------------------------- #
#             PAGE LAYOUT            #
# ---------------------------------- #

layout = html.Div([
    ghost_child,
    jumbotron,
    search_bar,
    summary_card,
    html.Br(),
    dbc.Container(
        dbc.Row([
            dbc.Col(info_table, width=5),
            dbc.Col(divi_chart, width=7),
        ])
    ),
    html.Br(),
    graph_controls,
    control_panel,
    price_chart,
])


# ---------------------------------- #
#             CALLBACKS              #
# ---------------------------------- #


@app.callback([
    Output('sector', 'children'), Output('industry', 'children'),
    Output('summary', 'children'), Output('employees', 'children'),
    Output('officer_title', 'children'), Output('officer_name', 'children'),
    Output('headquarter', 'children'),
], [
    Input('symbol', 'value')]
)
def asset_summary(symb):
    profile = oz.asset_profile(symb, 'asset_profile')

    sector = 'Sector: ' + profile.get('sector', ERR)
    industry = 'Industry: ' + profile.get('industry', ERR)

    summary = profile.get('longBusinessSummary', ERR)

    employees = profile.get('fullTimeEmployees', ERR)
    officer = profile.get('companyOfficers', [{}])[0]
    officer_title = officer.get('title', ERR)
    officer_age = str(officer.get('age', '-'))
    officer_name = officer.get('name', ERR) + ' (' + officer_age + ')'
    headquarter = profile.get('city', ERR) + ', ' + profile.get('state', '')

    return sector, industry, summary, employees, officer_title, officer_name, headquarter


@app.callback([
    Output('mkt-cap', 'children'), Output('avg-vol', 'children'),
    Output('prvs-vol', 'children'), Output('prvs-close', 'children'),
    Output('avg-price', 'children'), Output('low-high', 'children'),
], [
    Input('symbol', 'value')]
)
def price_summaries(symb):
    summary = oz.asset_profile(symb, 'summary_detail')
    mkt_cap = '$' + oz.convert_unit(summary.get('marketCap', 0))
    avg_vol = oz.convert_unit(summary.get('averageVolume', 0))
    prvs_vol = oz.convert_unit(summary.get('volume', 0))
    prvs_close = '$' + str(summary.get('previousClose', ERR))
    avg_price = '$' + str(round(summary.get('fiftyDayAverage', ERR), 2))
    low = '$' + str(summary.get('fiftyTwoWeekLow', ERR))
    high = '$' + str(summary.get('fiftyTwoWeekHigh', ERR))
    low_high = str(low) + '/' + str(high)

    return mkt_cap, avg_vol, prvs_vol, prvs_close, avg_price, low_high


@app.callback([
    Output('short-name', 'children'), Output('exchange', 'children'),
    Output('ipo-date', 'children')],
    [Input('symbol', 'value')]
)
def quote_type(symb):
    profile = oz.asset_profile(symb, 'quote_type')
    short_name = profile.get("shortName", ERR)
    exchange = oz.exchange_code(profile.get("exchange", ERR))

    # The IPO date is converted to string of the form 'MM DD, YYYY'
    ipo_ = profile.get('firstTradeDateEpochUtc')
    ipo_date_ = dt.datetime.strptime(ipo_, '%Y-%m-%d %H:%M:%S').date()
    ipo_date = dt.datetime.strftime(ipo_date_, "%b %d, %Y")

    return short_name, exchange, ipo_date


@app.callback(
    Output('ticker-data', 'children'),
    [Input('symbol', 'value')]
)
def clean_data(symb):
    ticker = yf.Ticker(symb)
    ohlc = ticker.history(period=DATA_WINDOW)

    # Serialize the output at JSON for faster global callbacks.
    ohlc_json = ohlc.to_json(orient='table')
    # This data is saved in the hidden div in the app.
    # 'table' orientation preserves the DateTime format.

    return ohlc_json


@app.callback(
    Output('ohlc-chart', 'figure'),
    [Input(component_id='symbol', component_property='value'),
     Input(component_id='ticker-data', component_property='children'),
     Input(component_id='field', component_property='value'),
     Input(component_id='benchmark', component_property='value'),
     Input(component_id='interval', component_property='value'),
     Input(component_id='plotype', component_property='value'),
     Input(component_id='sma', component_property='value'),
     Input(component_id='volume', component_property='value')]
)
def price_update(symb, ticker, field, benchmark, interval, ptyp_bool, sma_bool, vol_bool):
    ohlc = pd.read_json(ticker, orient='table')

    ohlc = oz.regroup_interval(ohlc, interval)
    # Re-write this to include 'hourly' and 'Benchmark'

    fig = pls.ohlc_chart(
        symb.upper(), ohlc, field, ptyp_bool, sma_bool, vol_bool
    )
    return fig


@app.callback(
    Output('dividend-chart', 'figure'),
    [Input(component_id='ticker-data', component_property='children')]
)
def dividend_info(ticker):
    ohlc = pd.read_json(ticker, orient='table')

    divi_per_share = ohlc[ohlc.Dividends != 0]

    if divi_per_share.empty:
        return {
            "layout": {
                "xaxis": {"visible": False},
                "yaxis": {"visible": False},
                "annotations": [{
                    "text": "Does not pay dividend",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 20}
                }]
            }
        }
    else:
        return pls.div_chart(divi_per_share)
