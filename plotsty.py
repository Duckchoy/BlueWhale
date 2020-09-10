import plotly.graph_objects as go
# import plotly.express as px
from plotly.subplots import make_subplots

import logging as log

# local function
import organizer as oz
from settings import GlobVars


# ---------------------------------- #
#            LOGGER SETUP            #
# ---------------------------------- #

logger = log.getLogger(__name__)
logger.setLevel(log.WARNING)
file_handler = log.FileHandler('logfile.log')
formatter = log.Formatter(
    '[%(asctime)s] ! %(levelname)s ! [%(filename)s: line %(lineno)d] %(message)s'
    )
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# ---------------------------------- #
#         CONSTANT PARAMETERS        #
# ---------------------------------- #

myvars = GlobVars()
SET_FONT = myvars.font

BKG_COLOR = 'rgba(236, 239, 241, 0.7)'


# ---------------------------------- #
#          PLOTTING FUNCS            #
# ---------------------------------- #

# DEF: Customization of the OHLC chart
def ohlc_chart(symb, df, field, ptyp_bool, sma_bool, vol_bool):
    df.reset_index(inplace=True)
    df['Date'] = df['Date'].dt.date

    vol_show = True if vol_bool[-1] == 1 else False

    # Passing the MA options, not doing it the best way though :(
    if len(sma_bool) == 0:
        show50, show200 = False, False
    elif len(sma_bool) == 2:
        show50, show200 = True, True
    else:
        if sma_bool[0] == 50:
            show50, show200 = True, False
        else:
            show50, show200 = False, True

    df_round = round(df, 2)

    hovertext = []
    for i in range(len(df)):
        hovertext.append(
            # 'Date: '+str(df['Date'][i]) +
            'Open: $' + str(df_round['Open'][i]) +
            '<br>High: $' + str(df_round['High'][i]) +
            '<br>Low: $' + str(df_round['Low'][i]) +
            '<br>Close: $' + str(df_round['Close'][i])
        )

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Watermarking the stock ticker
    fig.add_annotation(
        xref='paper', yref='paper',
        text=symb, showarrow=False,
        font=dict(family=SET_FONT, size=70),
        align="center",
        opacity=0.2,
        clicktoshow=False)

    # Price chart: Candlestick
    fig.add_trace(
        go.Candlestick(x=df['Date'],
                       open=df['Open'],
                       high=df['High'],
                       low=df['Low'],
                       close=df['Close'],
                       name='Candles',
                       text=hovertext,
                       hoverinfo='x+text',
                       visible=not ptyp_bool,
                       showlegend=False),
        secondary_y=True)

    # Price chart
    fig.add_trace(
        go.Scatter(x=df['Date'], y=df[field],
                   mode='lines',
                   name=field + ' Price',
                   line=dict(color='#27AE60', width=2.5),
                   text=hovertext,
                   textposition='top left',
                   hoverinfo='x+text',
                   visible=ptyp_bool,
                   showlegend=False),
        secondary_y=True)

    # 200-day Simple Moving Average
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=round(df[field].rolling(200).mean(), 2),
                   name='Mov. Av. (200d)',
                   hoverinfo='x',
                   hovertemplate='MA200: %{y:$.1f}<extra></extra>',
                   line=dict(color='rgb(13, 71, 161)', width=1.8),
                   showlegend=False,
                   visible=show200
                   ),
        secondary_y=True)

    # 50-day Simple Moving Average
    fig.add_trace(
        go.Scatter(x=df['Date'],
                   y=round(df[field].rolling(50).mean(), 2),
                   name='Mov. Av. (50d)',
                   hoverinfo='x',
                   hovertemplate='MA50: %{y:$.1f}<extra></extra>',
                   line=dict(color='rgb(229, 57, 53)', width=1.5),
                   showlegend=False,
                   visible=show50
                   ),
        secondary_y=True)

    # Volume chart
    fig.add_trace(
        go.Bar(x=df['Date'], y=df_round['Volume'],
               name="Volume",
               marker_color='rgba(179, 157, 219, 0.8)',
               hoverinfo='x',
               hovertemplate='Vol: %{y:.3s}<extra></extra>',
               showlegend=False,
               visible=vol_show
               ),
        secondary_y=False)

    # 50-day Simple Moving Average of Volume
    fig.add_trace(
        go.Scatter(x=df['Date'], y=round(df['Volume'].rolling(50).mean(), 2),
                   name='Vol. Av. (50d)',
                   hoverinfo='x',
                   hovertemplate='Vav: %{y:.3s}<extra></extra>',
                   line=dict(color='#330099', width=1.8),
                   opacity=0.4,
                   showlegend=False,
                   visible=vol_show
                   ),
        secondary_y=False)

    # y-axis properties: 'primary_y' is Volume & 'secondary_y' is Price.
    fig.update_yaxes(secondary_y=True,
                     zeroline=False,
                     showticklabels=True,
                     tickformat='$',
                     showspikes=True,
                     spikethickness=1.2, spikecolor='slategray',
                     spikemode='across', spikesnap="cursor",
                     showline=True,
                     linewidth=1.0, linecolor='black',
                     showgrid=True,
                     gridcolor='rgba(120, 144, 156, 0.2)',
                     )

    fig.update_yaxes(secondary_y=False,
                     title_text=None,
                     showline=True,
                     linewidth=1.0, linecolor='black',
                     zeroline=False,
                     showticklabels=False,
                     showgrid=False,
                     )

    # Hide holidays
    # this is a bit tricky, hiding weekends is causing gaps in monthly chart
    # one needs to grab market calendar for each year as well
    # check this: https://stackoverflow.com/questions/33094297/create-trading-holiday-calendar-with-pandas
    # fig.update_xaxes(
    #         rangebreaks=[
    #             dict(bounds=["sat", "mon"]), #hide weekends
    #             ])

    fig.update_xaxes(
        showgrid=False,
        showline=True,
        linewidth=1.0, linecolor='black', mirror=True,
        rangeslider_visible=False,
        rangeselector=dict(
            x=0.33,
            buttons=list([
                dict(count=7, label="1W", step="day", stepmode="backward"),
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(count=3, label="3Y", step="year", stepmode="backward"),
                dict(label="10Y", step="all")
            ])
        ))

    fig.update_layout(
        height=550,
        plot_bgcolor=BKG_COLOR,
        font_family=SET_FONT,
        font_size=16,
        margin=dict(t=60, r=50)
    )

    return fig


