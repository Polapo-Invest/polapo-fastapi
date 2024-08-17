## Setup Virtual Environment

```
pipenv install
```

## Run Development Server

```
uvicorn main:app --reload
```

## API Endpoint

### `/get_ticker/?companyname=회사명`

- get
    - request
        - query parameter로 전달
        - ex) `get_ticker/?company_name=naver`
    - response
        
        ```json
        {
        	"success": true,
        	"ticker": "[company's ticker]",
        }
        ```
        
        ```json
        {
        	"success": false,
        	"message": "Wrong Company Name: [requested company name] (Excluded from calculation)"
        }
        ```
        

### `/generate_html_report`

- post
    - request
        
        ```json
        {
        	"cs_model": "EW",
        	"ts_model": "VT",
        	"tickers": ["AAPL", "NVDA"],
        	"startyear": "2010-01-01"
        }
        ```
        
    - response
        
        ```json
        {
        	"report_html": html file as string type
        }
        ```
        

### `/backtest_result`

- post
    - request body
        
        ```json
        {
        	"cs_model": "EW",
        	"ts_model": "VT",
        	"tickers": ["AAPL", "NVDA"],
        	"startyear": "2010-01-01"
        }
        ```
        
    - response
        
        ```json
        {
        	"port_weights_img": port_weights_img,
          "asset_performance_img": asset_performance_img,
          "portfolio_performance_img": portfolio_performance_img
        }
        ```