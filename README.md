Here are the steps to run the project locally:

Install Python 3.7+.

Create a virtual environment:

Run python -m venv venv to create the environment.

Activate the environment with:

Windows: .\venv\Scripts\activate

macOS/Linux: source venv/bin/activate

Install dependencies with pip install fastapi uvicorn httpx.

Create financeDTO.py with the provided code for IncomeStatementDTO.

Run the app using uvicorn main:app --reload.

Access the app at http://127.0.0.1:8000 in your browser.




Build a financial data filtering app using data from a single API endpoint. The app will fetch
annual income statements for AAPL (Apple) and allow users to filter and analyze key metrics.