# DEF: Customization of the Dividend Yield chart
def div_chart(df):

    # try:
    #     df = df.set_index('Date')
    # except KeyError:
    #     logger.error('A Major error has happened.')
    #     logger.exception("That Stupid Problem")

    div_pct, df_date = oz.divi_info(df)

    annotate_fy = []
    for i in range(len(div_pct)):
        annotate_fy.append('{0}: {1}%'.format(
            str(div_pct['FYyy'][i]),
            str(round(div_pct['pct_yield'][i], 2)
                )
            )
        )

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=div_pct.index, y=div_pct['pct_yield'],
            name="DPS",
            texttemplate=annotate_fy,
            textposition="top center",
            showlegend=False,
            hoverinfo='none',
            mode='markers+lines+text',
            marker=dict(
                color='#0645AD',
                opacity=1,
                size=13,
                line=dict(
                    color='#27AE60',
                    width=3)
            ),
            line=dict(color='#27AE60', width=2.5),
        ),
        secondary_y=True,
    )

    hovertext = []
    for i in range(len(df)):
        hovertext.append(
            'Issued On: ' + str(df_date['Date'][i]) +
            '<br>Yield/Share: $' + str(
                round(df['Dividends'][i], 2))
        )

    fig.add_trace(
        go.Bar(
            x=df['Date'], y=round(df['Dividends'], 2),
            text=hovertext,
            hoverinfo='text',
            marker=dict(
                color='#0645AD',
                opacity=0.4,
                line=dict(
                    color='#E53935',
                    width=3)
            ),
            showlegend=False),
        secondary_y=False,
    )

    fig.update_xaxes(
        showgrid=True,
        showline=True,
        linewidth=1.0, linecolor='black', mirror=True,
        rangeslider_visible=False,
        rangeselector=dict(
            x=0.33,
        ))

    fig.update_yaxes(secondary_y=True,
                     zeroline=False,
                     showticklabels=False,
                     showline=True,
                     linewidth=1.0, linecolor='black',
                     showgrid=False,
                     )

    fig.update_yaxes(secondary_y=False,
                     title_text=None,
                     showline=True,
                     linewidth=1.0, linecolor='black',
                     zeroline=False,
                     showticklabels=True,
                     tickformat='$.2f',
                     showgrid=False,
                     )

    fig.update_layout(
        height=550,
        font_family=SET_FONT,
        font_size=16,
        bargap=0.9,
        title='Dividend History',
        plot_bgcolor='rgba(236, 239, 241, 0.7)',
        margin=dict(r=0, t=90, l=0, b=45)
    )

    return fig
