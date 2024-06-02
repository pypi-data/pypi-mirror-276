
from fudstop.apis.polygonio.polygon_database import PolygonDatabase
from fudstop.apis.occ.occ_sdk import occSDK
occ = occSDK(host='localhost', user='chuck', password='fud', port=5432, database='market_data')
dictb =  PolygonDatabase(host='localhost', user='chuck', password='fud', port=5432, database='market_data')
import pandas as pd
import httpx
from webull_options.webull_options import WebullOptions
from fudstop.apis.webull.webull_trading import WebullTrading
import os
import asyncio
import json
from fudstop._markets.list_sets.dicts import healthcare,energy,etfs,real_estate,communication_services,consumer_cyclical,consumer_defensive,technology,industrials,basic_materials,financial_services,utilities
from dotenv import load_dotenv
load_dotenv()
class OptionsData:
    def __init__(self):
        self.db = PolygonDatabase(host='localhost', user='chuck', password='fud', port=5432, database='market_data')
        self.opts = WebullOptions(database='market_data')
        self.trading = WebullTrading()
        self.all_tickers = healthcare+energy+etfs+real_estate+communication_services+consumer_cyclical+consumer_defensive+ technology+ industrials+ basic_materials+ financial_services+ utilities
        self.headers = {
        "Accept": os.environ.get('ACCEPT', '*/*'),
        "Accept-Encoding": os.environ.get('ACCEPT_ENCODING', 'gzip, deflate, br, zstd'),
        "Accept-Language": os.environ.get('ACCEPT_LANGUAGE', 'en-US,en;q=0.9'),
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

    async def run_query(self, query) -> pd.DataFrame:
        """Runs asyncpg query and executes """

        results = await self.db.fetch(query)

        # Assuming `self.db.fetch` returns a list of dictionaries
        if results:
            columns = results[0].keys()
        else:
            columns = []
        df = pd.DataFrame(results, columns=columns)

        return df
    
    async def get_sentiment_score(self, ticker: str) -> float:
        await self.db.connect()

        query = f"""
            SELECT sentiment
            FROM public.info
            WHERE ticker = '{ticker}'
        """

        df = await self.run_query(query)

        if not df.empty:
            sentiment = df['sentiment'].iloc[0]
            return self.map_sentiment_to_score(sentiment)
        return 0.0

    def map_sentiment_to_score(self, sentiment: str) -> float:
        sentiment_mapping = {
            'Strong bullish': 1.0,
            'Bullish': 0.75,
            'Moderately bullish': 0.5,
            'Neutral': 0.0,
            'Moderately bearish': -0.5,
            'Bearish': -0.75,
            'Strong bearish': -1.0
        }
        return sentiment_mapping.get(sentiment, 0.0)

    async def get_price_change(self, ticker: str) -> float:
        await self.db.connect()

        query = f"""
            SELECT change_percent
            FROM public.info
            WHERE ticker = '{ticker}'
        """

        df = await self.run_query(query)

        if not df.empty:
            return df['change_percent'].iloc[0]
        return 0.0

    async def get_price_change(self, ticker: str) -> float:
        await self.db.connect()

        query = f"""
            SELECT change_percent
            FROM public.info
            WHERE ticker = '{ticker}'
        """

        df = await self.run_query(query)

        if not df.empty:
            return df['change_percent'].iloc[0]
        return 0.0

    async def high_iv_percentile(self) -> pd.DataFrame:
        await self.db.connect()

        query = f"""-- Check high implied volatility percentile
            WITH sentiment_mapping AS (
                SELECT
                    ticker,
                    price,
                    ivp30,
                    ivp60,
                    ivp90,
                    CASE
                        WHEN sentiment = 'Strong bullish' THEN 1.0
                        WHEN sentiment = 'Bullish' THEN 0.75
                        WHEN sentiment = 'Moderately bullish' THEN 0.5
                        WHEN sentiment = 'Neutral' THEN 0.0
                        WHEN sentiment = 'Moderately bearish' THEN -0.5
                        WHEN sentiment = 'Bearish' THEN -0.75
                        WHEN sentiment = 'Strong bearish' THEN -1.0
                        ELSE 0.0 -- Default for any unexpected values
                    END AS sentiment_score
                FROM
                    public.info
            )
            SELECT
                ticker AS high_iv_percentile
            FROM
                sentiment_mapping
            WHERE
                ivp30 > 80 OR ivp60 > 80 OR ivp90 > 80;"""

        df = await self.run_query(query)

        return df  


    async def high_iv_rank(self) -> pd.DataFrame:
        await self.db.connect()

        query = f"""-- Check high implied volatility rank
            WITH sentiment_mapping AS (
                SELECT
                    ticker,
                    price,
                    ivr30,
                    ivr60,
                    ivr90,
                    CASE
                        WHEN sentiment = 'Strong bullish' THEN 1.0
                        WHEN sentiment = 'Bullish' THEN 0.75
                        WHEN sentiment = 'Moderately bullish' THEN 0.5
                        WHEN sentiment = 'Neutral' THEN 0.0
                        WHEN sentiment = 'Moderately bearish' THEN -0.5
                        WHEN sentiment = 'Bearish' THEN -0.75
                        WHEN sentiment = 'Strong bearish' THEN -1.0
                        ELSE 0.0 -- Default for any unexpected values
                    END AS sentiment_score
                FROM
                    public.info
            )
            SELECT
                ticker AS high_iv_rank
            FROM
                sentiment_mapping
            WHERE
                ivr30 > 80 OR ivr60 > 80 OR ivr90 > 80;"""

        df = await self.run_query(query)

        return df

    async def low_correlation(self) -> pd.DataFrame:
        await self.db.connect()

        query = f"""-- Check low correlation
            WITH sentiment_mapping AS (
                SELECT
                    ticker,
                    price,
                    corr30d,
                    corr60d,
                    corr90d,
                    CASE
                        WHEN sentiment = 'Strong bullish' THEN 1.0
                        WHEN sentiment = 'Bullish' THEN 0.75
                        WHEN sentiment = 'Moderately bullish' THEN 0.5
                        WHEN sentiment = 'Neutral' THEN 0.0
                        WHEN sentiment = 'Moderately bearish' THEN -0.5
                        WHEN sentiment = 'Bearish' THEN -0.75
                        WHEN sentiment = 'Strong bearish' THEN -1.0
                        ELSE 0.0 -- Default for any unexpected values
                    END AS sentiment_score
                FROM
                    public.info
            )
            SELECT
                ticker AS low_correlation
            FROM
                sentiment_mapping
            WHERE
                corr30d < 0.2 OR corr60d < 0.2 OR corr90d < 0.2;"""

        df = await self.run_query(query)

        return df
    
    async def high_hv_parkinsons(self) -> pd.DataFrame:
        await self.db.connect()

        query = f"""-- Check high historical volatility Parkinson (HVP)
            WITH sentiment_mapping AS (
                SELECT
                    ticker,
                    price,
                    hvp30,
                    hvp60,
                    hvp90,
                    CASE
                        WHEN sentiment = 'Strong bullish' THEN 1.0
                        WHEN sentiment = 'Bullish' THEN 0.75
                        WHEN sentiment = 'Moderately bullish' THEN 0.5
                        WHEN sentiment = 'Neutral' THEN 0.0
                        WHEN sentiment = 'Moderately bearish' THEN -0.5
                        WHEN sentiment = 'Bearish' THEN -0.75
                        WHEN sentiment = 'Strong bearish' THEN -1.0
                        ELSE 0.0 -- Default for any unexpected values
                    END AS sentiment_score
                FROM
                    public.info
            )
            SELECT
                ticker AS high_hv_parkinsons
            FROM
                sentiment_mapping
            WHERE
                hvp30 > 80 OR hvp60 > 80 OR hvp90 > 80;"""

        df = await self.run_query(query)

        return df


    async def high_volatility_positive_sentiment(self) -> pd.DataFrame:
        """
        Check for tickers with high implied volatility (IV) and positive sentiment.

        Conditions:
        - IV30, IV60, or IV90 > 80
        - Sentiment score > 0.5

        Returns:
            pd.DataFrame: Tickers meeting the conditions.
        """
        await self.db.connect()

        query = f"""-- Check high volatility and positive sentiment
            WITH sentiment_mapping AS (
                SELECT
                    ticker,
                    price,
                    ivx30,
                    ivx60,
                    ivx90,
                    sentiment,
                    CASE
                        WHEN sentiment = 'Strong bullish' THEN 1.0
                        WHEN sentiment = 'Bullish' THEN 0.75
                        WHEN sentiment = 'Moderately bullish' THEN 0.5
                        WHEN sentiment = 'Neutral' THEN 0.0
                        WHEN sentiment = 'Moderately bearish' THEN -0.5
                        WHEN sentiment = 'Bearish' THEN -0.75
                        WHEN sentiment = 'Strong bearish' THEN -1.0
                        ELSE 0.0 -- Default for any unexpected values
                    END AS sentiment_score
                FROM
                    public.info
            )
            SELECT
                ticker AS high_volatility_positive_sentiment
            FROM
                sentiment_mapping
            WHERE
                (ivx30 > 80 OR ivx60 > 80 OR ivx90 > 80)
                AND sentiment_score > 0.5;"""

        df = await self.run_query(query)

        return df
    


    async def low_beta_high_iv_percentile(self) -> pd.DataFrame:
        """
        Check for tickers with low beta and high implied volatility percentile (IVP).

        Conditions:
        - Beta120d < 1
        - IVP30, IVP60, or IVP90 > 80

        Returns:
            pd.DataFrame: Tickers meeting the conditions.
        """
        await self.db.connect()

        query = f"""-- Check low beta and high implied volatility percentile
            WITH sentiment_mapping AS (
                SELECT
                    ticker,
                    price,
                    beta120d,
                    ivp30,
                    ivp60,
                    ivp90,
                    CASE
                        WHEN sentiment = 'Strong bullish' THEN 1.0
                        WHEN sentiment = 'Bullish' THEN 0.75
                        WHEN sentiment = 'Moderately bullish' THEN 0.5
                        WHEN sentiment = 'Neutral' THEN 0.0
                        WHEN sentiment = 'Moderately bearish' THEN -0.5
                        WHEN sentiment = 'Bearish' THEN -0.75
                        WHEN sentiment = 'Strong bearish' THEN -1.0
                        ELSE 0.0 -- Default for any unexpected values
                    END AS sentiment_score
                FROM
                    public.info
            )
            SELECT
                ticker AS low_beta_high_iv_percentile
            FROM
                sentiment_mapping
            WHERE
                beta120d < 1
                AND (ivp30 > 80 OR ivp60 > 80 OR ivp90 > 80);"""

        df = await self.run_query(query)

        return df

    async def low_beta_high_iv_percentile(self) -> pd.DataFrame:
        await self.db.connect()

        query = f"""-- Check low beta and high implied volatility percentile
            WITH sentiment_mapping AS (
                SELECT
                    ticker,
                    price,
                    beta120d,
                    ivp30,
                    ivp60,
                    ivp90,
                    CASE
                        WHEN sentiment = 'Strong bullish' THEN 1.0
                        WHEN sentiment = 'Bullish' THEN 0.75
                        WHEN sentiment = 'Moderately bullish' THEN 0.5
                        WHEN sentiment = 'Neutral' THEN 0.0
                        WHEN sentiment = 'Moderately bearish' THEN -0.5
                        WHEN sentiment = 'Bearish' THEN -0.75
                        WHEN sentiment = 'Strong bearish' THEN -1.0
                        ELSE 0.0 -- Default for any unexpected values
                    END AS sentiment_score
                FROM
                    public.info
            )
            SELECT
                ticker AS low_beta_high_iv_percentile
            FROM
                sentiment_mapping
            WHERE
                beta120d < 1
                AND (ivp30 > 80 OR ivp60 > 80 OR ivp90 > 80);"""

        df = await self.run_query(query)

        return df

    async def high_option_interest_positive_price_change(self) -> pd.DataFrame:
        """
        Check for tickers with high open interest and a positive price change.

        Conditions:
        - Open interest > 100,000
        - Change percent > 0

        Returns:
            pd.DataFrame: Tickers meeting the conditions.
        """
        await self.db.connect()

        query = f"""-- Check high option interest and positive price change
            WITH sentiment_mapping AS (
                SELECT
                    ticker,
                    price,
                    open_interest,
                    change_percent,
                    CASE
                        WHEN sentiment = 'Strong bullish' THEN 1.0
                        WHEN sentiment = 'Bullish' THEN 0.75
                        WHEN sentiment = 'Moderately bullish' THEN 0.5
                        WHEN sentiment = 'Neutral' THEN 0.0
                        WHEN sentiment = 'Moderately bearish' THEN -0.5
                        WHEN sentiment = 'Bearish' THEN -0.75
                        WHEN sentiment = 'Strong bearish' THEN -1.0
                        ELSE 0.0 -- Default for any unexpected values
                    END AS sentiment_score
                FROM
                    public.info
            )
            SELECT
                ticker AS high_option_interest_positive_price_change
            FROM
                sentiment_mapping
            WHERE
                open_interest > 100000
                AND change_percent > 0;"""

        df = await self.run_query(query)

        return df


    async def low_hv_high_iv_rank(self) -> pd.DataFrame:
        await self.db.connect()

        query = f"""-- Check low historical volatility and high implied volatility rank
            WITH sentiment_mapping AS (
                SELECT
                    ticker,
                    price,
                    hv30,
                    hv60,
                    hv90,
                    ivr30,
                    ivr60,
                    ivr90,
                    CASE
                        WHEN sentiment = 'Strong bullish' THEN 1.0
                        WHEN sentiment = 'Bullish' THEN 0.75
                        WHEN sentiment = 'Moderately bullish' THEN 0.5
                        WHEN sentiment = 'Neutral' THEN 0.0
                        WHEN sentiment = 'Moderately bearish' THEN -0.5
                        WHEN sentiment = 'Bearish' THEN -0.75
                        WHEN sentiment = 'Strong bearish' THEN -1.0
                        ELSE 0.0 -- Default for any unexpected values
                    END AS sentiment_score
                FROM
                    public.info
            )
            SELECT
                ticker AS low_hv_high_iv_rank
            FROM
                sentiment_mapping
            WHERE
                (hv30 < 30 AND ivr30 > 80)
                OR (hv60 < 30 AND ivr60 > 80)
                OR (hv90 < 30 AND ivr90 > 80);"""

        df = await self.run_query(query)

        return df



    async def high_eps_low_pe_in_industry(self, industry: str) -> pd.DataFrame:
        """
        Check for tickers with high EPS and low P/E ratio in a specific industry.

        Conditions:
        - EPS > 5
        - P/E < 15
        - Industry matches the provided industry

        Args:
            industry (str): The industry to filter by.

        Returns:
            pd.DataFrame: Tickers meeting the conditions.
        """
        await self.db.connect()

        query = f"""-- Check high EPS and low P/E ratio in a specific industry
            WITH sentiment_mapping AS (
                SELECT
                    ticker,
                    price,
                    eps,
                    pe,
                    industry,
                    CASE
                        WHEN sentiment = 'Strong bullish' THEN 1.0
                        WHEN sentiment = 'Bullish' THEN 0.75
                        WHEN sentiment = 'Moderately bullish' THEN 0.5
                        WHEN sentiment = 'Neutral' THEN 0.0
                        WHEN sentiment = 'Moderately bearish' THEN -0.5
                        WHEN sentiment = 'Bearish' THEN -0.75
                        WHEN sentiment = 'Strong bearish' THEN -1.0
                        ELSE 0.0 -- Default for any unexpected values
                    END AS sentiment_score
                FROM
                    public.info
            )
            SELECT
                ticker AS high_eps_low_pe_in_industry
            FROM
                sentiment_mapping
            WHERE
                eps > 5
                AND pe < 15
                AND industry = '{industry}';"""

        df = await self.run_query(query)

        return df



    async def high_pe_in_industry(self, industry: str) -> pd.DataFrame:
        await self.db.connect()

        query = f"""-- Check high P/E ratio in a specific industry
            WITH sentiment_mapping AS (
                SELECT
                    ticker,
                    price,
                    pe,
                    industry,
                    CASE
                        WHEN sentiment = 'Strong bullish' THEN 1.0
                        WHEN sentiment = 'Bullish' THEN 0.75
                        WHEN sentiment = 'Moderately bullish' THEN 0.5
                        WHEN sentiment = 'Neutral' THEN 0.0
                        WHEN sentiment = 'Moderately bearish' THEN -0.5
                        WHEN sentiment = 'Bearish' THEN -0.75
                        WHEN sentiment = 'Strong bearish' THEN -1.0
                        ELSE 0.0 -- Default for any unexpected values
                    END AS sentiment_score
                FROM
                    public.info
            )
            SELECT
                ticker AS high_pe_in_industry
            FROM
                sentiment_mapping
            WHERE
                pe > 20 AND industry = '{industry}';"""

        df = await self.run_query(query)

        return df

    async def high_option_volume(self) -> pd.DataFrame:
        await self.db.connect()

        query = f"""-- Check high option volume relative to average option volume
            WITH sentiment_mapping AS (
                SELECT
                    ticker,
                    price,
                    avg_opt_vol_1mo,
                    opt_vol,
                    CASE
                        WHEN sentiment = 'Strong bullish' THEN 1.0
                        WHEN sentiment = 'Bullish' THEN 0.75
                        WHEN sentiment = 'Moderately bullish' THEN 0.5
                        WHEN sentiment = 'Neutral' THEN 0.0
                        WHEN sentiment = 'Moderately bearish' THEN -0.5
                        WHEN sentiment = 'Bearish' THEN -0.75
                        WHEN sentiment = 'Strong bearish' THEN -1.0
                        ELSE 0.0 -- Default for any unexpected values
                    END AS sentiment_score
                FROM
                    public.info
            ),
            average_values AS (
                SELECT
                    AVG(opt_vol) AS avg_opt_vol
                FROM
                    sentiment_mapping
            )
            SELECT
                ticker AS high_option_volume
            FROM
                sentiment_mapping, average_values
            WHERE
                opt_vol > avg_opt_vol;"""

        df = await self.run_query(query)

        return df


    async def high_call_volume(self) -> pd.DataFrame:
        await self.db.connect()

        query = f"""-- Check high call volume
            WITH sentiment_mapping AS (
                SELECT
                    ticker,
                    price,
                    ivx30,
                    ivx30_chg,
                    call_vol,
                    change_percent,
                    beta120d,
                    hv30,
                    CASE
                        WHEN sentiment = 'Strong bullish' THEN 1.0
                        WHEN sentiment = 'Bullish' THEN 0.75
                        WHEN sentiment = 'Moderately bullish' THEN 0.5
                        WHEN sentiment = 'Neutral' THEN 0.0
                        WHEN sentiment = 'Moderately bearish' THEN -0.5
                        WHEN sentiment = 'Bearish' THEN -0.75
                        WHEN sentiment = 'Strong bearish' THEN -1.0
                        ELSE 0.0 -- Default for any unexpected values
                    END AS sentiment_score
                FROM
                    public.info
            ),
            average_values AS (
                SELECT
                    AVG(call_vol) AS avg_call_vol
                FROM
                    sentiment_mapping
            )
            SELECT
                ticker AS high_call_volume
            FROM
                sentiment_mapping, average_values
            WHERE
                call_vol > avg_call_vol;"""

        df = await self.run_query(query)

        return df
    
    async def positive_price_change(self) -> pd.DataFrame:
        await self.db.connect()

        query = f"""-- Check positive price change
            WITH sentiment_mapping AS (
                SELECT
                    ticker,
                    price,
                    ivx30,
                    ivx30_chg,
                    call_vol,
                    change_percent,
                    beta120d,
                    hv30,
                    CASE
                        WHEN sentiment = 'Strong bullish' THEN 1.0
                        WHEN sentiment = 'Bullish' THEN 0.75
                        WHEN sentiment = 'Moderately bullish' THEN 0.5
                        WHEN sentiment = 'Neutral' THEN 0.0
                        WHEN sentiment = 'Moderately bearish' THEN -0.5
                        WHEN sentiment = 'Bearish' THEN -0.75
                        WHEN sentiment = 'Strong bearish' THEN -1.0
                        ELSE 0.0 -- Default for any unexpected values
                    END AS sentiment_score
                FROM
                    public.info
            )
            SELECT
                ticker AS positive_price_change
            FROM
                sentiment_mapping
            WHERE
                change_percent > 0;"""

        df = await self.run_query(query)

        return df


    async def positive_sentiment(self) -> pd.DataFrame:
        await self.db.connect()

        query = f"""-- Check positive sentiment
            WITH sentiment_mapping AS (
                SELECT
                    ticker,
                    price,
                    ivx30,
                    ivx30_chg,
                    call_vol,
                    change_percent,
                    beta120d,
                    hv30,
                    CASE
                        WHEN sentiment = 'Strong bullish' THEN 1.0
                        WHEN sentiment = 'Bullish' THEN 0.75
                        WHEN sentiment = 'Moderately bullish' THEN 0.5
                        WHEN sentiment = 'Neutral' THEN 0.0
                        WHEN sentiment = 'Moderately bearish' THEN -0.5
                        WHEN sentiment = 'Bearish' THEN -0.75
                        WHEN sentiment = 'Strong bearish' THEN -1.0
                        ELSE 0.0 -- Default for any unexpected values
                    END AS sentiment_score
                FROM
                    public.info
            )
            SELECT
                ticker AS positive_sentiment
            FROM
                sentiment_mapping
            WHERE
                sentiment_score > 0.5;"""

        df = await self.run_query(query)

        return df
    
    async def low_historical_volatility(self) -> pd.DataFrame:
        await self.db.connect()

        query = f"""-- Check low historical volatility
            WITH sentiment_mapping AS (
                SELECT
                    ticker,
                    price,
                    ivx30,
                    ivx30_chg,
                    call_vol,
                    change_percent,
                    beta120d,
                    hv30,
                    CASE
                        WHEN sentiment = 'Strong bullish' THEN 1.0
                        WHEN sentiment = 'Bullish' THEN 0.75
                        WHEN sentiment = 'Moderately bullish' THEN 0.5
                        WHEN sentiment = 'Neutral' THEN 0.0
                        WHEN sentiment = 'Moderately bearish' THEN -0.5
                        WHEN sentiment = 'Bearish' THEN -0.75
                        WHEN sentiment = 'Strong bearish' THEN -1.0
                        ELSE 0.0 -- Default for any unexpected values
                    END AS sentiment_score
                FROM
                    public.info
            ),
            average_values AS (
                SELECT
                    AVG(hv30) AS avg_hv30
                FROM
                    sentiment_mapping
            )
            SELECT
                ticker AS low_hv
            FROM
                sentiment_mapping, average_values
            WHERE
                hv30 < avg_hv30;"""

        df = await self.run_query(query)

        return df

    async def high_beta(self) -> pd.DataFrame:
        await self.db.connect()

        query = f"""-- Check high beta
            WITH sentiment_mapping AS (
                SELECT
                    ticker,
                    price,
                    ivx30,
                    ivx30_chg,
                    call_vol,
                    change_percent,
                    beta120d,
                    hv30,
                    CASE
                        WHEN sentiment = 'Strong bullish' THEN 1.0
                        WHEN sentiment = 'Bullish' THEN 0.75
                        WHEN sentiment = 'Moderately bullish' THEN 0.5
                        WHEN sentiment = 'Neutral' THEN 0.0
                        WHEN sentiment = 'Moderately bearish' THEN -0.5
                        WHEN sentiment = 'Bearish' THEN -0.75
                        WHEN sentiment = 'Strong bearish' THEN -1.0
                        ELSE 0.0 -- Default for any unexpected values
                    END AS sentiment_score
                FROM
                    public.info
            )
            SELECT
                ticker AS high_beta
            FROM
                sentiment_mapping
            WHERE
                beta120d > 1;"""

        df = await self.run_query(query)

        return df
    async def iv_below_avg(self) -> pd.DataFrame:
        await self.db.connect()

        query = f"""-- Check IV below average
            WITH sentiment_mapping AS (
                SELECT
                    ticker,
                    price,
                    ivx30,
                    ivx30_chg,
                    call_vol,
                    change_percent,
                    beta120d,
                    hv30,
                    CASE
                        WHEN sentiment = 'Strong bullish' THEN 1.0
                        WHEN sentiment = 'Bullish' THEN 0.75
                        WHEN sentiment = 'Moderately bullish' THEN 0.5
                        WHEN sentiment = 'Neutral' THEN 0.0
                        WHEN sentiment = 'Moderately bearish' THEN -0.5
                        WHEN sentiment = 'Bearish' THEN -0.75
                        WHEN sentiment = 'Strong bearish' THEN -1.0
                        ELSE 0.0 -- Default for any unexpected values
                    END AS sentiment_score
                FROM
                    public.info
            ),
            average_values AS (
                SELECT
                    AVG(ivx30) AS avg_ivx30
                FROM
                    sentiment_mapping
            )
            SELECT
                ticker AS iv_below_avg
            FROM
                sentiment_mapping, average_values
            WHERE
                ivx30 < avg_ivx30;"""
        


        df = await self.run_query(query)

        return df

    async def get_all_options(self, ticker: str):

        """"""
        try:
            data, from_, opts = await self.opts.all_options(ticker)
            print(opts.as_dataframe)
            await self.db.batch_insert_dataframe(opts.as_dataframe, table_name='wb_opts', unique_columns='ticker,strike,cp,expiry')

            return opts.as_dataframe
        except Exception as e:
            print(e)


    async def options_monitor(self, ticker:str):

        monitor = await occ.options_monitor(ticker)

        return monitor


import asyncio
opt_data = OptionsData()
