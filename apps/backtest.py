# ---------------------------------- #
#            MODULE IMPORTS          #
# ---------------------------------- #

# Dash components
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# Make my 'app' local
from main import app
from settings import GlobVars

# Importing standard Python modules

# ---------------------------------- #
#           CSS STYLE SHEETS         #
# ---------------------------------- #

myvars = GlobVars()
TODAY = myvars.today
HISTORY = myvars.history

sideBar = {
    'position': 'fixed',
    'top': '45px',
    'bottom': 0,
    'left': '0px',
    'width': '22%',
    'padding': '30px 20px',
    'background-color': '#34495E',
    'box-shadow': '2px 8px 8px #888888',
}

setBalance = {
    'width': '170px',
    'text-align': 'center',
    'border': 'solid 2px',
    'border-radius': '30px',
    'font-size': '17px',
}

dropdownStyle = {
    'width': '90px',
    'border': 'solid 1px',
    'border-radius': '30px',
}

faSymbol = {
    'background-color': 'white',
    'padding': '11px 15px',
    'width': '43px',
    'height': '43px',
    'border': 'solid 2px',
    'border-radius': '50%',
    'color': 'green',
}

# ---------------------------------- #
#           PAGE COMPONENTS          #
# ---------------------------------- #

# Configuring the control panel for backtesting
# Set balance which will be the purchasing limit
set_balance = dbc.FormGroup(
    dbc.Row([
        dbc.Col(
            dbc.Input(
                placeholder="Balance",
                type="text",
                value='10000',
                style=setBalance,
            ),
        ),
        dbc.Col(
            html.I(className="fas fa-dollar-sign fa-1x",
                   style=faSymbol
                   ),
            style={'left': '50px', 'top': '1px'}
        )
    ])
)

# Date pickers
calendars = dbc.FormGroup(
    dbc.Row([
        dbc.Col(
            dcc.DatePickerSingle(
                id='start-date',
                placeholder="Start Date",
                min_date_allowed=HISTORY,
                max_date_allowed=TODAY,
                initial_visible_month=HISTORY,
                date=str(HISTORY),
                display_format='MM/DD/YY',
            ),
            style={'left': '-6px'},
        ),
        dbc.Col(
            dcc.DatePickerSingle(
                id='end-date',
                placeholder="End Date",
                min_date_allowed=HISTORY,
                max_date_allowed=TODAY,
                initial_visible_month=TODAY,
                date=str(TODAY),
                display_format='MM/DD/YY',
            ),
            style={'left': '-12px'},
        )
    ],
        no_gutters=True,
        style={'margin-bottom': '20px'}
    ))

# Time Interval Dropdown
interval_dropdown = dbc.FormGroup(
    dbc.Row([
        dbc.Col(
            dbc.Label("Interval", color='white'),
            style={'top': '7px'},
        ),
        dbc.Col(
            dcc.Dropdown(
                id='test-interval',
                options=[
                    {'label': 'Daily', 'value': 'D'},
                    {'label': 'Weekly', 'value': 'W'},
                    {'label': 'Monthly', 'value': 'M'}],
                value='D',
                clearable=False,
                style=dropdownStyle
            )
        )
    ])
)

# Price Field Dropdown
ohlc_dropdown = dbc.FormGroup(
    dbc.Row([
        dbc.Col(
            dbc.Label("Price Field", color='white'),
            style={'top': '8px'}
        ),
        dbc.Col(
            dcc.Dropdown(
                id='test-field',
                options=[
                    {'label': 'CLOSE', 'value': 'Close'},
                    {'label': 'OPEN', 'value': 'Open'},
                    {'label': 'HIGH', 'value': 'High'},
                    {'label': 'LOW', 'value': 'Low'}],
                value='Close',
                clearable=False,
                style=dropdownStyle
            )
        )
    ])
)

# Strategy Dropdown
sizerule_selector = dbc.FormGroup(
    dbc.Row([
        dbc.Col(
            dbc.Label("Sizing Rule", color='white'),
            style={'top': '8px'}
        ),
        dbc.Col(
            dcc.Dropdown(
                id='sizerule_selector',
                options=[
                    {'label': 'Flat', 'value': 'Flat'},
                    {'label': 'Kelly', 'value': 'Kelly'},
                    {'label': 'More', 'value': 'None'}],
                value='Flat',
                clearable=False,
                style=dropdownStyle
            )
        )
    ])
)

# Benchmark Dropdown
bench_dropdown = dbc.FormGroup(
    dbc.Row([
        dbc.Col(
            dbc.Label("Benchmark", color='white'),
            style={'top': '8px'}
        ),
        dbc.Col(
            dcc.Dropdown(
                options=[
                    {'label': 'S&P 500', 'value': '^GSPC'},
                    {'label': 'Dow', 'value': '^DJI'},
                    {'label': 'NASDAQ', 'value': '^IXIC'},
                    {'label': 'Russell', 'value': '^RUT'},
                ],
                clearable=True,
                id='test-benchmark',
                placeholder='select',
                style=dropdownStyle
            )
        )
    ])
)

