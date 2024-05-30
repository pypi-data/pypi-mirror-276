from fudstop.apis.polygonio.polygon_database import PolygonDatabase
from fudstop.apis.polygonio.async_polygon_sdk import Polygon
from fudstop.apis.webull.webull_markets import WebullMarkets
from fudstop.apis.webull.webull_trading import WebullTrading
from asyncpg import create_pool
import asyncio
import httpx
from datetime import datetime, timedelta
wm = WebullMarkets(host='localhost', user='chuck', password='fud', port=5432, database='market_data')
trading = WebullTrading()
poly = Polygon(host='localhost', user='chuck', password='fud', port=5432, database='market_data')
db = PolygonDatabase(host='localhost', user='chuck', password='fud', port=5432, database='market_data')




class Starter:
    def __init__(self, pool):
        self.db = db
        self.poly = poly
        self.wm = wm
        self.trading = trading

        self.pool = pool  # Pool should be passed during the initialization
        self.last_processed = {}  # Dictionary to track tickers and their last processed time



    async def fetch_json(self, endpoint, params):
        """
        Asynchronously fetches JSON data from a given endpoint with specified parameters.
        
        :param endpoint: The URL of the API endpoint.
        :param params: Dictionary containing query parameters for the request.
        :return: JSON response as a dictionary.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint, params=params)
            response.raise_for_status()  # Raises an exception for HTTP errors.
            return response.json()  # Parses the JSON response and returns it.
        

    async def run_indefinitely(self):
        while True:
            ticker = await self.fetch_random_ticker()
            if ticker:
                yield ticker
  

    async def fetch(self, query, *args):
        """
        Fetch data from the database using the provided SQL query.

        :param query: The SQL query to execute.
        :param args: The arguments to pass to the SQL query.
        :return: The result of the query as a list of records.
        """
        async with self.pool.acquire() as conn:  # Acquire a connection from the pool
            return await conn.fetch(query, *args)

    async def fetch_random_ticker(self):
        """
        Queries a random ticker from the 'option_trades' table and ensures that no ticker
        is processed more than once per minute.
        """
        current_time = datetime.now()
        processed_tickers = [ticker for ticker, last_time in self.last_processed.items()
                             if (current_time - last_time) < timedelta(minutes=1)]

        query = """
        SELECT ticker FROM option_trades
        WHERE ticker NOT IN (SELECT unnest($1::text[]))
        ORDER BY RANDOM()
        LIMIT 1;
        """
        result = await self.fetch(query, processed_tickers)
        ticker = result[0]['ticker'] if result else None

        if ticker:
            self.last_processed[ticker] = current_time  # Update the last processed time for the ticker
            return ticker
        else:
            print("No new tickers available at the moment.")
            return None

    


    async def connect_to_db(self):
        try:
            await self.db.connect()

            print(f"Connected.")
        except Exception as e:
            print(e)