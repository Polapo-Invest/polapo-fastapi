import yfinance as yf
import yahooquery as yq
import json

def get_ticker_by_company_name(company_name):
    search = yq.search(company_name)
    quotes = search.get('quotes', [])
    
    if not quotes:
        result = json.dumps({'success':False, 'message':f"Wrong Company Name: {company_name} (Excluded from calculation)"})
        print(result)
        return result
    
    # Returning the first result
    ticker = quotes[0].get('symbol')
    print(ticker)
    result = json.dumps({'success': True, 'ticker':ticker})
    print(result)
    return result