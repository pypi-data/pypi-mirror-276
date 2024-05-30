from discord_webhook import DiscordEmbed, AsyncDiscordWebhook
from fudstop.apis.occ.occ_models import StockInfo
from fudstop._markets.list_sets.dicts import hex_color_dict
import os
from dotenv import load_dotenv
load_dotenv()
from fudstop.apis.polygonio.async_polygon_sdk import Polygon
from fudstop.apis.polygonio.polygon_database import PolygonDatabase
from fudstop.apis.webull.webull_trading import WebullTrading
import asyncio
db = PolygonDatabase(host='localhost', user='chuck', password='fud', port=5432, database='market_data')

import pandas as pd


async def rsi_embed(hook, ticker, status, timespan, rsi,underlying_data: dict, db):

    """Sends RSI feeds to discord."""

    webhook = AsyncDiscordWebhook(hook)
    color = hex_color_dict.get('red') if status == 'oversold' else hex_color_dict.get('green')
    print(color)
    embed = DiscordEmbed(title=f"RSI Feed - {ticker} | {timespan}", description=f"# > {ticker} | {status} | {timespan}\n```py\n{ticker} is currently trading with an RSI of {round(float(rsi),2)}.```", color=color)
    embed.add_embed_field(name='Latest Underlying:', value=f"> Open: **${underlying_data.get('open')[0]}**\n> High: **${underlying_data.get('high')[0]}**\n> Low: **${underlying_data.get('low')[0]}**\n> Close: **${underlying_data.get('close')[0]}**\n> VWAP: **${underlying_data.get('vwap')[0]}**\n\n> Volume: **{underlying_data.get('volume')[0]}**\n> Num Trades: **{underlying_data.get('num_trades')[0]}**")
    embed.set_footer(text='Implemented by FUDSTOP | Data by Polygon.io', icon_url = os.environ.get('fudstop_logo'))

    webhook.add_embed(embed)

    df = pd.DataFrame(underlying_data)
    df['ticker'] = ticker
    df['status'] = status
    df['timespan'] = timespan
    df['rsi'] = rsi
    await db.batch_insert_dataframe(df, table_name='rsi_feed', unique_columns='ticker, timespan, status')

    await webhook.execute()



async def macd_embed(hook, type, ticker, timespan, db):
    color = hex_color_dict.get('green') if type == 'bullish' else hex_color_dict.get('red')
    webhhook = AsyncDiscordWebhook(hook)

    embed = DiscordEmbed(title=f"MACD {type} - {ticker} | {timespan}", description=f"```py\n{ticker}'s MACD is about to cross {type} on the {timespan} timespan.```", color=color)
    embed.set_footer(text='Implemented by FUDSTOP | data by Polygon.io', icon_url = os.environ.get('fudstop_logo'))
    embed.set_timestamp()
    webhhook.add_embed(embed)

    data_dict = { 
        'ticker': ticker,
        'type': type,
        'timespan': timespan,

    }

    df=  pd.DataFrame(data_dict)

    await db.batch_insert_dataframe(df, table_name='macd_feed', unique_columns='ticker, timespan, type')

    await webhhook.execute()



async def cost_dist_embed(hook, status, ticker, profit_ratio, db):
    color = hex_color_dict.get('green') if status == 'bullish signal' else hex_color_dict.get('red')
    webhhook = AsyncDiscordWebhook(hook)

    embed = DiscordEmbed(title=f"PLAYERS PROFITING {status} - {ticker} | {profit_ratio}%", description=f"```py\n{profit_ratio}% of players are currently profiting for {ticker}. This is a {status} because the price is far from the average, which could lead to a sell-off in the near-term. Use with other metrics.```", color=color)
    embed.set_timestamp()
    webhhook.add_embed(embed)
    data_dict = { 
        'ticker': ticker,
        'status': status,
        'profit_ratio': profit_ratio
    }
    df = pd.DataFrame(data_dict, index=[0])
    await db.batch_insert_dataframe(df, table_name='cost_feed', unique_columns='ticker, status, profit_ratio')
    await webhhook.execute()



