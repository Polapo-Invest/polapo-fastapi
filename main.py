from fastapi import FastAPI, Request
import os
import google.generativeai as genai
from dotenv import load_dotenv
import pandas as pd
import quantstats as qs

from io import BytesIO
import base64
import matplotlib
from PIL import Image
import tempfile

from ETF_Functions import get_ticker_by_company_name, get_etf_price_data
from backtesting_engine import GEMTU772

matplotlib.use('Agg') # Engine reset issue solution code (TkAgg->Agg)

load_dotenv()

genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

# fastapi
app = FastAPI()

@app.get("/")
def test():
    pass

@app.get("/get_ticker")
def get_ticker(company_name: str):
    result = get_ticker_by_company_name(company_name)
    return result

@app.post('/Backtest_result')
async def generate_report(request: Request):
    print("BACKTEST")
    print(request.json())
    print(request.body())
    data = await request.json()
    print(data)

    if data is None:
        return {"error": "No input data provided"}, 400

    cs_model = data.get('cs_model')
    ts_model = data.get('ts_model')
    tickers = data.get('tickers')
    startyear = data.get('startyear')

    if not cs_model or not ts_model:
        return {"error": "Missing model selection"}, 400

    df = get_etf_price_data(tickers, startyear)
    
    engine = GEMTU772(df)
    res = engine.run(cs_model=cs_model, ts_model=ts_model, cost=0.0005)
    port_weights, port_asset_rets, port_rets = res

    port_weights_img, asset_performance_img, portfolio_performance_img = engine.performance_analytics(port_weights, port_asset_rets, port_rets)

    print("============")
    print(res)
    print("=====")
    # print(type(res))
    # print(port_weights_img)
    # print(type(port_weights_img))

    return {
        "port_weights_img": port_weights_img,
        "asset_performance_img": asset_performance_img,
        "portfolio_performance_img": portfolio_performance_img
    }