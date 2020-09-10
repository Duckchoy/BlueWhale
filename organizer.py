import pandas as pd
import yahooquery as yq
from datetime import datetime


def exchange_code(exc_code):
    """
      Convert ICE acronyms to full name of the exchange.

      Parameters:
        exc_code (str): The ICE code for exchange. Must be in upper case.

      Returns:
        str: Full name of the exchange.

    """
    # TODO: Create a dictionary from a file with longer list of global exchanges

    if exc_code == 'NMS':
        return 'NASDAQ'
    elif exc_code == 'NYS':
        return 'New York Stock Exchange'
    elif exc_code == 'NYQ':
        return 'New York Stock Exchange'
    elif exc_code == 'NYO':
        return 'New York Options Exchange'
    elif exc_code == 'CBT':
        return 'Chicago Board of Trade'
    elif exc_code == 'ASE':
        return 'American Stock Exchange'
    elif exc_code == 'MID':
        return 'Chicago Stock Exchange'
    else:
        return '-'


def convert_unit(dollar, significant=2):
    """
      Converts large numbers to the units of Kilo, Millions, Billions, Trillions.

      Parameters:
        dollar (float): a large number that's to be converted
        significant (int): (default: 2) sets the significant place after decimal

      Returns:
        str: a float-string, attached to acronyms: K/ M/ B/ T.

    """

    kilo = 1000.
    million = 1000 * kilo
    billion = 1000 * million
    trillion = 1000 * billion

    num = len(str(dollar))
    if num > 12:
        return str(round(dollar / trillion, significant)) + 'T'
    elif 12 >= num > 9:
        return str(round(dollar / billion, significant)) + 'B'
    elif 9 >= num > 6:
        return str(round(dollar / million, significant)) + 'M'
    else:
        return str(round(dollar / kilo, significant)) + 'K'


def divi_info(df):
    """
      Summary line.

      Extended description of function.

      Parameters:
      arg1 (int): Description of arg1

      Returns:
      int: Description of return value

    """
    div_pct = pd.DataFrame(columns=['FYyy', 'pct_yield'])
    # We are using the Federal Fiscal Year for resampling
    div_pct['pct_yield'] = (100 * df.Dividends / df.Close).resample("A-SEP").sum()
    # Shifting the DateTime by 6 months so the data is plotted at mid-FY (3-31)
    # div_pct.index = div_pct.index.shift(-6, freq='M')
    # Creating a string of 'FY18', 'FY19' etc
    year_string = div_pct.index.strftime('%y')
    div_pct['FYyy'] = 'FY' + year_string
    # The first row removed since it never has all the data for that FY
    div_pct = div_pct[1:]

    df.reset_index(inplace=True)
    df_date = pd.DataFrame(columns=['Date'])
    df_date['Date'] = df['Date'].dt.date

    # If the calendar month is < OCT then remove current FY
    today = datetime.today()
    if int(today.month) < 10:
        div_pct = div_pct[:-1]

    return div_pct, df_date


def regroup_interval(df, interval):
    """
      Summary line.

      Extended description of function.

      Parameters:
      arg1 (int): Description of arg1

      Returns:
      int: Description of return value

    """

    ohlc_dict = {'Open': 'first',
                 'High': 'max',
                 'Low': 'min',
                 'Close': 'last',
                 'Volume': 'sum'}

    if interval == 'W':
        return df.resample('W-Fri').apply(ohlc_dict)  # 'Week ending Friday'
    elif interval == 'M':
        return df.resample('M').apply(ohlc_dict)  # Month ending on 30th or 31st
    else:
        return df


def asset_profile(symb, attribute):
    """
      Summary line.

      Extended description of function.

      Parameters:
      arg1 (int): Description of arg1

      Returns:
      int: Description of return value

    """

    ticker = yq.Ticker(symb)
    profile = getattr(ticker, attribute)
    profile = profile[symb]

    return profile
