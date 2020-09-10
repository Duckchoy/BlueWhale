import datetime as dt
from dateutil.relativedelta import relativedelta


class GlobVars:

    def __init__(self):
        self.datawindow = 10
        self.err = '-'
        self.today = dt.datetime.today().date()
        self.history = self.today - relativedelta(years=self.datawindow)

        self.font = "Droid Sans"
        self.oceanblue = '#0077BE'
        self.dollargreen = '#85bb65'

        self.colors = {
            'primary': '#4582ec',
            'secondary': '#02b875',
            'success': '#02b875',
            'info': '#17a2b8',
            'warning': '#f0ad4e',
            'danger': '#d9534f',
            }
