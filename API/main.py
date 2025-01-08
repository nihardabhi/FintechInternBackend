
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

async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        # Map the necessary data to the DTO as requirement
        return [
            IncomeStatementDTO(date=datetime.strptime(item["date"], "%Y-%m-%d").date(), revenue=item["revenue"], netIncome=item["netIncome"], grossProfit=item["grossProfit"], eps=item["eps"], operatingIncome=item["operatingIncome"])
            for item in data
        ]




@app.on_event("startup")
async def on_startup():
    global fetchedData
    fetchedData = await fetch_data()  # Fetch the data once on app startup





@app.get("/", response_model=List[IncomeStatementDTO])
def get_annual_income():
    return fetchedData




@app.get("/fetch_date_filtered_data/{start_year}/{end_year}", response_model=List[IncomeStatementDTO])
async def get_filtered_data(start_year: int, end_year: Optional[int] = None):
    # Check if end_year is provided when start_year is provided
    if not end_year:
        end_year = start_year  # If no end year provided, set it equal to start year

    # Check if end_year is less than start_year
    if end_year < start_year:
        raise HTTPException(status_code=400, detail="End year cannot be smaller than start year.")
        
    # Filter the data based on the provided start and end year
    filtered_data = [
        item for item in fetchedData
        if start_year <= item.date.year <= end_year  # Directly compare the year attribute
    ]
    
    return filtered_data





@app.get("/fetch_revenue_filtered_data/{start_revenue}/{end_revenue}", response_model=List[IncomeStatementDTO])
async def get_filtered_data(start_revenue: float, end_revenue: float):
    # Check if end_year and start year both provided
    if end_revenue is None or start_revenue is None:
        raise HTTPException(status_code=400, detail="please enter both start or end date revenue")

    # Check if end_year is less than start_year
    if end_revenue < start_revenue:
        raise HTTPException(status_code=400, detail="End revenue cannot be smaller than start revenue.")
    
    # Filter the data based on the provided start and end year
    filtered_data = [
    item for item in fetchedData
        if start_revenue <= item.revenue <= end_revenue  # Directly compare the year attribute
    ]
    
    return filtered_data






@app.get("/fetch_netincome_filtered_data/{start_netincome}/{end_netincome}", response_model=List[IncomeStatementDTO])
async def get_filtered_data(start_netincome: float, end_netincome: float):
    # Check if end_year and start year both provided
    if end_netincome is None or start_netincome is None:
        raise HTTPException(status_code=400, detail="please enter both start or end date revenue")

    # Check if end_year is less than start_year
    if end_netincome < start_netincome:
        raise HTTPException(status_code=400, detail="End revenue cannot be smaller than start revenue.")
    
    # Filter the data based on the provided start and end year
    filtered_data = [
    item for item in fetchedData
        if start_netincome <= item.netIncome <= end_netincome  # Directly compare the year attribute
    ]
    
    return filtered_data






if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
