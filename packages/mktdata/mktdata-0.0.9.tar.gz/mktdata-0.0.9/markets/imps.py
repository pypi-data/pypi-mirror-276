from fudstop.apis.webull.webull_markets import WebullMarkets
from fudstop.apis.webull.webull_trading import WebullTrading
from fudstop.apis.polygonio.polygon_database import PolygonDatabase
from fudstop.apis.polygonio.async_polygon_sdk import Polygon
from fudstop.apis.helpers import identify_sector, get_human_readable_string
import os
import asyncpg
from embeddings import specials
from dotenv import load_dotenv
load_dotenv()
from polygon.websocket import WebSocketClient, Market
from polygon.websocket.models import WebSocketMessage
from typing import List
from zoneinfo import ZoneInfo  # For Python 3.9 and later
import asyncio
import httpx
import pandas as pd
from fudstop._markets.list_sets.dicts import technology,industrials,communication_services,consumer_cyclical,consumer_defensive,healthcare,energy,etfs,real_estate,utilities,basic_materials,financial_services,option_conditions_dict,stock_conditions_description_dictionary, hex_color_dict
from fudstop.apis.polygonio.mapping import option_condition_dict, stock_condition_dict, STOCK_EXCHANGES,OPTIONS_EXCHANGES
from datetime import datetime, timezone
from polygon.websocket import EquityTrade
all_tickers = technology + industrials + communication_services + consumer_cyclical + consumer_defensive + healthcare + energy + etfs + real_estate + utilities + basic_materials + financial_services

poly = Polygon(host='localhost', password='fud', port=5432, user='chuck', database='market_data')
db = PolygonDatabase(host='localhost', password='fud', port=5432, user='chuck', database='market_data')
wbm = WebullMarkets(host='localhost', password='fud', port=5432, user='chuck', database='market_data')
wbt = WebullTrading()

# Establish a connection pool (consider doing this outside of your function if possible)
async def create_pool():
    return await asyncpg.create_pool(dsn='postgresql://chuck:fud@localhost/market_data')


# Helper function to convert the data
def convert_equity_trade(trade: EquityTrade):
    # Convert timestamp from nanoseconds since Unix epoch to human-readable UTC format
    trade.timestamp = datetime.fromtimestamp(trade.timestamp / 1_000_000_000, tz=timezone.utc).isoformat()

    # Convert conditions
    trade.conditions = [stock_condition_dict.get(code, "Unknown Condition") for code in trade.conditions]

    # Convert exchange code
    trade.exchange = STOCK_EXCHANGES.get(trade.exchange, "Unknown Exchange")
    return trade

async def get_client(endpoint, api_key=None):
    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    
    # Create and configure the client
    async with httpx.AsyncClient(base_url=endpoint, headers=headers) as client:
        response = await client.get(endpoint)  # Assuming the endpoint is the full URL you want to GET
        return response.json()  # This will return the response from the endpoint



