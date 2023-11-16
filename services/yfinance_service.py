
import yfinance as yf

class YFinance:
    def get_monthly_historical_data(self, ticker, start_date, end_date):
        stock = yf.Ticker(ticker)
        historical_data = stock.history(start=start_date, end=end_date, interval='1mo')
        return historical_data
