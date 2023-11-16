
# AI-Powered Financial Analysis Application

## Overview
This Streamlit application offers an advanced, AI-driven platform for financial analysis. It's designed to integrate with multiple financial data sources and AI technologies, including OpenAI's GPT models, providing users with deep insights into stock market dynamics, portfolio performance, and news sentiment.

## Installation

### Requirements
- Python 3.x
- Streamlit
- Other dependencies listed in `requirements.txt`

### Steps
To install and run the application:
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Launch the application:
   ```bash
   streamlit run index.py
   ```

## Features

### 1. Fundamental Analysis of Stocks
This section allows users to perform an in-depth analysis of stocks.
- **Ticker Selection:** Choose a stock ticker and set the duration for historical data analysis.
- **Analysis Options:**
  - Balance Sheet: Delve into assets, liabilities, and equity.
  - Income Statement: Review revenue, expenses, and profitability.
  - Comprehensive View: A holistic financial overview.
  - Comparative Ratios: Benchmark against industry peers.
- **Data Sources:** Integrates APIs like Finnhub, YFinance, and Financial Modelling Prep for real-time financial data.

### 2. Portfolio Analysis
Tailored for investors to analyze and optimize their stock portfolio.
- **Input Portfolio:** Enter stock symbols and the number of shares.
- **Data Aggregation:** Collects data on market performance, ratios, and more.
- **AI-Driven Insights:** Utilizes OpenAI's GPT for advanced portfolio analysis, including risk assessment and diversification strategies.

### 3. News Sentiment Analysis
Understand market sentiments through news analysis.
- **Article Fetching:** Select the number of news articles via Polygon API.
- **Sentiment Analysis:** Employs a BERT model (note: due to its size, not included in the GitHub repository) for sentiment classification of news headlines.
- **Visualization:** Graphically represents sentiment trends over time.

## Technical Details
Each service module in the application is tailored for specific data interactions:
- **Finnhub Service:** Fetches stock-specific data and metrics.
- **FMP Service:** Gathers comprehensive financial reports and ratios.
- **GPT Service:** Provides AI-driven textual analysis and insights.
- **Polygon Service:** Sources news articles for sentiment analysis.
- **YFinance Service:** Offers historical stock performance data.

## Usage and Navigation
- **Starting the Application:** Run `streamlit run index.py`.
- **Interface:** User-friendly with clear navigation through different analysis modules.
- **Interactivity:** Interactive widgets for data input and dynamic results display.

