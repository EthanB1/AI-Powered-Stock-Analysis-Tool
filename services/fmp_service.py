import os
import logging
import requests
import pandas as pd
# Load .env environment variables
from dotenv import load_dotenv
load_dotenv()


class Fmp:
    API_KEY = os.getenv("FMP")

    def fetch_and_format_financial_data(self, url):
        # Fetch the data
        logging.info(f"Fetching data from URL: {url}")
        response = requests.get(url)
        data = response.json()

        # Convert the data to a pandas dataframe
        df = pd.DataFrame(data)

        # Drop specific columns and sort
        df = df.drop(columns=['cik', 'link', 'finalLink']).sort_values(by='date')

        # Set the 'date' field as index and transpose
        return df.set_index('date').T

    def get_balance_sheet_statement(self, ticker, years=10):
        url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?apikey={self.API_KEY}&limit={years}"
        return self.fetch_and_format_financial_data(url)
    
    def get_income_statement(self, ticker, years=10):
        url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?apikey={self.API_KEY}&limit={years}"
        return self.fetch_and_format_financial_data(url)
    
    def get_cash_flows_data(self, ticker, years=10):
        url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?apikey={self.API_KEY}&limit={years}"
        return self.fetch_and_format_financial_data(url)
    
    
    def get_company_profile(self, ticker):
        url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={self.API_KEY}"
        logging.info(f"Fetching company profile for ticker: {ticker}")
        response = requests.get(url)
        data = response.json()

        if data:
            return pd.DataFrame(data)
        else:
    # Return an empty DataFrame with specified columns
            return pd.DataFrame(columns=['column1', 'column2'])  # Adjust columns as per your needs


# Example usage
fmp_client = Fmp()
company_profile = fmp_client.get_company_profile('AAPL')
print(company_profile)
