import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

# For encoding local images
import base64

# declaring the layout and server etc
from main import app, server

# import all pages in the app
from apps import backtest, research

# ---------------------------------- #
#         GLOBAL COMPONENTS          #
# ---------------------------------- #

# Navigation Bar
LOGO_IMAGE = base64.b64encode(open('./assets/logo.png', 'rb').read())
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand(
                    html.I(className="fas fa-home fa-1x",
                        style={'color': '#D5F5E3'}
                        ),
                    # html.Img(
                    # src='data:image/png;base64,{}'.format(LOGO_IMAGE.decode()),
                    # height="30px"),
                href="/research"),
            dbc.NavbarToggler(id="navbar-toggler1"),
            dbc.Nav([
                dbc.DropdownMenu(
                        [dbc.DropdownMenuItem("Summary", href="/research"),
                         dbc.DropdownMenuItem("Risk Profile", href="/research"),
                         dbc.DropdownMenuItem("Outlook", href="/research"),
                         dbc.DropdownMenuItem("Fundamentals", href="/research")
                         ],
                     label="Research", nav=True, in_navbar=True),
                dbc.NavItem(dbc.NavLink("Backtest", href="/backtest")),
                dbc.NavItem(dbc.NavLink("Economy", href="/research")),
                dbc.NavItem(dbc.NavLink("Contact", href="/research"))
                ],
                id="navbar-collapse1",
                navbar=True,
            ),
        ]
    ),
    color='success',
    dark=True,
    sticky="top"
)

## we use a callback to toggle the collapse on small screens (later)
# def toggle_navbar_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open
#
# for i in [2]:
#     app.callback(
#         Output(f"navbar-collapse{i}", "is_open"),
#         [Input(f"navbar-toggler{i}", "n_clicks")],
#         [State(f"navbar-collapse{i}", "is_open")],
#     )(toggle_navbar_collapse)

# ---------------------------------- #
#            GLOBAL LAYOUT           #
# ---------------------------------- #

app.layout = html.Div([
    dcc.Location(
        id='url',
        hash='home',
        refresh=False,  # Don't refresh the page when updating location
        ),
    navbar,
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
    )
def display_page(pathname):
    if pathname == '/research':
        return research.layout
    elif pathname == '/backtest':
        return backtest.layout
    # elif pathname == '/economy':
    #     return economy.layout
    # elif pathname == '/contact':
    #     return contact.layout
    else:
        return research.layout

if __name__ == '__main__':
    app.run_server(port=8888,
                   debug=True)
