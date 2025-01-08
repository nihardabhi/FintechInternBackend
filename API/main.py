from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException
import httpx
import uvicorn
from financeDTO import IncomeStatementDTO

app = FastAPI()

key = 'eeLEnvvieQAsZKIsd5OODUmvjW2uXGUr'
url = 'https://financialmodelingprep.com/api/v3/income-statement/AAPL?period=annual&apikey={}'.format(key)

fetchedData = {}

# Fetch data function, returns list of IncomeStatementDTO
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        # Map the necessary data to the DTO as requirement
        return [
            IncomeStatementDTO(
                date=datetime.strptime(item["date"], "%Y-%m-%d").date(),
                revenue=item["revenue"],
                netIncome=item["netIncome"],
                grossProfit=item["grossProfit"],
                eps=item["eps"],
                operatingIncome=item["operatingIncome"]
            )
            for item in data
        ]

# Fetch data on app startup
@app.on_event("startup")
async def on_startup():
    global fetchedData
    fetchedData = await fetch_data()  # Fetch the data once on app startup

# Endpoint to return all income statements
@app.get("/", response_model=List[IncomeStatementDTO])
def get_annual_income():
    return fetchedData

# Endpoint to return filtered data by date range (start year to end year)
@app.get("/fetch_date_filtered_data/{start_year}/{end_year}", response_model=List[IncomeStatementDTO])
async def get_filtered_data(start_year: int, end_year: Optional[int] = None):
    if not end_year:
        end_year = start_year  # If no end year provided, set it equal to start year
    if end_year < start_year:
        raise HTTPException(status_code=400, detail="End year cannot be smaller than start year.")
    # Filter the data by year range
    filtered_data = [
        item for item in fetchedData
        if start_year <= item.date.year <= end_year
    ]
    return filtered_data

# Endpoint to return filtered data by revenue range
@app.get("/fetch_revenue_filtered_data/{start_revenue}/{end_revenue}", response_model=List[IncomeStatementDTO])
async def get_filtered_data(start_revenue: float, end_revenue: float):
    # Check if end_revenue and start_revenue both provided
    if end_revenue is None or start_revenue is None:
        raise HTTPException(status_code=400, detail="Please enter both start and end revenue.")
    if end_revenue < start_revenue:
        raise HTTPException(status_code=400, detail="End revenue cannot be smaller than start revenue.")
    # Filter the data by revenue range
    filtered_data = [
        item for item in fetchedData
        if start_revenue <= item.revenue <= end_revenue
    ]
    return filtered_data

# Endpoint to return sorted data by revenue (ascending or descending)
@app.get("/fetch_sorted_revenue_filtered_data/{sortId}", response_model=List[IncomeStatementDTO])
async def get_sorted_revenue_data(sortId: int):
    if sortId not in [0, 1]:
        raise HTTPException(status_code=400, detail="Please enter a valid sort id (0 for ascending, 1 for descending).")
    # Sort by revenue
    sorted_data = sorted(fetchedData, key=lambda item: item.revenue, reverse=(sortId == 1))
    return sorted_data

# Endpoint to return sorted data by net income (ascending or descending)
@app.get("/fetch_sorted_netincome_filtered_data/{sortId}", response_model=List[IncomeStatementDTO])
async def get_sorted_netincome_data(sortId: int):
    if sortId not in [0, 1]:
        raise HTTPException(status_code=400, detail="Please enter a valid sort id (0 for ascending, 1 for descending).")
    # Sort by net income
    sorted_data = sorted(fetchedData, key=lambda item: item.netIncome, reverse=(sortId == 1))
    return sorted_data

# Endpoint to return filtered data by net income range
@app.get("/fetch_netincome_filtered_data/{start_netincome}/{end_netincome}", response_model=List[IncomeStatementDTO])
async def get_filtered_data_by_netincome(start_netincome: float, end_netincome: float):
    # Check if end_netincome and start_netincome both provided
    if end_netincome is None or start_netincome is None:
        raise HTTPException(status_code=400, detail="Please enter both start and end net income.")
    if end_netincome < start_netincome:
        raise HTTPException(status_code=400, detail="End net income cannot be smaller than start net income.")
    # Filter the data by net income range
    filtered_data = [
        item for item in fetchedData
        if start_netincome <= item.netIncome <= end_netincome
    ]
    return filtered_data

# Run the app using uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
