# pip install -r requirements.txt
# python -m streamlit run index.py
import altair as alt
import pandas as pd
import streamlit as st
import logging

from services.fmp_service import Fmp
from services.gpt_service import Gpt
from services.finnhub_service import Finnhub
from services.polygon_service import Polygon
from services.yfinance_service import YFinance

logging.basicConfig(level=logging.INFO)

# Front page container
with st.container():
    st.markdown("<h1 style='text-align: center;'>AI Powered Stock Analysis</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center;'>
            <p>Welcome to the AI powered stock analysis tool.</p>
        </div>
    """, unsafe_allow_html=True)

def combine_financial_statements(ticker, years):
    fmp_service = Fmp()
    balance_sheet = fmp_service.get_balance_sheet_statement(ticker, years).reset_index()
    income_statement = fmp_service.get_income_statement(ticker, years).reset_index()
    cash_flow = fmp_service.get_cash_flows_data(ticker, years).reset_index()

    # Create demarcation rows (empty rows with a label)
    demarcation = pd.DataFrame([['---' * 10] + [''] * (balance_sheet.shape[1] - 1)], columns=balance_sheet.columns)

    # Vertically stack the dataframes with demarcation rows
    combined_df = pd.concat([balance_sheet, demarcation, income_statement, demarcation, cash_flow], axis=0, ignore_index=True)

    return combined_df

def main():

    selected_tab = st.sidebar.radio("Navigation", ["Stock Fundamental Analysis", "Portfolio Analysis", "News Sentiment Analysis"])

    if selected_tab == "Stock Fundamental Analysis":
        # Display Stock Fundamental Analysis content
        st.header("Stock Fundamental Analysis")
        ticker_search = st.text_input("Ticker:", value="PTON").upper()
        years_search = st.number_input("Years:", value=5, min_value=1, max_value=10)
         # Balance Sheet Analysis
        if st.button("Balance Sheet"):
            try:
                if not years_search or not ticker_search:
                    st.error('"Ticker" and "Years" are mandatory fields')
                else:
                    balance_sheets = Fmp().get_balance_sheet_statement(ticker_search, years_search)
                    st.session_state['balance_sheet_analysis'] = Gpt().analyze_balance_sheet(balance_sheets)
                    st.write(f"### Balance Sheets of {ticker_search}")
                    st.dataframe(balance_sheets)
                    st.divider()
                    st.write("### Analysis")
                    st.write(st.session_state['balance_sheet_analysis'])
            except Exception as err:
                st.error(err)

        # Income Statement Analysis
        if st.button("Income Statement"):
            try:
                if not years_search or not ticker_search:
                    st.error('"Ticker" and "Years" are mandatory fields')
                else:
                    income_statement = Fmp().get_income_statement(ticker_search, years_search)
                    st.write(f"### Income Statement of {ticker_search}")
                    st.dataframe(income_statement)
                    st.divider()
                    st.write("### Analysis")
                    income_statement_analysis = Gpt().analyze_income_statement_with_gpt(income_statement)
                    st.write(income_statement_analysis)
            except Exception as err:
                st.error(err)

        # Cash Flows Analysis
        if st.button("Cash Flows"):
            try:
                if not years_search or not ticker_search:
                    st.error('"Ticker" and "Years" are mandatory fields')
                else:
                    cash_flows = Fmp().get_cash_flows_data(ticker_search, years_search)
                    st.write(f"### Cash Flows of {ticker_search}")
                    st.dataframe(cash_flows)
                    st.divider()
                    st.write("### Analysis")
                    cash_flows_analysis = Gpt().analyze_cash_flows_statement_with_gpt(cash_flows)
                    st.write(cash_flows_analysis)
            except Exception as err:
                st.error(err)

        # Full Financial Picture Analysis
        if st.button("Full Financial Picture"):
            try:
                if not years_search or not ticker_search:
                    st.error('"Ticker" and "Years" are mandatory fields')
                else:
                    combined_financials = combine_financial_statements(ticker_search, years_search)
                    st.write(f"### Combined Financial Statements of {ticker_search}")
                    st.dataframe(combined_financials)
                    st.divider()
                    st.write("### Comprehensive Analysis")
                    full_picture_analysis = Gpt().analyze_full_picture(combined_financials)
                    st.write(full_picture_analysis)
            except Exception as err:
                st.error(err)

        # Ratio Comparison Analysis
        if st.button("Ratio Comparison"):
            try:
                if not ticker_search:
                    st.error('"Ticker" is a mandatory field')
                else:
                    st.write(f"### {ticker_search} Ratio Comparison")
                    ratio_df = Finnhub().get_ratios_for_ticker(ticker_search)
                    peers_df = Finnhub().get_peer_ratios(ticker_search)
                    avg_metrics = pd.DataFrame(data={"Average Metrics Among Peers": peers_df.mean().transpose()}) 
                    ratio_df = pd.concat([ratio_df, avg_metrics], axis=1, join="inner")
                    st.dataframe(ratio_df)
                    st.divider()
                    st.write("### Analysis")
                    analysis_result = Gpt().analyze_ratios_with_openai(ticker_search, ratio_df)
                    st.write(analysis_result)
            except Exception as err:
                st.error(err)


    elif selected_tab == "Portfolio Analysis":
        st.header("Portfolio Analysis")
        #portfolio analysis
        def fetch_portfolio_data(portfolio):
            finnhub_client = Finnhub()
            fmp_client = Fmp()
            yfinance_client = YFinance()

            portfolio_details = []
            for ticker, shares in portfolio:
                # Fetch monthly historical data for the past year
                historical_data = yfinance_client.get_monthly_historical_data(ticker, '2022-01-01', '2023-01-01')
                current_price = historical_data['Close'][-1] if not historical_data.empty else 'N/A'

                # Fetch financial ratios
                financial_ratios = finnhub_client.get_ratios_for_ticker(ticker)

                # Fetch company profile and format it
                company_profile_raw = fmp_client.get_company_profile(ticker)
                company_profile = company_profile_raw.iloc[0].to_dict() if not company_profile_raw.empty else {}

                # Construct the details dictionary for each stock
                stock_details = {
                    'ticker': ticker,
                    'shares': shares,
                    'current_price': current_price,
                    'historical_data': historical_data,
                    'financial_ratios': financial_ratios,
                    'market_cap': company_profile.get('mktCap', 'N/A'),
                    'sector': company_profile.get('sector', 'N/A'),
                    'industry': company_profile.get('industry', 'N/A'),
                    'beta': company_profile.get('beta', 'N/A')
                    # Additional details can be added as needed
                }

                portfolio_details.append(stock_details)

            return portfolio_details


        def portfolio_input():
            st.markdown("Enter your portfolio details below:")

            # Initialize GPT client at the beginning of the function
            gpt_client = Gpt()

            # Check if 'num_stocks' is already in session state
            if 'num_stocks' not in st.session_state:
                st.session_state['num_stocks'] = 5  # Default number of stocks

            # Update the number of stocks based on user input
            num_stocks = st.number_input('Number of Stocks', min_value=1, max_value=10, step=1, key='num_stocks')

            with st.form("portfolio_form"):
                portfolio_data = []
                for i in range(st.session_state['num_stocks']):
                    col1, col2 = st.columns(2)
                    with col1:
                        ticker = st.text_input(f"Stock Ticker {i+1}", key=f"ticker_{i}")
                    with col2:
                        shares = st.number_input(f"Shares {i+1}", min_value=0, key=f"shares_{i}")
                    portfolio_data.append((ticker, shares))

                submitted = st.form_submit_button("Submit")

            if submitted and portfolio_data:
                st.session_state['portfolio'] = portfolio_data
                portfolio_details = fetch_portfolio_data(portfolio_data)
                
                analysis = gpt_client.analyze_portfolio(portfolio_details)
                st.session_state['analysis'] = analysis
                st.write(analysis)

                # Reset follow-up questions
                st.session_state['follow_up_questions'] = []

            # Follow-up question section, appears after analysis
            if 'analysis' in st.session_state:
                follow_up_question = st.text_input("Have any follow-up questions? Ask here:", key="follow_up_question")
                if follow_up_question:
                    follow_up_response = gpt_client.handle_follow_up_question(follow_up_question, st.session_state['analysis'])
                    st.session_state['follow_up_questions'].append((follow_up_question, follow_up_response))
                    st.write(follow_up_response)

        # Display portfolio input form and analysis
        portfolio_input()

    elif selected_tab == "News Sentiment Analysis":
        st.header("News Sentiment Analysis")
        ticker_search = st.text_input("Ticker:", value="PTON").upper()

        def draw_prediction_analisys_chart(sentiment_df):
            # Calculate the total number of each sentiment category
            sentiment_counts = sentiment_df['Predicted Sentiment'].value_counts()
            # Draw the chart
            if sentiment_counts.size > 0:
                data = pd.DataFrame({
                    'Positive': sentiment_df.loc[sentiment_df['Predicted Sentiment'] == "Positive"].value_counts(),
                    'Neutral': sentiment_df.loc[sentiment_df['Predicted Sentiment'] == "Neutral"].value_counts(),
                    'Negative': sentiment_df.loc[sentiment_df['Predicted Sentiment'] == "Negative"].value_counts()
                })
                # Melt the DataFrame to have columns and values
                data_melted = data.melt()
                # Create a color scheme for the columns
                column_color_scheme = {
                    'Positive': 'green',
                    'Neutral': 'blue',
                    'Negative': 'red'
                }
                chart = alt.Chart(data_melted).mark_bar().encode(
                    x=alt.X('variable:N', title='Predicted Sentiment'),
                    y=alt.Y('value:Q', title='Number of Headlines'),
                    color=alt.Color('variable:N', scale=alt.Scale(domain=list(column_color_scheme.keys()), range=list(column_color_scheme.values())))
                )
                # Add a title to the chart
                chart = chart.properties(
                    title='Sentiment Analysis of Headlines',
                    width=600,   # Adjust the width as needed
                    height=600   # Adjust the height as needed
                )
                st.altair_chart(chart)

        news_limit = st.number_input("Number of Headlines:", value=75, min_value=1, max_value=150)
        if st.button("News Sentiment Analysis"):
            try:
                if not ticker_search:
                    st.error('"Ticker" is a mandatory field')
                else:
                    st.write(f"### {ticker_search} News Sentiment Analysis")
                    news_articles = Polygon().get_articles_from_api(ticker_search, news_limit)
                    if not news_articles:
                        raise BaseException("No Articles found.")
                    # make analysis using openapi
                    st.write(f"### Prediction from articles")
                    df_results = Polygon().make_prediction_from_articles(news_articles)
                    st.dataframe(df_results)
                    draw_prediction_analisys_chart(df_results)
            except (Exception, BaseException) as err:
                st.write(err)

if __name__ == "__main__":
    main()
