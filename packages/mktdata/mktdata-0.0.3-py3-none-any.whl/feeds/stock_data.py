import os 
from dotenv import load_dotenv
load_dotenv()
import asyncio
import httpx
import time
from fudstop.apis.occ.occ_sdk import occSDK
import pandas as pd
import aiohttp
from datetime import datetime, timedelta
from embeddings.technical_embeds import rsi_embed, macd_embed, cost_dist_embed, volatility_embed
from fudstop.apis.polygonio.async_polygon_sdk import Polygon
from fudstop.apis.polygonio.polygon_database import PolygonDatabase
from fudstop.apis.webull.webull_trading import WebullTrading
poly = Polygon(host='localhost', user='chuck', password='fud', port=5432, database='market_data')
from .starter import Starter
occ = occSDK(host='localhost', user='chuck', password='fud', port=5432, database='market_data')
profiting_98="https://discord.com/api/webhooks/1204677752238637056/VhyMKcDc7m1BKoiZl-Li5dAHqT3sEgQpm7jCqQmBTY6Et0dLRPnAl6B1OEU55uFCpvVO"
profiting_2="https://discord.com/api/webhooks/1204677995051094077/SpryFul0yuCEmPaMpiHWgCz6R15t9pjR63I8_6ncgCN3RRPz_E57VHdyLi28O7cALeTO"
class StockData:
    def __init__(self, pool):
        self.pool=pool

        self.starter = Starter(pool)
        self.timespans = ['m1', 'm5', 'm10', 'm20', 'm30', 'm60', 'm120', 'm240', 'd', 'w']

        self.api_key = os.environ.get('YOUR_POLYGON_KEY')
        self.poly = poly
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        self.two_days_ago = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
        self.three_days_ago = (datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d')
        self.thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        self.thirty_days_from_now = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        self.fifteen_days_ago = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
        self.fifteen_days_from_now = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')
        self.eight_days_from_now = (datetime.now() + timedelta(days=8)).strftime('%Y-%m-%d')
        self.eight_days_ago = (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d')
        self.processed_tickers = {timespan: {} for timespan in self.timespans}  # Cache for processed tickers
        self.processing_interval = timedelta(minutes=1)  # Interval
        self.occ = occSDK(host='localhost', user='chuck', password='fud', port=5432, database='market_data')
        self.db = PolygonDatabase(host='localhost', user='chuck', password='fud', port=5432, database='market_data')
        self.trading = WebullTrading()
        
        self.quiet_hook = os.environ.get('quiet')
        self.volatile_hook = os.environ.get('volatile')
        self.still = os.environ.get('still')
        self.extreme = os.environ.get('extreme')
        self.unclear = os.environ.get('unclear')



    async def cost_dist(self):
        await self.db.connect()
        async for ticker in self.starter.run_indefinitely():
            status = None
            current_time = datetime.now()

            # Check if ticker was processed recently
            if ticker in self.processed_tickers:
                last_processed_time = self.processed_tickers[ticker]
                if (current_time - last_processed_time) < self.processing_interval:
                    print(f"Skipping {ticker} processed recently")
                    return None
                

            try:

                cost_task = await self.trading.cost_distribution(ticker, start_date=self.three_days_ago, end_date=self.today)

                profit_ratio = round(float(cost_task.closeProfitRatio)*100,2)
                print(f"PROFIT RATIO CHECK: {profit_ratio}")
                if profit_ratio >= 98:

                    status = 'bearish signal'


                    await cost_dist_embed(hook=profiting_98, ticker=ticker, status=status, profit_ratio=profit_ratio)
                
                if profit_ratio <= 2:
                    status = 'bullish signal'


                    await cost_dist_embed(hook=profiting_2, ticker=ticker, status=status, profit_ratio=profit_ratio)




            except Exception as e:
                pass


    async def stock_info(self):
        await self.db.connect()
        async for ticker in self.starter.run_indefinitely():
            processed_tickers = set()


            status = None
            current_time = datetime.now()

            # Check if ticker was processed recently
            if ticker in processed_tickers:
                last_processed_time = processed_tickers[ticker]
                if (current_time - last_processed_time) < self.processing_interval:
                    print(f"Skipping {ticker} processed recently")
                    return None
                

            try:
                info = await self.occ.stock_info(symbol=ticker, has_options=True)
                df = info.as_dataframe
                print(df)
                df['symbol'] = ticker

                df = df.drop(columns=['update_date'])
                await self.db.batch_insert_dataframe(df=df, table_name='info', unique_columns='symbol')
            



                volatile_rank = info.volatileRank
                if volatile_rank in ['Rather quiet', 'Quiet']:
                    hook = self.quiet_hook
                    status = volatile_rank
                    await volatility_embed(hook, info, status, ticker)

                if volatile_rank in ['Slightly volatile', 'Volatile']:
                    hook = self.volatile_hook
                    status = volatile_rank
                    await volatility_embed(hook, info, status, ticker)
                if volatile_rank in ['', 'Volatility unclear']:
                    hook = self.unclear
                    status = volatile_rank
                    await volatility_embed(hook, info, status, ticker)
                if volatile_rank == 'Extremely volatile':
                    hook = self.extreme
                
                    status = volatile_rank
                    await volatility_embed(hook, info, status, ticker)

                if volatile_rank == 'Absolutely still':
                    hook = self.still
                
                    status = volatile_rank
                    await volatility_embed(hook, info, status, ticker)
            except Exception as e:
                print(e)
