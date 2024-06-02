import os 
from dotenv import load_dotenv
load_dotenv()
from embeddings.technical_embeds import option_embed
import asyncio
import httpx
import time
from fudstop.apis.polygonio.polygon_options import PolygonOptions
import pandas as pd
import aiohttp
from datetime import datetime, timedelta
from embeddings.technical_embeds import rsi_embed, macd_embed, cost_dist_embed
from fudstop.apis.polygonio.async_polygon_sdk import Polygon
from fudstop.apis.polygonio.polygon_database import PolygonDatabase
from .starter import Starter
from fudstop.apis.webull.webull_trading import WebullTrading
poly = Polygon(host='localhost', user='chuck', password='fud', port=5432, database='market_data')
from .starter import Starter

vol1k_25k="https://discord.com/api/webhooks/1246112589956775986/_XfVlgu06E0_OFOUQxMdj4paXET_hTxLEjiE_fM9S2WdABe9oJM686QI-xzaH3d0FM80"
vol25k_50k="https://discord.com/api/webhooks/1246112713671708854/QiDj5eZxKZuLgKckJ9bb0qm_Bbc00qXElhG8zdGSW8CKX1RWiXzGXC7uhMnM_MTjlZMB"
vol50k="https://discord.com/api/webhooks/1246112864272650382/XQVZTzdZls_k4NXbYLV2Ff3PUh3o3XXKfytB5BLhvMT6yZ0rbyF3GCIkGKHL8TFszjkI"


class OptionData:
    def __init__(self, pool):
        self.pool = pool
        self.timespans = ['m1', 'm5', 'm10', 'm15', 'm20', 'm30', 'm60', 'm120', 'm240', 'd', 'w']
        self.api_key = os.environ.get('YOUR_POLYGON_KEY')
        self.poly_opts = PolygonOptions(database='market_data')
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        self.two_days_ago = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
        self.thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        self.thirty_days_from_now = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        self.fifteen_days_ago = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
        self.fifteen_days_from_now = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')
        self.eight_days_from_now = (datetime.now() + timedelta(days=8)).strftime('%Y-%m-%d')
        self.eight_days_ago = (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d')
        self.processed_tickers = {timespan: {} for timespan in self.timespans}  # Cache for processed tickers
        self.processing_interval = timedelta(minutes=1)  # Interval
        self.db = PolygonDatabase(user='chuck', database='market_data', password='fud', port=5432, host='localhost')
        self.trading = WebullTrading()
        self.starter = Starter(pool)
        self.options = PolygonOptions()
        





    async def option_greeks(self):
        
        try:
            db = PolygonDatabase(user='chuck', database='market_data', password='fud', port=5432, host='localhost')
            await db.connect()
            
            while True:
                async for ticker in self.starter.run_indefinitely():
                    data = await self.poly_opts.get_option_chain_all(ticker, expiration_date_gte=self.today, expiration_date_lite=self.thirty_days_from_now)

                    # Assuming data has attributes: volume, ticker, strike, expiry, contract_type, change_percent
                    vol_1k_to_25k = [
                        (vol, tick, price, bid, mid, ask, strk, exp, cp, chg_pct, oi) 
                        for vol, tick, price, bid, mid, ask, strk, exp, cp, chg_pct, oi in zip(data.volume, data.underlying_ticker, data.underlying_price, data.bid, data.midpoint, data.ask, data.strike, data.expiry, data.contract_type, data.change_percent, data.open_interest) 
                        if vol >= 1250 and vol <= 24999 and vol > oi
                    ]

                    # Print the filtered data
                    for vol, tick, price, bid,mid, ask, strk, exp, cp, chg_pct, oi in vol_1k_to_25k:
                        asyncio.create_task(option_embed(hook=vol1k_25k, ticker=tick, strike=strk, cp=cp, expiry = exp, volume=vol, oi=oi, condition='1k to 25k volume', price=price, bid=bid, mid=mid, ask=ask, chg_pct=chg_pct))

                    # Assuming data has attributes: volume, ticker, strike, expiry, contract_type, change_percent
                    vol_25k_to_50k = [
                        (vol, tick, price, bid, mid, ask, strk, exp, cp, chg_pct, oi) 
                        for vol, tick, price, bid, mid, ask, strk, exp, cp, chg_pct, oi in zip(data.volume, data.underlying_ticker, data.underlying_price, data.bid, data.midpoint, data.ask, data.strike, data.expiry, data.contract_type, data.change_percent, data.open_interest) 
                        if vol >= 25000 and vol <= 49999 and vol > oi
                    ]

                    # Print the filtered data
                    for vol, tick, price, bid,mid, ask, strk, exp, cp, chg_pct, oi in vol_25k_to_50k:
                        asyncio.create_task(option_embed(hook=vol25k_50k, ticker=tick, strike=strk, cp=cp, expiry = exp, volume=vol, oi=oi, condition='25k to 50k volume', price=price, bid=bid, mid=mid, ask=ask, chg_pct=chg_pct))

                    # Assuming data has attributes: volume, ticker, strike, expiry, contract_type, change_percent
                    vol_50k_plus = [
                        (vol, tick, price, bid, mid, ask, strk, exp, cp, chg_pct, oi) 
                        for vol, tick, price, bid, mid, ask, strk, exp, cp, chg_pct, oi in zip(data.volume, data.underlying_ticker, data.underlying_price, data.bid, data.midpoint, data.ask, data.strike, data.expiry, data.contract_type, data.change_percent, data.open_interest) 
                        if vol >= 50000 and vol > oi
                    ]

                    # Print the filtered data
                    for vol, tick, price, bid,mid, ask, strk, exp, cp, chg_pct, oi in vol_50k_plus:
                        asyncio.create_task(option_embed(hook=vol50k, ticker=tick, strike=strk, cp=cp, expiry = exp, volume=vol, oi=oi, condition='50k+ volume', price=price, bid=bid, mid=mid, ask=ask, chg_pct=chg_pct))


                    greeks = [(tick, sym, unp, chpct, strk, cp, exp,dte, vol, oi, d,g,v,t,ch,cl,sp,ut,va,ve,vm, iv, iv_pct) for tick, sym, unp, chpct, strk, cp, exp, dte,vol, oi, d,g,v,t,ch,cl,sp,ut,va,ve,vm, iv, iv_pct in zip(data.underlying_ticker, data.ticker, data.underlying_price, data.change_percent, data.strike, data.contract_type, data.expiry, data.days_to_expiry_series, data.volume, data.open_interest, data.delta, data.gamma, data.theta, data.vega, data.charm, data.color, data.speed,data.ultima,data.vanna,data.veta,data.vomma,data.implied_volatility, data.iv_percentile)]
                    columns = ['ticker', 'symbol', 'underlying_price', 'change_percent', 'strike', 'cp', 'expiry',
                'days_to_expiry', 'volume', 'open_interest', 'delta', 'gamma', 'theta', 'vega', 'charm', 'color', 'speed',
                'ultima', 'vanna', 'veta', 'vomma', 'iv', 'iv_percentile']
                    

                    df = pd.DataFrame(greeks, columns=columns)
                    print(df)

                    await db.batch_insert_dataframe(df, table_name='greeks', unique_columns='ticker,strike,cp,expiry')






        except Exception as e:
            print(e)








