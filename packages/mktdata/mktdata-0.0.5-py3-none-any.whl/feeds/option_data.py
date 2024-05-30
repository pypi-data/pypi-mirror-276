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
f2osob_day="https://discord.com/api/webhooks/1206934896304726087/8ZBH7ZOTi3xr7ouk8SxYx1qccVXBvaBdWQW57hE7ZRjx943oQbcL-efGdZ45ad8jx7jn"
f2osob_hour="https://discord.com/api/webhooks/1206935054069272586/fCwEere6jiLvIHmSQGWJTsT7wcH26zxxdzFrHo58Uc00hdEdiDZ2x6ZV13PPm8WT1-bW"
f2osob_week="https://discord.com/api/webhooks/1206935164337389621/-V0EQ9GOWD6qhcxi7sPcfL4blKd81250E4b0f8AMo5EafZjPKmdBPmFt15IasRdEzSTl"
f2osob_month="https://discord.com/api/webhooks/1206935260433223710/7UHtfwnR8y08YlAQyJzPGtpMc3Xi7xeXgyTRvbvKGMoAuwnNBP9024ZR7A6H9Vx2GljX"
f2osob_minute="https://discord.com/api/webhooks/1242496945910579322/wf81VQSnLH3I31wLJA4u6yS8RovlWfRlg1cndodr39Ggy_Piyg_67v9C1a6KViwuRtDd"
macd_minute="https://discord.com/api/webhooks/1162153390059561072/cWyUfeWO7-dtKmuQ16jQbtPv-4Cbc64Gyfp6mfjobXLQaFrKWsT8qxePs7-6veNSp_w2"
macd_hour="https://discord.com/api/webhooks/1207036388999037009/qMP6OLR2MbuUvwCUUAWgvrdxOGcWqpVEBBQe642s3955ywc-O_sdrkygAnSjfCi9_c8t"
macd_day="https://discord.com/api/webhooks/1207036286011973632/Tg6EHghgPCMBpeIDT4e5GHN6QHokiZluUuIox2L5ZBRwheT-EjmXd59T5rGIziMHB_iz"
macd_week="https://discord.com/api/webhooks/1207036457668321280/rC3jFaSf6-xdzImejX2hxYPPFl1jHriY3GyluQWpp-6UzNg9tivvluoLvltxSRbAD1e0"
macd_month="https://discord.com/api/webhooks/1207036529432862740/-GeT46BidLSbfE79aYaJy8SJzZoL5kRVRI_Cn5mrLKLBEHXOBPsoQnHue9aRpwtxizi0"
engulf_day="https://discord.com/api/webhooks/1212598193032925194/Kp8veREPWv3ZEsGVMkb8zaQ-IVCxA4vwZHFNb0Aqf4hJ3zyI5I6TorKIm6fo8cpuf7TS"
engulf_week="https://discord.com/api/webhooks/1212598195935248394/VGU_pco8XR7WjqJ99_XdLeIeECHPZyzEGra6SIFITXiI-FlVv_5vB-XCmlDCpNJwz82F"
engulf_month="https://discord.com/api/webhooks/1212598198057828424/YNJHrw3H6xG2Q_fBTgtGcPSf_Uz1SifxprVv_OAfEugZx4N650gwRXdVnNx_eqPhRDsv"
engulf_hour="https://discord.com/api/webhooks/1212598201216143401/8YCDXc7Pwd_f51kPHt06GJtJp5baiKOu_KZFebWBeSxZTvX_OfAaBRY8BTj5GtZIJ2Wo"
engulf_4hour="https://discord.com/api/webhooks/1212598203661291610/mKf3eJAhKbDQ5kt1surt4Bl0mZTrA0MrmLfDADgpy8Xfz5MmnSCySVlbw3lzn9jmY1UN"
engulf_minute="https://discord.com/api/webhooks/1213155128161607712/ieF6ektHPErCiXQihgN5CD2JJa2u1GLW2d9SKqGa2HnJTri6S3k4u7_AhzFd3HBkJGWD"
engulf_30minute="https://discord.com/api/webhooks/1213155275536728115/mISPJIUHt1w7CqW6s7i0c-V0_uOL5aE9QzEATLFApb86ZhkgiAfTf-2Mi-5uxULhmwPC"
vol1k_25k="https://discord.com/api/webhooks/1210603719519903754/VFz_tr34NPURpE9jM__yvsnTqUb4XwJLpeP9Mz8RzpcNc0uYG5XTFWml8UxxHiiD4GkF"
vol25k_50k="https://discord.com/api/webhooks/1210604610905964564/8iSoW_QDjOkgjascCIvuiKL__n6KJv2ru6lm9-l9ZeQGRWNBkfPlpjb7TPaDNwNiXqSd"
vol50k="https://discord.com/api/webhooks/1210604487631437874/X8MvC8n5x7dRfP9pvInhCHTUMiuw3foHPn-UeSmK-iobsOTEMGalwxSyunrdip4a5kZR"

profiting_98="https://discord.com/api/webhooks/1204677752238637056/VhyMKcDc7m1BKoiZl-Li5dAHqT3sEgQpm7jCqQmBTY6Et0dLRPnAl6B1OEU55uFCpvVO"
profiting_2="https://discord.com/api/webhooks/1204677995051094077/SpryFul0yuCEmPaMpiHWgCz6R15t9pjR63I8_6ncgCN3RRPz_E57VHdyLi28O7cALeTO"
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








