from fastapi import FastAPI

from ETF_Functions import get_ticker_by_company_name

# fastapi
app = FastAPI()

@app.get("/")
def test():
    pass

@app.get("/get_ticker")
def get_ticker(company_name: str):
    result = get_ticker_by_company_name(company_name)
    return result