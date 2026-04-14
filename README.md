Alpha Insight Engine
Alpha Insight Engine is a professional interactive terminal built with Python and SQL, integrated with the WRDS database. It provides a robust framework for analyzing U.S. equities from 2021 to 2026.
Key Technical Highlights
• Comprehensive Metrics: Visualizes ROA, ROE, ROC, and Liquidity Ratios (Current/Quick) using smoothed trend lines with user-defined entry point markers (Red Dots).
• Automated Diagnostics: Features a logic-driven system providing instant textual insights into a firm’s solvency and profitability.
• Advanced Risk Analysis: Dynamically calculates Annualized Volatility and the Sharpe Ratio for the specific period following the selected date.
• Performance Backtesting: Computes total returns from a chosen historical node to the present, simulating "buy-and-hold" scenarios.
How to Use
1.	Run the first cell to log in using your own WRDS credentials.
2.	Input a ticker (e.g., NVDA) and select a date between 2021 and 2026.
3.	Click "Generate Deep Value Report" to see the full analysis.
Tech Stack: WRDS API, Pandas, Matplotlib, Ipywidgets.