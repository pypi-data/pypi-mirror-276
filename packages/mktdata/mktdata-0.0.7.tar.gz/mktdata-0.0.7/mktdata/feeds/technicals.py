import os 
from dotenv import load_dotenv
load_dotenv()
import asyncio
import httpx
from fudstop.apis.helpers import format_large_numbers_in_dataframe
from datetime import datetime, timedelta
from embeddings.technical_embeds import rsi_embed, macd_embed, td9_embed, candlestick_embed, option_embed
from mktdata.stock_data import StockData
from fudstop.apis.polygonio.async_polygon_sdk import Polygon
from fudstop.apis.polygonio.polygon_database import PolygonDatabase
from fudstop.apis.webull.webull_trading import WebullTrading
import aiohttp
from fudstop.apis.polygonio.polygon_options import PolygonOptions
import pandas as pd
import time
import logging

logging.basicConfig(level=logging.INFO)
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

class TechnicalProcessor:
    def __init__(self, pool):
        self.pool = pool

        self.starter = Starter(pool)
        self.timespans = ['minute', 'hour', 'week', 'day', 'month']
        self.chart_timespans = ['m1', 'm5', 'm10', 'm20', 'm30', 'm60', 'm120', 'm240', 'd', 'w', 'm']
        self.engulf_intervals = ['m60', 'm240', 'd', 'w','m','m1','m30']
        self.rsi_dict = { 
            'minute': f2osob_minute,
            'hour': f2osob_hour,
            'week': f2osob_week,
            'day': f2osob_day,
            'month': f2osob_month
        }
        self.options = PolygonOptions(database='market_data')
        self.db = PolygonDatabase(host='localhost', user='chuck', database='market_data', password='fud', port=5432)
        self.api_key = os.environ.get('YOUR_POLYGON_KEY')
        self.poly = poly
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        self.thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        self.thirty_days_from_now = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        self.ninety_days_from_now = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
        self.fifteen_days_ago = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
        self.fifteen_days_from_now = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')
        self.eight_days_from_now = (datetime.now() + timedelta(days=8)).strftime('%Y-%m-%d')
        self.eight_days_ago = (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d')
        self.processed_tickers = {timespan: {} for timespan in self.timespans}  # Cache for processed tickers
        self.processing_interval = timedelta(minutes=1)  # Interval

        self.trading = WebullTrading()
        self.processed_td9_tickers = {timespan: {} for timespan in self.chart_timespans}
        self.interval_dict = {
            'm': os.environ.get('td9_m', 'https://discord.com/api/webhooks/1207884982647918613/TY0qda6Kr7MMUCiOfNRMKZIqgBZ94EWcN5JVt_wLb3VeDU4vBbt0Pwml1EEIsWfLaub3'),
            'd': os.environ.get('td9_d', 'https://discord.com/api/webhooks/1207885362526158928/0HaIDN2XLugQvaliFxuiKCYLsXhEBOd4vqiWQt_XkeFXgq2jnXRbVBaPH7C5NDf-FCTr'),
            'w': os.environ.get('td9_w', 'https://discord.com/api/webhooks/1207885265448738918/vnfuFtm4Yw-NcaYmgziCJJZcLW1UfNEJDn0d7KPk0rY_q7M44W6R98f2fg3y8leKyOvA'),
            'm1': os.environ.get('td9_m1', 'https://discord.com/api/webhooks/1212540300350988359/e_BX3yWTdZaOyvFC3P1Ir7CAq5LN8IRxCcq9R_VJZvqFDfnSwXOxnyxhctyDpJdVq9ym'),
            'm5': os.environ.get('td9_m5', 'https://discord.com/api/webhooks/1212540358827835432/EoQKj7Pt0idb0Z0qaAahxXKvpMgVhL6KPGOjIdjxWgOS3P9tJmlFqdAi3MRRBATPayBE'),
            'm15': os.environ.get('td9_m15', 'https://discord.com/api/webhooks/1212540447919186000/Flqytu4d4I8bZiD8GzZf1j2qb0xiMFQRg9dV96bE9stCIqXGQJ5RkQJB0mIhOCH8gRQ5'),
            'm30': os.environ.get('td9_m30', 'https://discord.com/api/webhooks/1212540241689190480/SCcvC4GeOYoeodES7zYEMOqyYpwWeBoB3awGAO6Xp6KkeXSJJqemgz7VfSjCscILQxzW'),
            'm60': os.environ.get('td9_m60', 'https://discord.com/api/webhooks/1212540533151506503/WFu8NiwQi3iH86OH9lBegT-AwJM8rh-fWPuR-EhInWr20T0wJnWEm4VHCzLZ2Ore8SPa'),
            'm120': os.environ.get('td9_m120', 'https://discord.com/api/webhooks/1212540620833427486/tASJYDyKR7tmsH0MjH8kPG2AuNBgY12Dr_mZ8jHqRUDsyYztHllWuSZM6DB7iVSbLYTj'),
            'm240': os.environ.get('td9_m240', 'https://discord.com/api/webhooks/1212540713934266438/kMrwDe94JpdZC0oFqsgdaqg3jU3YK2RgXebgHhIKs8jul2LO3HqyFR0aD55OJjB_svjR')
        }
        self.hammer_hooks = { 
            'm1': os.environ.get('hammer_minute'),
            'm30': os.environ.get('hammer_30minute'),
            'm60': os.environ.get('hammer_hour'),
            'm240': os.environ.get('hammer_4hour'),
            'd': os.environ.get('hammer_day'),
            'w': os.environ.get('hammer_week'),
            'm': os.environ.get('hammer_month'),
        }

        self.engulf_hooks = { 
            'd': os.environ.get('engulf_day'),
            'w': os.environ.get('engulf_week'),
            'm': os.environ.get('engulf_month'),
            'm60': os.environ.get('engulf_hour'),
            'm240': os.environ.get('engulf_4hour'),
            'm1': os.environ.get('engulf_minute'),
            'm30': os.environ.get('engulf_30minute')
            
        }

        self.flag_hooks = { 
            'm60': os.environ.get('flags_hour'),
            'd': os.environ.get('flags_day'),
            'm': os.environ.get('flags_month'),
            'w': os.environ.get('flags_week')
        }
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Access-Token": "dc_us_tech1.18fb31644a4-c795ddfca0344416bab698fcddeeb26d",
            "App": "global",
            "App-Group": "broker",
            "Appid": "wb_web_app",
            "Device-Type": "Web",
            "Did": "gldaboazf4y28thligawz4a7xamqu91g",
            "Hl": "en",
            "Content-Type": "application/json",
            "Locale": "eng",
            "Origin": "https://app.webull.com",
            "Os": "web",
            "Ph": "Windows Chrome",
            "Platform": "web",
            "Priority": "u=1, i",
            "Referer": "https://app.webull.com/",
            "Reqid": "f157840b26874213816076c417456ade",
            "T-Time": "1715662035135",
            "Tz": "America/Chicago",
            "Ver": "4.6.3",
            "X-S": "56766c7a71c1a81a0c1e8a1927dbd15eb3043da89cd608c46d29658ccfda33f5",
            "X-Sv": "xodp2vg9"
        }

    ####################

    ##      CHECKS #######

    #############################

    async def is_bullish_engulfing(self, df):
        """
        Checks for Bullish Engulfing pattern.
        """
        candle_today = df.iloc[0]
        candle_prev = df.iloc[1]

        basic_shape = (candle_today['Close'] > candle_today['Open'] and
                       candle_prev['Close'] < candle_prev['Open'] and
                       candle_today['Open'] < candle_prev['Close'] and
                       candle_today['Close'] > candle_prev['Open'])
        increased_volume = candle_today['Volume'] > candle_prev['Volume']
        yield basic_shape and increased_volume

    async def is_hammer(self, df):
        """
        Checks for Hammer pattern.
        """
        candle = df.iloc[0]
        prev_candles = df.iloc[1:4]

        if prev_candles.empty:
            yield False
        else:
            downtrend = all(row.Close < row.Open for row in prev_candles.itertuples())
            if not downtrend:
                yield False
            else:
                body = abs(candle['Close'] - candle['Open'])
                lower_shadow = min(candle['Open'], candle['Close']) - candle['Low']
                upper_shadow = candle['High'] - max(candle['Open'], candle['Close'])
                is_long_lower_shadow = lower_shadow >= 2 * body
                is_small_upper_shadow = upper_shadow <= body * 0.5
                is_small_body = body <= lower_shadow * 0.3
                yield is_long_lower_shadow and is_small_upper_shadow and is_small_body

    async def is_inverted_hammer(self, df):
        """
        Checks for Inverted Hammer pattern.
        """
        candle = df.iloc[0]

        body = abs(candle['Close'] - candle['Open'])
        upper_shadow = candle['High'] - max(candle['Open'], candle['Close'])
        lower_shadow = min(candle['Open'], candle['Close']) - candle['Low']
        total_range = candle['High'] - candle['Low']
        long_upper_shadow = upper_shadow > (2 * body) and upper_shadow > (0.5 * total_range)
        small_lower_shadow = lower_shadow < (0.1 * total_range)
        small_body = body < (0.2 * total_range)
        yield long_upper_shadow and small_lower_shadow and small_body

    async def is_shooting_star(self, df):
        """
        Checks for Shooting Star pattern.
        """
        candle = df.iloc[0]
        prev_candles = df.iloc[1:4]

        if prev_candles.empty:
            yield False
        else:
            is_uptrend = prev_candles['Close'].iloc[-1] > prev_candles['Open'].iloc[-1]
            body = abs(candle['Close'] - candle['Open'])
            total_range = candle['High'] - candle['Low']
            upper_shadow = candle['High'] - max(candle['Open'], candle['Close'])
            lower_shadow = min(candle['Open'], candle['Close']) - candle['Low']
            long_upper_shadow = upper_shadow > (2 * body)
            small_body_near_low = body <= (total_range * 0.2) and lower_shadow <= (body * 0.1)
            yield is_uptrend and long_upper_shadow and small_body_near_low

    async def is_three_black_crows(self, df):
        """
        Checks for Three Black Crows pattern.
        """
        if len(df) < 3:
            return False
        else:
            last_three = df.head(3)
            bearish = all(last_three['Close'].iloc[i] < last_three['Open'].iloc[i] for i in range(3))
            descending_closes = all(last_three['Close'].iloc[i] < last_three['Close'].iloc[i-1] for i in range(1, 3))
            opens_within_previous = all(last_three['Open'].iloc[i] < last_three['Open'].iloc[i-1] for i in range(1, 3))
            return bearish and descending_closes and opens_within_previous

    async def is_three_white_soldiers(self, df):
        """
        Checks for Three White Soldiers pattern.
        """
        if len(df) < 3:
            return False
        else:
            last_three = df.head(3)
            bullish = all(last_three['Close'].iloc[i] > last_three['Open'].iloc[i] for i in range(3))
            ascending_closes = all(last_three['Close'].iloc[i] > last_three['Close'].iloc[i-1] for i in range(1, 3))
            not_lower_opens = all(last_three['Open'].iloc[i] >= last_three['Close'].iloc[i-1] for i in range(1, 3))
            return bullish and ascending_closes and not_lower_opens

    async def is_bearish_engulfing(self, df):
        """
        Checks for Bearish Engulfing pattern.
        """
        candle_today = df.iloc[0]
        candle_prev = df.iloc[1]

        basic_shape = (candle_today['Close'] < candle_today['Open'] and
                       candle_prev['Close'] > candle_prev['Open'] and
                       candle_today['Open'] > candle_prev['Close'] and
                       candle_today['Close'] < candle_prev['Open'])
        increased_volume = candle_today['Volume'] > candle_prev['Volume']
        yield basic_shape and increased_volume

    async def is_hanging_man(self, df):
        """
        Checks for Hanging Man pattern.
        """
        candle = df.iloc[0]
        prev_candles = df.iloc[1:4]

        if prev_candles.empty:
            yield False
        else:
            is_uptrend = prev_candles['Close'].iloc[-1] > prev_candles['Open'].iloc[-1]
            body = abs(candle['Close'] - candle['Open'])
            total_range = candle['High'] - candle['Low']
            lower_shadow = min(candle['Open'], candle['Close']) - candle['Low']
            upper_shadow = candle['High'] - max(candle['Open'], candle['Close'])
            body_small = body <= (total_range * 0.2)
            lower_shadow_long = lower_shadow >= (body * 2)
            upper_shadow_small = upper_shadow <= (body * 0.1)
            yield is_uptrend and body_small and lower_shadow_long and upper_shadow_small

    async def is_bullish_harami(self, df):
        """
        Checks for Bullish Harami pattern.
        """
        candle_today = df.iloc[0]
        candle_prev = df.iloc[1]

        basic_shape = (candle_today['Close'] > candle_today['Open'] and
                       candle_prev['Close'] < candle_prev['Open'] and
                       candle_today['Open'] > candle_prev['Open'] and
                       candle_today['Close'] < candle_prev['Close'])
        decreased_volume = candle_today['Volume'] < candle_prev['Volume']
        yield basic_shape and decreased_volume


   
                
    async def check_td9_bullish(self, df):
        """
        Checks for TD9 bullish setup.
        """
        try:
            count = 0
            for i in range(len(df) - 1, 3, -1):  # Start from the most recent candle going backwards
                if df.iloc[i]['Close'] > df.iloc[i-4]['Close']:
                    count += 1
                else:
                    count = 0
                if count == 9:
                    return True
            return False
        except Exception as e:
            pass

    async def check_td9_bearish(self, df):
        """
        Checks for TD9 bearish setup.
        """
        try:
            count = 0
            for i in range(len(df) - 1, 3, -1):  # Start from the most recent candle going backwards
                if df.iloc[i]['Close'] < df.iloc[i-4]['Close']:
                    count += 1
                else:
                    count = 0
                if count == 9:
                    
                    return True
            return False
        except Exception as e:
            pass

    async def check_macd_sentiment(self, ticker, timespan, hist: list):
        try:
            if hist is not None:
                if hist is not None and len(hist) >= 3:
                    
                    last_three_values = hist[:3]
                    if abs(last_three_values[0] - (-0.02)) < 0.04 and all(last_three_values[i] > last_three_values[i + 1] for i in range(len(last_three_values) - 1)):
                        yield 'bullish'

                    if abs(last_three_values[0] - 0.02) < 0.04 and all(last_three_values[i] < last_three_values[i + 1] for i in range(len(last_three_values) - 1)):
                        yield 'bearish'
        except Exception as e:
            pass


    async def fetch_rsi_for_timespan(self, ticker, timespan):
        """
        Fetch the RSI for a specific ticker and timespan.

        :param ticker: The ticker symbol.
        :param timespan: The timespan to fetch RSI for.
        :return: The RSI data.
        """
        await self.db.connect()
        if ticker == 'SPX':
            ticker = 'I:SPX'
        status = None
        current_time = datetime.now()

        # Check if ticker was processed recently
        if ticker in self.processed_tickers[timespan]:
            last_processed_time = self.processed_tickers[timespan][ticker]
            if (current_time - last_processed_time) < self.processing_interval:
                logging.info(f"Skipping {ticker} for {timespan}, processed recently")
                return None

        try:
            rsi = await self.poly.rsi(ticker, timespan, limit=50)
            macd = await self.poly.macd(ticker, timespan=timespan)
            hist = macd.macd_histogram

            macd_tasks = []
            async for macd_cross in self.check_macd_sentiment(ticker, timespan, hist):
                if macd_cross is not None:
                    macd_hook = None
                    if timespan == 'week':
                        macd_hook = macd_week
                    elif timespan == 'hour':
                        macd_hook = macd_hour
                    elif timespan == 'day':
                        macd_hook = macd_day
                    elif timespan == 'month':
                        macd_hook = macd_month
                    
                    if macd_hook:
                        macd_tasks.append(
                            asyncio.create_task(
                                macd_embed(hook=macd_hook, type=macd_cross, ticker=ticker, timespan=timespan, db=self.db)
                            )
                        )

            if macd_tasks:
                await asyncio.gather(*macd_tasks)

            if rsi.rsi_value[0] <= 30:
                status = 'oversold'
            elif rsi.rsi_value[0] >= 70:
                status = 'overbought'

            if status is not None:
                webhook_url = self.rsi_dict.get(timespan)
                await rsi_embed(hook=webhook_url, ticker=ticker, status=status, timespan=timespan, rsi=rsi.rsi_value[0], underlying_data=rsi.underlying_dict, db=self.db)
            
            # Update the last processed time for the ticker
            self.processed_tickers[timespan][ticker] = current_time
            return rsi

        except Exception as e:
            logging.error(f"Error fetching RSI for {ticker} ({timespan}): {e}")
            return None
    async def rsi_feed(self):
        try:
            while True:
                tickers = []
                async for ticker in self.starter.run_indefinitely():
                    if ticker:
                        tickers.append(ticker)
                        if len(tickers) >= 5:  # Process in batches of 5 tickers
                            break

                if tickers:
                    # Process RSI for each timespan
                    rsi_tasks = [self.fetch_rsi_for_timespan(ticker, timespan) for ticker in tickers for timespan in self.timespans]
                    await asyncio.gather(*rsi_tasks)

                    # Process TD9 for each chart timespan
                    td9_tasks = [self.fetch_td9_for_timespan(ticker, chart_timespan) for ticker in tickers for chart_timespan in self.chart_timespans]
                    await asyncio.gather(*td9_tasks)


                    

        

        except Exception as e:
            print(f"Error processing tickers: {e}")


    async def check_and_notify(self, ticker, timespan, interval, td9_df, lol_td9_df, check_pattern_func, status, hooks):
        async for pattern_detected in check_pattern_func(td9_df):
            if pattern_detected:
                asyncio.create_task(candlestick_embed(hook=hooks.get(interval), timespan=timespan, status=status, ticker=ticker, df=lol_td9_df))
                logging.info(f"{status.upper()} detected for {ticker}")

    async def check_and_notify_simple(self, ticker, timespan, td9_df, lol_td9_df, check_pattern_func, status, webhook_url):
        pattern_detected = await check_pattern_func(td9_df)
        if pattern_detected:
            asyncio.create_task(candlestick_embed(hook=webhook_url, timespan=timespan, status=status, ticker=ticker, df=lol_td9_df))
            logging.info(f"{status.upper()} detected for {ticker}")

    async def async_get_td9(self, ticker, interval):
        try:
            timeStamp = None
            if ticker == 'I:SPX':
                ticker = 'SPXW'
            elif ticker =='I:NDX':
                ticker = 'NDX'
            elif ticker =='I:VIX':
                ticker = 'VIX'
            elif ticker == 'I:XSP':
                ticker = 'XSP'
            ticker_id = await self.trading.get_ticker_id(ticker)





            if timeStamp is None:
                # if not set, default to current time
                timeStamp = int(time.time())

            base_fintech_gw_url = f'https://quotes-gw.webullfintech.com/api/quote/charts/query?tickerIds={ticker_id}&type={interval}&count=300&extendTrading=1'



            if interval == 'm1':
                timespan = '1min'
            elif interval == 'm60':
                timespan = '1hour'
            elif interval == 'm20':
                timespan = '20min'
            elif interval == 'm5':
                timespan = '5min'
            elif interval == 'm15':
                timespan = '15min'
            elif interval == 'm30':
                timespan = '30min'
            elif interval == 'm120':
                timespan = '2hour'
            elif interval == 'm240':
                timespan = '4hour'
            elif interval == 'd':
                timespan = 'day'
            elif interval == 'w':
                timespan = 'week'
            elif interval == 'm':
                timespan = 'month'
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(base_fintech_gw_url) as resp:
                    r = await resp.json()
                    try:
                        # Check if the data is present and the expected structure is correct
                        if r and isinstance(r, list) and 'data' in r[0]:
                            data = r[0]['data']

                            data = r[0]['data']
                            if data is not None:
                                parsed_data = []
                                for entry in data:
                                    values = entry.split(',')
                                    if values[-1] == 'NULL':
                                        values = values[:-1]
                                    elif values[-1] == 'NULL':
                                        values = values[:-1]  # remove the last element if it's 'NULL'
                                    parsed_data.append([float(value) if value != 'null' else 0.0 for value in values])
                                try:
                                    sorted_data = sorted(parsed_data, key=lambda x: x[0], reverse=True)
                                    
                                    # Dynamically assign columns based on the length of the first entry
                                    columns = ['Timestamp', 'Open', 'Close', 'High', 'Low', 'N', 'Volume', 'Vwap'][:len(sorted_data[0])]
                                    
                                    df = pd.DataFrame(sorted_data, columns=columns)
                                    # Convert the Unix timestamps to datetime objects in UTC first
                                    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s', utc=True)

                                    # Convert UTC to Eastern Time (ET)
                                    df['Timestamp'] = df['Timestamp'].dt.tz_convert('US/Eastern')
                                    df['Timestamp'] = df['Timestamp'].dt.tz_localize(None)
                                    df['Ticker'] = ticker
                                    df['timespan'] = interval


                                    df['ticker'] = ticker

                                    
                                    td9_df = df.head(13)
                                    lol_td9_df = df[['Open', 'High', 'Low', 'Close']].head(13)
                                    lol_td9_df = format_large_numbers_in_dataframe(lol_td9_df)
                                    check_bull_task = asyncio.create_task(self.check_td9_bullish(td9_df))
                                    check_bear_task = asyncio.create_task(self.check_td9_bearish(td9_df))

                                    results = await asyncio.gather(check_bull_task, check_bear_task)
                                    
                                    if results[0] == True:
                                        print(results[0])
                                        status = 'bullish_td9'
                                        asyncio.create_task(td9_embed(hook=self.interval_dict.get(interval), timespan=timespan, status=status, ticker=ticker, df=lol_td9_df, db=self.db))


                                    if results[1] == True:
                                        print(results[1])
                                        status = 'bearish_td9'
                                        asyncio.create_task(td9_embed(hook=self.interval_dict.get(interval), timespan=timespan, status=status, ticker=ticker, df=lol_td9_df, db=self.db))
                                    # Checking for additional candlestick patterns
                                    # async for check_star in self.is_shooting_star(td9_df):
                                    #     if check_star:
                                    #         status = 'shooting_star'
                                    #         await candlestick_embed(hook=self.interval_dict.get(interval), timespan=timespan, status=status, ticker=ticker, df=td9_df)
                                    #         print(f"SHOOTING STAR DETECTED {ticker}")

                                    async for check_bull_engulf in self.is_bullish_engulfing(td9_df):
                                        if check_bull_engulf == True:
                                            status = 'bullish_engulfing'
                                            asyncio.create_task(candlestick_embed(hook=self.engulf_hooks.get(interval), timespan=timespan, status=status, ticker=ticker, df=lol_td9_df, db=self.db))
                                            print(f"BULLISH ENGULFING DETECTED {ticker}")

                                    async for check_bear_engulf in self.is_bearish_engulfing(td9_df):
                                        if check_bear_engulf == True:
                                            status = 'bearish_engulfing'
                                            asyncio.create_task(candlestick_embed(hook=self.engulf_hooks.get(interval), timespan=timespan, status=status, ticker=ticker, df=lol_td9_df, db=self.db))
                                            print(f"BEARISH ENGULFING DETECTED {ticker}")



                                    async for check_hammer in self.is_hammer(td9_df):
                                        if check_hammer == True:
                                            status = 'hammer'
                                            asyncio.create_task(candlestick_embed(hook=self.hammer_hooks.get(interval), timespan=timespan, status=status, ticker=ticker, df=lol_td9_df, db=self.db))
                                            print(f"HAMMER DETECTED {ticker}")


                                    soldiers_pattern_detected = await self.is_three_white_soldiers(td9_df)
                                    if soldiers_pattern_detected == True:
                                        status = 'bullish_soldiers'
                                        asyncio.create_task(candlestick_embed(hook="https://discord.com/api/webhooks/1244511042990768169/cD7NmOHJzvxOl81S7Uk3m6ScJFqrXVlyYOIOeEFyxGJfhW0RTnZ4P99MQd2qbf1d63zO", timespan=timespan, status=status, ticker=ticker, df=lol_td9_df, db=self.db))
                                        print("Three Black Crows pattern detected!")

                                    crows_pattern_detected = await self.is_three_black_crows(td9_df)
                                    if crows_pattern_detected == True:
                                        status = 'bearish_crows'
                                        asyncio.create_task(candlestick_embed(hook="https://discord.com/api/webhooks/1244511114960699474/cXrDi3nfa-9zm35heARDOv4xnGYuaOcjJb-V7ZgJuz_Y0pH_sZqv7fLaA071AJ1N0Qgf", timespan=timespan, status=status, ticker=ticker, df=lol_td9_df, db=self.db))
                                        print("Three White Soldiers pattern detected!")

                                                                                    
                                except Exception as e:
                                    print(f"Error processing ticker: {e}")        
                        else:
                            # Handle the case where the data is not in the expected format
                            print(f"No data available for {ticker} or unexpected response format.")
                            return None
                    except KeyError as e:
                        # Log the error
                        print(f"KeyError encountered while processing {ticker}: {e}")
                        return None
        except Exception as e:
            pass

    async def fetch_td9_for_timespan(self, ticker, timespan):
        status = None
        current_time = datetime.now()

        # Check if ticker was processed recently
        if ticker in self.processed_td9_tickers[timespan]:
            last_processed_time = self.processed_tickers[timespan][ticker]
            if (current_time - last_processed_time) < self.processing_interval:
                print(f"Skipping {ticker} for {timespan}, processed recently")
                return None


        try:

            td9_df = await self.async_get_td9(ticker, interval=timespan)
            print(td9_df)
        except Exception as e:
            print(f"Error processing ticker: {e}")
