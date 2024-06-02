import os
from dotenv import load_dotenv
import httpx
load_dotenv()
from io import StringIO
import time
import asyncio
from fudstop.apis.webull.trade_models.news import NewsItem
import pandas as pd
from mktdata.optionsdata import OptionsData
from fudstop.apis.webull.webull_trading import WebullTrading

from fudstop.apis.webull.webull_markets import WebullMarkets
from fudstop.apis.oic.oic_sdk import OICSDK
from fudstop.apis.occ.occ_sdk import occSDK
from fudstop.apis.polygonio.polygon_database import PolygonDatabase
from fudstop._markets.list_sets.ticker_lists import most_active_tickers
from datetime import datetime, timedelta
import pytz

import matplotlib.pyplot as plt
import numpy as np
class StockData:
    def __init__(self):
        self.occ=occSDK(host='localhost', user='chuck', password='fud', port=5432, database='market_data')
        self.markets = WebullMarkets(host='localhost', user='chuck', password='fud', port=5432, database='market_data')
        self.db =  PolygonDatabase(host='localhost', user='chuck', password='fud', port=5432, database='market_data')
        self.trading = WebullTrading()
        self.oic = OICSDK()
        self.optdata = OptionsData()
        self.headers = {
            "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            "Accept-Encoding": os.environ.get('ACCEPT_ENCODING', 'gzip, deflate, br, zstd'),
            "Accept-Language": 'en-US,en;q=0.9',
            "Access-Token": os.environ.get('ACCESS_TOKEN', 'dc_us_tech1.18f756afb8d-c4f928f23fa74e7cbe55c8f3fd57e7e3'),
            "App": os.environ.get('APP', 'global'),
            "App-Group": os.environ.get('APP_GROUP', 'broker'),
            "AppID": os.environ.get('APPID', 'wb_web_app'),
            "Device-Type": os.environ.get('DEVICE_TYPE', 'Web'),
            "DID": os.environ.get('DID', 'gldaboazf4y28thligawz4a7xamqu91g'),
            "HL": os.environ.get('HL', 'en'),
            "Content-Type": os.environ.get('CONTENT_TYPE', 'application/json'),
            "Locale": os.environ.get('LOCALE', 'eng'),
            "Origin": os.environ.get('ORIGIN', 'https://app.webull.com'),
            "OS": os.environ.get('OS', 'web'),
            "PH": os.environ.get('PH', 'Windows Chrome'),
            "Platform": os.environ.get('PLATFORM', 'web'),
            "Priority": os.environ.get('PRIORITY', 'u=1, i'),
            "Referer": os.environ.get('REFERER', 'https://app.webull.com/'),
            "ReqID": os.environ.get('REQID', '07d36b39af6242da92808985d8636217'),
            "T-Time": os.environ.get('T_TIME', '1715662035135'),
            "TZ": os.environ.get('TZ', 'America/Chicago'),
            "Ver": os.environ.get('VER', '4.6.3'),
            "X-S": os.environ.get('X_S', '56766c7a71c1a81a0c1e8a1927dbd15eb3043da89cd608c46d29658ccfda33f5'),
            "X-SV": os.environ.get('X_SV', 'xodp2vg9')
        }




    async def batch_insert(self, table_name:str, df: pd.DataFrame, unique_columns) -> pd.DataFrame:
        await self.db.connect()

        await self.db.batch_insert_dataframe(df, table_name, unique_columns)

        return df
    


    async def short_interest(self, ticker:str='AAPL'):
        try:
            data = await self.trading.get_short_interest(ticker)
            df = data.df
            df['symbol'] = ticker

            
            await self.batch_insert(df=data.df, table_name='short_interest', unique_columns='symbol')
      

            return data
        except Exception as e:
            print(e)

    async def analyst_ratings(self, ticker:str='AAPL'):
        try:
            data = await self.trading.get_analyst_ratings(ticker)

            df = data.df
            df['symbol'] = ticker

            await self.batch_insert(df=data.df, table_name='analysts', unique_columns='symbol')

        except Exception as e:
            print(e)

    async def balance_sheet(self, ticker:str='AAPL'):
        try:
            data = await self.trading.balance_sheet(ticker)
        
            df = data.df
            df['symbol'] = ticker

            await self.batch_insert(df=data.df, table_name='balance_sheet', unique_columns='symbol')
            return data
        except Exception as e:
            print(e)

    async def cost_distribution(self, ticker:str='AAPL'):
        try:
            data = await self.trading.cost_distribution(ticker)
        
            df = data.df
            df['symbol'] = ticker

            await self.batch_insert(df=data.df, table_name='cost_dist', unique_columns='symbol')
            return data
        except Exception as e:
            print(e)


    async def cash_flow(self, ticker:str='AAPL'):
        try:
            data = await self.trading.cash_flow(ticker)

            df = data.df
            df['symbol'] = ticker

            await self.batch_insert(df=data.df, table_name='cash_flow', unique_columns='symbol')
            return data
        except Exception as e:
            print(e)

    async def income_statement(self, ticker:str='AAPL'):
        try:
            data = await self.trading.income_statement(ticker)
            data
            df = data.df
            df['symbol'] = ticker

            await self.batch_insert(df=data.df, table_name='income_statement', unique_columns='symbol')
            return data
        except Exception as e:
            print(e)



    async def etf_holdings(self, ticker:str='AAPL'):
        try:
            data = await self.trading.etf_holdings(ticker, pageSize='50')
  
            df = data.df
            df['symbol'] = ticker

            await self.batch_insert(df=data.df, table_name='etfs', unique_columns='symbol')
            return data
        except Exception as e:
            print(e)



    async def inst_holdings(self, ticker:str='AAPL'):
        try:
            data = await self.trading.institutional_holding(ticker)
            shares_lost = data.decrease.holding_count_change
            shares_gained = data.increase.holding_count_change
            net_amt = shares_lost + shares_gained
            decrease_in_institutions = data.decrease.institutional_count
            increast_in_institutions = data.increase.institutional_count
            df = data.as_dataframe
            df['symbol'] = ticker
            df['net'] = net_amt

            await self.batch_insert(df=df, table_name='inst', unique_columns='symbol')
            return data
        except Exception as e:
            print(e)


    async def quote(self, ticker:str='AAPL'):
        try:
            data = await self.trading.get_stock_quote(symbol='AAPL')
            data['ticker'] = ticker


            await self.batch_insert(df=data, table_name='inst', unique_columns='symbol')
            return data
        except Exception as e:
            print(e)        


    async def order_flow(self, ticker:str='AAPL'):
        try:

            data= await self.trading.order_flow(ticker, count='800')

            df = data.order_df
            df.to_csv('gme_flow.csv')
            df['symbol'] = ticker
            
            await self.batch_insert(df=df, table_name='order_flow', unique_columns='symbol')

            return data
        except Exception as e:
            print(e)


    async def stock_info(self, ticker:str='AAPL', as_dataframe:bool=True):
        try:
            data = await self.occ.stock_info(ticker, as_dataframe=as_dataframe)


            data['symbol'] = ticker
            data = data.drop(columns=['update_date'])
            await self.db.batch_insert_dataframe(data, table_name='info', unique_columns='symbol')

            print(data)
            return data
        except Exception as e:
            print(e)

    async def scan_for_call_options(self, ticker: str='AAPL'):
        try:
            # Fetch stock info
            stock_data = await self.stock_info(ticker)
            
            # Extract necessary attributes
            price = stock_data.price
            iv30 = stock_data.ivx30
            iv30_change = stock_data.ivx30Chg
            call_vol = stock_data.callVol
            change_percent = stock_data.changePercent
            sentiment = stock_data.sentiment
            beta = stock_data.beta120D
            hv30 = stock_data.hv30
            
            # Define conditions for a bullish call option signal
            conditions = [
                iv30 < np.mean([stock_data.ivx7, stock_data.ivx14, stock_data.ivx21]),  # IV lower than recent average
                iv30_change > 0,  # IV is increasing
                call_vol > np.mean([stock_data.optVol, stock_data.stockVol]),  # High call volume
                change_percent > 0,  # Positive price change
                sentiment > 0.5,  # Positive sentiment
                beta > 1,  # High beta indicating higher market volatility
                hv30 < np.mean([stock_data.hv10, stock_data.hv20])  # Historical volatility is low
            ]

            # If all conditions are met, signal a potential increase in call options value
            if all(conditions):
                return f"Potential increase in call options value for {ticker}."
            else:
                return f"No strong signal for call options value increase for {ticker}."
        
        except Exception as e:
            print(e)
            return "Error occurred while scanning for call options."
        

    async def news(self, ticker:str='AAPL', page_size:str='10'):
        """Gets news articles for a ticker"""
        ticker_id = await self.trading.get_ticker_id(ticker)
        try:
            async with httpx.AsyncClient(headers=self.headers) as client:
                data = await client.get(f"https://nacomm.webullfintech.com/api/information/news/tickerNews?tickerId={ticker_id}&currentNewsId=0&pageSize={page_size}")
                data = data.json()
                df = NewsItem(data).df
                df['symbol'] = ticker
                await self.db.batch_insert_dataframe(df, table_name='news', unique_columns='symbol')
                return NewsItem(data)




        except Exception as e:
            print(e)


    async def cost_distribution(self, ticker:str='AAPL', start_date:str='2024-01-01', end_date:str='2024-05-18'):
        """Gets cost distribution for a ticker"""
        try:
            cost_dist = await self.trading.cost_distribution(symbol=ticker, start_date=start_date, end_date=end_date)

        

            df = cost_dist.df
            df['symbol'] = ticker
            df = df.drop(columns=['Distributions'])
            await self.db.batch_insert_dataframe(df, table_name='cost_dist', unique_columns='symbol')

            return cost_dist
        except Exception as e:
            print(e)



    async def second_bars(self, ticker: str = 'AAPL', timespan: str = 'm1', count: str = '800'):
        """Gets OHLCV data"""
        ticker_id = await self.trading.get_ticker_id(ticker)
        endpoint = f"https://quotes-gw.webullfintech.com/api/quote/charts/seconds-mini?tickerId={ticker_id}&type={timespan}&count={count}&restorationType=0"
        
        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.get(endpoint)
            data = response.json()[0]['data']
            
        # Convert data to list of lists
        rows = [line.split(',') for line in data]

        # Create DataFrame with correct column names
        df = pd.DataFrame(rows, columns=["timestamp", "open", "close", "high", "low", "vwap", "volume", "avg"])

        # Convert data types
        df = df.astype({
            "timestamp": 'int64',
            "open": 'float64',
            "close": 'float64',
            "high": 'float64',
            "low": 'float64',
            "vwap": 'float64',
            "volume": 'int64',
            "avg": 'float64'
        })

        # Convert timestamps to Eastern Time
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df['timestamp'] = df['timestamp'].dt.tz_localize(None)


        return df
    async def fetch_database_data(self, table_name, ticker: str = None):
        query = f"SELECT * FROM {table_name}"

        if ticker is not None:
            query += f" WHERE symbol = '{ticker}'"

        results = await self.db.fetch(query)

        # Assuming `self.db.fetch` returns a list of dictionaries
        if results:
            columns = results[0].keys()
        else:
            columns = []

        df = pd.DataFrame(results, columns=columns)

        return df
    

    async def candles(self, ticker:str='AAPL', timespan:str='d', timestamp: str = None):

        """OHLCV"""
        if timestamp:
            # Convert human-readable time to Unix timestamp
            dt =datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            unix_timestamp = int(dt.timestamp())
        else:
            # Use the current time if no timestamp is provided
            unix_timestamp = int(time.time())
        
        endpoint = f"https://quotes-gw.webullfintech.com/api/quote/charts/query-mini?tickerId=913243251&type={timespan}&count=800&timestamp={unix_timestamp}&restorationType=1"

        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.get(endpoint)
            data = response.json()[0]['data']
            
        # Convert data to list of lists
        rows = [line.split(',') for line in data]

        # Create DataFrame with correct column names
        df = pd.DataFrame(rows, columns=["timestamp", "open", "close", "high", "low", "vwap", "volume", "avg"])
        df.replace('null', np.nan, inplace=True)
        # Convert data types
        df = df.astype({
            "timestamp": 'int64',
            "open": 'float64',
            "close": 'float64',
            "high": 'float64',
            "low": 'float64',
            "vwap": 'float64',
            "volume": 'int64',
            "avg": 'float64'
        })

        # Convert timestamps to Eastern Time
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df['timestamp'] = df['timestamp'].dt.tz_localize(None)
        df['timestamp'] = df['timestamp'].astype(str)  # Convert to string to avoid JSON serialization error
        df['timespan'] = timespan
       # Calculate the percentage change and add it as a new column
        df['change_percent'] = df['close'].pct_change() * 100
        df['change_percent'] = df['change_percent'].round(2)

        df['symbol'] = ticker
        return df
    

    async def screener(self):
        ma5_10_cross = "\"wlas.tag.ma5_up_ma10\""
        rsi_16_os = "\"wlas.tag.rsi6_over_sell\""
        rsi_24_os = "\"wlas.tag.rsi24_over_sell\""
        bull_engulfing = "\"wlas.tag.postive_include_negative\""
        macd_golden_cross = "\"wlas.tag.macd_golden_cross\""
        three_white_soldiers="\"wlas.tag.three_white_soldiers\""
        endpoint = f"https://quotes-gw.webullfintech.com/api/wlas/screener/ng/query"

        async with httpx.AsyncClient(headers=self.headers) as client:
            data = await client.post(endpoint, json={"fetch":200,"rules":{"wlas.screener.rule.region":"securities.region.name.6","wlas.screener.rule.classicsindicator":f"[{macd_golden_cross}]"},"sort":{"rule":"wlas.screener.rule.price","desc":True}})

            data = data.json()

            nextFetch = data['nextFetch']

            for i in data['items']:
                print(i)
# import pandas as pd


# optsdata = OptionsData()
# market_data = StockData()
# from asyncio import Semaphore
# sema = Semaphore(1)
# async def main():
#     async with sema:
#         await market_data.db.connect()
#         stock_info = await market_data.stock_info()
#         option_data = [optsdata.get_all_options(ticker) for ticker in most_active_tickers]
#         news = [market_data.news(i) for i in most_active_tickers]
#         await asyncio.gather(*news, *option_data)

# asyncio.run(main())