async def td9_embed(hook, timespan, status, ticker, df, db):
    color = hex_color_dict.get('green') if status == 'bullish_td9' else hex_color_dict.get('red')
    webhhook = AsyncDiscordWebhook(hook)

    embed = DiscordEmbed(title=f"{status} - {ticker} | {timespan} TD9", description=f"```py\n{df}```", color=color)
    embed.add_embed_field(name=f"TD9", value='> The TD9 is a reversal indicator. Pair with other indicators for increased likelihood of reversal - such as RSI.')
    embed.set_footer(icon_url=os.environ.get('fudstop_logo'), text='Implemented by FUDSTOP')
    embed.set_timestamp()
    webhhook.add_embed(embed)

    data_dict = { 
        'ticker': ticker,
        'timespan': timespan,
        'status': status,

    }
    df = pd.DataFrame(data_dict, index=[0])

    await db.batch_insert_dataframe(df, table_name='td9_feed', unique_columns='ticker, timespan, status')
    await webhhook.execute()



async def candlestick_embed(hook, timespan, status, ticker, df, db):
    color = hex_color_dict.get('green') if 'bullish' in status else hex_color_dict.get('red')
    webhhook = AsyncDiscordWebhook(hook)

    embed = DiscordEmbed(title=f"{status} - {ticker} | {timespan}", description=f"```py\n{df}```", color=color)
    embed.add_embed_field(name=f"{status}", value='> TO DO.')
    embed.set_footer(icon_url=os.environ.get('fudstop_logo'), text='Implemented by FUDSTOP')
    embed.set_timestamp()
    webhhook.add_embed(embed)

    data_dict = { 
        'ticker': ticker,
        'timespan': timespan,
        'pattern': status,


    }
    df = pd.DataFrame(data_dict, index=[0])
    await db.batch_insert_dataframe(df, table_name='candle_feed', unique_columns='ticker, timespan, pattern')
    await webhhook.execute()




async def option_embed(hook,ticker, strike, cp, expiry, volume, oi, condition, price, bid, mid, ask, chg_pct):
    color = hex_color_dict.get('green') if 'call' in cp else hex_color_dict.get('red')
    webhhook = AsyncDiscordWebhook(hook)

    embed = DiscordEmbed(title=f"High⚡Volume - {ticker} | {strike} | {cp} | {expiry}", description=f"> VOL: **{volume}** vs. OI: **{oi}**", color=color)
    embed.add_embed_field(name=f"Underlying:", value=f"Price: **${price}**", inline=False)
    embed.add_embed_field(name=f"Contract:", value=f"> Bid: **${bid}**\n> Mid: **${mid}**\n> Ask: **${ask}**\n> Chg%: **{chg_pct}**")
    embed.add_embed_field(name=f"{condition}", value=f'> {condition}')
    embed.set_footer(icon_url=os.environ.get('fudstop_logo'), text='Implemented by FUDSTOP')
    embed.set_timestamp()
    webhhook.add_embed(embed)

    await webhhook.execute()



async def volatility_embed(hook,info:StockInfo, status, ticker):
    try:
        color = hex_color_dict.get('orange')
        webhhook = AsyncDiscordWebhook(hook)

        embed = DiscordEmbed(title=f"{status} - {ticker}", description=f"```py\nVolatility levels are {status} for {ticker}.\n\n{ticker}'s current price is ${info.price}. Its 52 week high is ${info.highPrice52Wk} and its 52 week low is ${info.lowPrice52Wk}```", color=color)

        embed.add_embed_field(name=f"{ticker}'s Day Stats:", value=f"> Open: **${info.open}\n> High: **${info.high}**\n> Low: **${info.low}**\n> Close: **${info.price}**\n> Prev. Close: **${info.prevClose}**\n> Change%: **{info.changePercent}**")
        try:
            embed.add_embed_field(name=f"Stock Info:", value=f"> Beta60d: **{round(float(info.beta60D),2)}**\n> Correlation: **{round(float(info.corr60D),2)}**\n> Iv Pct 60d: **{round(float(info.ivp60),2)}**\n> Iv Rank 60d: **{round(float(info.ivr60),2)}**\n> Hist. Volatility60d: **{round(float(info.hv60),2)}**")
        except Exception as e:
            print(e)
        embed.add_embed_field(name=f"Stock Spread", value=f"> Bid: **${info.bid}**\n> Ask: **${info.ask}**")
        embed.add_embed_field(name=f"Options Info:", value=f"Call Vol: **{info.callVol}**\n> Put Vol: **{info.putVol}**\n> Total Vol: **{info.optVol}**\n> 1M Avg: **{info.avgOptVol1MO}**\n\n> Total OI: **{info.openInterest}**\n> 1M AVG: **{info.avgOptOI1MO}**")


        embed.set_footer(icon_url=os.environ.get('fudstop_logo'), text='Implemented by FUDSTOP')
        embed.set_timestamp()
        webhhook.add_embed(embed)

        await webhhook.execute()
    except Exception as e:
        print(e)