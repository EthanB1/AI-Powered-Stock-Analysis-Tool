import os
import logging
from openai import OpenAI
# Load .env environment variables
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

class Gpt:
    def __init__(self):
        self.api_key = os.environ.get("GPT")
        self.client = OpenAI(api_key=self.api_key)

    def _gpt_request(self, prompt_text, max_tokens, temperature=0.7, top_p=1, frequency_penalty=0.5):
        try:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text}
            ]

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                frequency_penalty=frequency_penalty
            )

            if response.choices and response.choices[0].message:
                return response.choices[0].message.content.strip()
            else:
                return "No response from the model."
        except Exception as e:
            logging.error(str(e))
            raise Exception(str(e))

    def analyze_balance_sheet(self, df):
        balance_sheet_str = df.to_string()
        prompt_text = f"Please analyze the following balance sheet data for the last few years:\n\n{balance_sheet_str}\n\nProvide insights on the assets, liabilities, and equity trends, and evaluate if the investing risk has increased in 750 words or less."
        return self._gpt_request(prompt_text, 1000)

    def analyze_income_statement_with_gpt(self, df):
        income_statement_str = df.to_string()
        prompt_text = f"Please analyze the following income statement data for the last few years:\n\n{income_statement_str}\n\nProvide insights on the revenue, expenses, and net income trends, evaluate profit margins and the operational efficiency of the company in 750 words or less."
        return self._gpt_request(prompt_text, 1000)

    def analyze_cash_flows_statement_with_gpt(self, df):
        cash_flows_str = df.to_string()
        prompt_text = f"Please analyze the following cash flows statement data for the last few years:\n\n{cash_flows_str}\n\nProvide insights on the operating, investing, and financing cash flows. Highlight any major changes or trends in cash positions and evaluate the company's ability to generate positive cash flow in 750 words or less."
        return self._gpt_request(prompt_text, 1000)

    def analyze_ratios_with_openai(self, ticker, ratio_df):
        prompt = f"""
            Analyze the financial metrics for the company with ticker symbol {ticker}:

            - P/E Ratio (Price-to-Earnings Ratio) for {ticker}: {ratio_df["metric"]['P/E Ratio']}
            Average P/E Ratio among peers: {ratio_df["Average Metrics Among Peers"]['P/E Ratio']}

            - P/B Ratio (Price-to-Book Ratio) for {ticker}: {ratio_df["metric"]['P/B Ratio']}
            Average P/B Ratio among peers: {ratio_df["Average Metrics Among Peers"]['P/B Ratio']}

            - P/S Ratio (Price-to-Sales Ratio) for {ticker}: {ratio_df["metric"]['P/S Ratio']}
            Average P/S Ratio among peers: {ratio_df["Average Metrics Among Peers"]['P/S Ratio']}

            - Dividend Yield for {ticker}: {ratio_df["metric"]['Dividend Yield']}
            Average Dividend Yield among peers: {ratio_df["Average Metrics Among Peers"]['Dividend Yield']}

            - ROE (Return on Equity) for {ticker}: {ratio_df["metric"]['ROE']}
            Average ROE among peers: {ratio_df["Average Metrics Among Peers"]['ROE']}

            - ROA (Return on Assets) for {ticker}: {ratio_df["metric"]['ROA']}
            Average ROA among peers: {ratio_df["Average Metrics Among Peers"]['ROA']}

            - Debt-to-Equity Ratio for {ticker}: {ratio_df["metric"]['Debt-to-Equity Ratio']}
            Average Debt-to-Equity Ratio among peers: {ratio_df["Average Metrics Among Peers"]['Debt-to-Equity Ratio']}

            - Current Ratio for {ticker}: {ratio_df["metric"]['Current Ratio']}
            Average Current Ratio among peers: {ratio_df["Average Metrics Among Peers"]['Current Ratio']}

            - Quick Ratio for {ticker}: {ratio_df["metric"]['Quick Ratio']}
            Average Quick Ratio among peers: {ratio_df["Average Metrics Among Peers"]['Quick Ratio']}

            - Operating Margin for {ticker}: {ratio_df["metric"]['Operating Margin']}
            Average Operating Margin among peers: {ratio_df["Average Metrics Among Peers"]['Operating Margin']}

            - Gross Margin for {ticker}: {ratio_df["metric"]['Gross Margin']}
            Average Gross Margin among peers: {ratio_df["Average Metrics Among Peers"]['Gross Margin']}

            - Price-to-Cash Flow for {ticker}: {ratio_df["metric"]['Price-to-Cash Flow']}
            Average Price-to-Cash Flow among peers: {ratio_df["Average Metrics Among Peers"]['Price-to-Cash Flow']}

            Considering the above data points and understanding the importance of these metrics in evaluating a company's financial health and performance:

            1. How does the company stand in terms of profitability, liquidity, and solvency compared to its peers?
            2. Are there any alarming disparities or noteworthy strengths in any specific metrics?
            3. What might these metrics indicate about the company's operational efficiency, financial strategies, or market positioning?
            4. Are there potential opportunities or risks that these metrics highlight?

            Please provide a comprehensive analysis of the company's financial standing compared to its peers.
        """
        return self._gpt_request(prompt, 1000)

    def analyze_full_picture(self, financial_data):
        financial_data_str = financial_data.to_string()
        prompt = f"""
            Analyzing a company's complete financial health based on its consolidated financial statements. 
            The data includes the Balance Sheet, Income Statement, and Cash Flow Statement over a period of years. 
            Here are the key figures:\n\n{financial_data_str}\n\n
            Based on this data, provide a comprehensive analysis covering the following points:
            1. Overall financial health and stability of the company.
            2. Key strengths and weaknesses evident from the balance sheet.
            3. Profitability analysis based on the income statement.
            4. Cash flow adequacy and liquidity position.
            5. Trends over the years and any significant changes or anomalies.
            6. Potential risks and investment opportunities.
            7. Summary of the company's financial performance and future outlook.

            Please present the analysis in a clear, structured, and detailed manner in 750 words or less.
        """
        return self._gpt_request(prompt, 1000)
    

    def analyze_portfolio(self, portfolio_details):
        """
        Generate a detailed GPT prompt for portfolio analysis based on FMP API data, financial ratios, and stock weights.

        :param portfolio_details: List of dictionaries containing portfolio data
        :return: GPT-generated analysis as a string
        """
        total_portfolio_value = sum(stock['shares'] * stock['current_price'] for stock in portfolio_details)
        prompt = "Analyze the following stock portfolio, focusing on market position, financial health, risk factors, weight of each stock in the portfolio, and financial ratios: \n\n"

        for stock in portfolio_details:
            stock_value = stock['shares'] * stock['current_price']
            weight = stock_value / total_portfolio_value
            ratios = stock.get('financial_ratios', {})
            ratio_text = "\n".join([f"{key}: {value}" for key, value in ratios.items()])

            prompt += f"Stock: {stock['ticker']} - Shares: {stock['shares']}, Price: {stock['current_price']}, Market Cap: {stock.get('market_cap', 'N/A')}, Sector: {stock.get('sector', 'N/A')}, Beta: {stock.get('beta', 'N/A')}, Weight in Portfolio: {weight:.2%}.\n"
            prompt += f"Financial Ratios:\n{ratio_text}\n\n"

        prompt += "Based on this data, provide a detailed analysis of each stock and the overall portfolio, including diversification, performance, risk profile, and weight distribution. \n\n"
        response = self._gpt_request(prompt, max_tokens=1000)  # Adjust max_tokens as needed

        return response
    
    def handle_follow_up_question(self, question, previous_analysis):
        MAX_TOKENS = 8000
        prompt_intro = "Based on the following portfolio analysis, answer the user's follow-up question:\n\n"
        combined_input = prompt_intro + previous_analysis + "\n\nFollow-up Question: " + question

        if len(combined_input) > MAX_TOKENS:
            start_index = len(combined_input) - MAX_TOKENS
            combined_input = "..." + combined_input[start_index:]

        print("Sending to GPT:", combined_input)  # For debugging

        try:
            response = self._gpt_request(combined_input, max_tokens=250, temperature=0.7, top_p=1, frequency_penalty=0.5)
        except Exception as e:
            response = f"An error occurred: {e}"

        return response