# A submit button
submit_button = dbc.FormGroup([
    html.Br(),
    dbc.Button(
        id='submit_button',
        n_clicks=0,
        children='Submit',
        color='danger',
        block=True,
        style={
            'font-size': '17px',
            'font-weight': '600',
        }
    ),
])

# Putting all of them together to form the "control pane"
control_panel = dbc.FormGroup([
    calendars,
    set_balance,
    interval_dropdown,
    ohlc_dropdown,
    sizerule_selector,
    bench_dropdown,
    submit_button
])

# Performance Report and Trade Logs
log_files = dbc.FormGroup([
    html.Br(),
    dbc.Row(
        dbc.Col(
            dbc.Label("Performance", color='white'),
            width=6,
        ),
        justify="center",
    ),
    dbc.Row([
        dbc.Col(
            dbc.Button(
                html.I(className="fas fa-download fa-1x",
                       style={'color': 'white'}
                       ),
                color="info", className="mr-1", outline=True,
            ),
            width='auto',
            style={'left': '10px'}
        ),
        dbc.Col(
            dbc.Button(
                html.I(className="fas fa-external-link-alt fa-1x",
                       style={'color': 'white'}
                       ),
                color="info", className="mr-1", outline=True,
            ),
            width='auto',
        )
    ], justify="center",
    ),
])

# Putting above all together in a sidebar that controls the Parameters
side_bar = html.Div(
    [
        html.H4('Controls',
                style={'textAlign': 'center',
                       'color': 'white'
                       }
                ),
        html.Hr(),
        control_panel,
        log_files,
    ],
    style=sideBar,
)

# Selecting a Stock & Strategy
# Stock picker
stock_pick = dbc.Row([
    dbc.Input(
        type="search",
        id='symbol', name='search',
        placeholder='AAPL',
        value='aapl', bs_size="lg",
        style={
            'height': '43px',
            'width': '100px',
        },
    ),
    dbc.Col(
        html.I(className="fas fa-search fa-1x",
               style={'background-color': 'white'}
               ),
        style={'left': '-50px', 'top': '11px'}
    ),
])

# Strategy Dropdown
strategy_selector = dbc.InputGroup(
    [
        dbc.InputGroupAddon("Strategy", addon_type="prepend"),
        dbc.Select(
            options=[
                {'label': 'Buy and Hold', 'value': 'BH'},
                {'label': 'Dollar Cost Averaging', 'value': 'DCA'},
                {'label': 'Buy low, Sell high', 'value': 'BLSH'},
                {'label': 'Crossing the Moving Average', 'value': 'MAC'},
                {'label': 'Positive/Negative Momentum (RSI)', 'value': 'RSI'},
                {'label': 'Crossing the Bollinger Bands', 'value': 'BBC'},
            ],
            value='BH',
        ),
    ]
),

# Putting them together
stock_strat = dbc.Row(
    [
        dbc.Col(stock_pick,
                width={'size': 2, 'offset': 3},
                style={'left': '50px'}
                ),
        dbc.Col(strategy_selector,
                width=4,
                style={'left': '-50px'}
                ),
        dbc.Col(
            dbc.Button("Run",
                   id="loading-button",
                   color="primary", className="mr-1",
                   style={'font-size': '16px',
                          'font-weight': '600',
                          'width': '100px',
                          'border-radius': '2px',
                          }),
            width=1,
            style={'left': '-15px'},
        ),
        dbc.Col(
            dbc.Button("Abort",
                       color="danger", className="mr-1",
                       style={'font-size': '16px',
                              'font-weight': '600',
                              'width': '100px',
                              'border-radius': '2px',
                              }
                       ),
            width=1,
            style={'left': '-5px'},
        ),
    ],
    no_gutters=True,
    align='center',
)

portfolio_plot = dbc.Container([
                    html.Div(
                        dbc.Spinner(
                            html.Div(id="loading-output"),
                            type="grow",
                            color='primary',
                            # fullscreen=True,
                        ),
                        style={'left': '300px'}
                    )
                ])

progress_bar = html.Div([
    dcc.Interval(id="progress-interval", n_intervals=0, interval=500),
    dbc.Progress(id="progress", striped=True),
]
)

# ---------------------------------- #
#             PAGE LAYOUT            #
# ---------------------------------- #

layout = html.Div(
    [
        side_bar,
        html.Br(),
        stock_strat,
        # dbc.Col(progress_bar,
        #     width=3,
        #     style={'left': '600px', 'top':'300px'})
        portfolio_plot,
    ]
)


# ---------------------------------- #
#             CALLBACKS              #
# ---------------------------------- #

@app.callback(
    [Output("progress", "value"), Output("progress", "children")],
    [Input("progress-interval", "n_intervals")],
)
def update_progress(n):
    # check progress of some background process, in this example we'll just
    # use n_intervals constrained to be in 0-100
    progress = min(n % 110, 100)
    # only add text after 5% progress to ensure text isn't squashed too much
    return progress, f"{progress} %" if progress >= 5 else ""


@app.callback(
    Output("loading-output", "children"), [Input("loading-button", "n_clicks")]
)
def load_output(n):
    import time
    if n:
        time.sleep(1)
        return f"Output loaded {n} times"
    pass
