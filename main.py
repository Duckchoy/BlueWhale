import dash
import dash_bootstrap_components as dbc

# https://fontawesome.com/v4.7.0/icons/
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"

external_stylesheets = [
                        dbc.themes.LITERA,
                        # SPACELAB and YETI are two other styles I like
                        # https://bootswatch.com
                        FONT_AWESOME,
                        ]

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                update_title='Fetching...',
                title="alphadash",
                suppress_callback_exceptions=True
                )

server = app.server