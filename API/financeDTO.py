import datetime
from pydantic import BaseModel


class IncomeStatementDTO(BaseModel):
    date: datetime.date
    revenue: float
    netIncome: float
    grossProfit: float
    eps: float
    operatingIncome: float
