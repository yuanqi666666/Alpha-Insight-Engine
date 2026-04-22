# Alpha Insight Engine: A Quantitative Corporate Financial Analysis Tool
**Alpha Insight Engine** is an automated financial due diligence tool designed for Equity Research Analysts and Portfolio Managers. By integrating directly with the **WRDS (Wharton Research Data Services)** database, the engine transforms raw Compustat quarterly fundamental data into actionable visual insights, bridging the gap between raw database entries and high-level investment decision-making.
## 🚀 Key Features
 * **Multidimensional Financial Perspective**: Automatically extracts and visualizes critical profitability metrics, including ROA, ROE, and ROC.
 * **Automated Risk Surveillance**: Monitors liquidity ratios (Current/Quick Ratios) in real-time and triggers systemic alerts when figures fall below industrial safety thresholds.
 * **Deep Accounting Insights**: Evaluates earnings quality via the **Accrual Ratio** to identify potential distortions between reported net income and actual operating cash flows.
 * **Interactive Analysis Terminal**: Powered by ipywidgets, featuring a user-friendly UI for custom Ticker input and baseline date selection.
 * **Quantitative Risk Metrics**: Computes localized annualized volatility and the **Sharpe Ratio** for the selected post-event period.
## 🛠️ Tech Stack
 * **Data Engine**: wrds (Wharton Research SQL API)
 * **Data Engineering**: Pandas, NumPy
 * **Visualization**: Matplotlib (Synchronized multi-axis rendering)
 * **Interface**: ipywidgets, IPython.display
## 📦 Quick Start
### 1. Prerequisites
Ensure your Python environment is 3.8+ and install the required dependencies:
```bash
pip install wrds pandas matplotlib ipywidgets numpy

```
### 2. Database Authentication
This project requires valid WRDS credentials. Upon execution, the system will prompt for your WRDS username and password to initialize the secure connection.
### 3. Execution
 1. Open the project in a Jupyter environment.
 2. Enter a U.S. Ticker (e.g., NVDA) in the interactive UI.
 3. Select a baseline date and click **"Generate Deep Value Report"**.
## 📊 Core Analytical Logic
The engine utilizes optimized SQL queries to pull raw accounting items from comp.fundq. Key proprietary logic includes:
 * **Earnings Quality**: Calculated as (Net Income - Operating Cash Flow) / abs(Net Income). A ratio < 0.1 is flagged as "High Quality" (Cash-Backed).
 * **Solvency Monitoring**: A hard-coded threshold of Current Ratio < 1.2 is used to trigger liquidity warnings.
 * **Value Simulation**: Leverages the prccq (Price Close - Quarter) field to calculate total shareholder returns since the selected entry point.
## 🤝 Contribution & Feedback
The project is under active development. Suggestions for new analytical models via Issues or Pull Requests are highly encouraged.
