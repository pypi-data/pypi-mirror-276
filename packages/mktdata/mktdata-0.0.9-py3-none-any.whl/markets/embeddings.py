from discord_webhook import AsyncDiscordWebhook, DiscordEmbed
import asyncio
import disnake
from fudstop._markets.list_sets.dicts import hex_color_dict
import os
from dotenv import load_dotenv
load_dotenv()

special_hook = os.environ.get('specials_2')

async def specials(whale_df, components:dict):
    


    underlying_symbol = components.get('underlying_symbol')
    strike = components.get('strike_price')
    expiry= components.get('expiry_date')
    cp = components.get('call_put')
    for i, row in whale_df.iterrows():
        try:
            ask_vol = row['ask_volume']
            bid_vol = row['bid_volume']
            cross_vol = row['cross_volume']
            date = row['date']
            oi = row['open_interest']
            floor_vol = row['floor_volume']
            high_price = row['high_price']
            low_price = row['low_price']
            sweep_vol = row['sweep_volume']
            multi_let = row['multi_leg_volume']
            stock_multi = row['stock_multi_leg_volume']
            iv_high = round(float(row['iv_high'])*100,2) if row['iv_high'] is not None else 0
            iv_low = round(float(row['iv_low'])*100,2) if row['iv_low'] is not None else 0
            total_prem = row['total_premium']
            trades = row['trades']
            volume = row['volume']
            mid_vol = row['mid_volume']
            last_price = round(float(row['last_price']),2) if row['last_price'] is not None else 0
            avg_price = row['avg_price']
            avg_price = round(float(avg_price),ndigits=4) if avg_price is not None else 0
            iv = round(float(row['implied_volatility'])*100,2) if row['implied_volatility'] is not None else 0
            iv_midpoint = (iv_high + iv_low) / 2
            is_iv_closer_to_low = iv < iv_midpoint

            # Check if the average price deviates significantly from the last price
            # Define a threshold for significant deviation, e.g., 5%
            significant_deviation_threshold = 0.35  # 5 percent
            price_deviation = abs(last_price - avg_price) / last_price

            is_price_significantly_lower = avg_price >= last_price and price_deviation > significant_deviation_threshold

            # More complex conditions combining several factors
            if volume > oi and ask_vol > (bid_vol * 1.5):
                # Implement the actions or analysis to be done when conditions are met
        
            # Add any specific processing logic here



                embed = DiscordEmbed(title=f"🌩️ SPECIAL - {underlying_symbol} | {strike} | {cp} | {expiry} 🌩️", description=f"# > VOLUME BREAKDOWN:\n\n```py\nBuy: **{ask_vol}** Sell: **{bid_vol}**\n\nSweep: **{sweep_vol}**\n> Cross: **{cross_vol}**\nMid: **{mid_vol}**\nFloor: **{floor_vol}**\nMulti: **{multi_let}** StockMulti: **{stock_multi}**\n\nTOTAL: {volume} vs {oi} OI", color=hex_color_dict.get('gold'))

                embed.add_embed_field(name=f"Date:", value=f"> **{date}**", inline=False)

                embed.add_embed_field(name=f"Total Premium:", value=f"> **${total_prem}**\n> Trades: **{trades}**")
                embed.add_embed_field(name=f"IV:", value=f"> Low IV: **{iv_high}**\n> IV Now: **{iv}**\n> High IV: **{iv_low}**")
                embed.add_embed_field(name=f"Pricing:", value=f"> High: **${high_price}**\n> Now: **${last_price}**\n> Low: **${low_price}**")

                hook = AsyncDiscordWebhook(special_hook, content=f"@everyone")

                
                hook.add_embed(embed)
                embed.set_timestamp()
                await hook.execute()
        except Exception as e:
            print(e)



import disnake
from discord_webhook import DiscordEmbed, AsyncDiscordWebhook



async def multi_rsi(hook, ticker):

    webhook = AsyncDiscordWebhook(hook, content=f"{ticker} is oversold across the day, hour, and minute timeframe!")



    await webhook.execute()



async def rsi_feed(hook, ticker, rsi, status, timespan):
    color = hex_color_dict.get('green') if status == 'oversold' else hex_color_dict.get('red')
    webhhook = AsyncDiscordWebhook(hook)

    embed = DiscordEmbed(title=f"RSI {status} - {ticker} | {timespan}", description=f"```py\n{ticker} is currently {status} with an RSI of {rsi}.```", color=color)
    embed.set_footer(text='Implemented by FUDSTOP | data by Polygon.io', icon_url = os.environ.get('fudstop_logo'))
    embed.set_timestamp()
    webhhook.add_embed(embed)

    await webhhook.execute()


async def macd_feed(hook, type, ticker, timespan):
    color = hex_color_dict.get('green') if type == 'bullish' else hex_color_dict.get('red')
    webhhook = AsyncDiscordWebhook(hook)

    embed = DiscordEmbed(title=f"MACD {type} - {ticker} | {timespan}", description=f"```py\n{ticker}'s MACD is about to cross {type} on the {timespan} timespan.```", color=color)
    embed.set_footer(text='Implemented by FUDSTOP | data by Polygon.io', icon_url = os.environ.get('fudstop_logo'))
    embed.set_timestamp()
    webhhook.add_embed(embed)

    await webhhook.execute()




async def change_percent_feed(data):

    session_change = [i.get('session.change') for i in data]
    session_change_percent = [i.get('session.change_percent')  for i in data]
    session_early_trading_change = [i.get('session.early_trading_change')  for i in data]
    session_early_trading_change_percent = [i.get('session.early_trading_change_percent')  for i in data]
    session_close = [i.get('session.close')  for i in data]
    session_high = [i.get('session.high')  for i in data]
    session_low = [i.get('session.low')  for i in data]
    session_open = [i.get('session.open')  for i in data]
    session_volume = [i.get('session.volume')  for i in data]
    session_previous_close = [i.get('session.previous_close')  for i in data]
    details_contract_type = [i.get('details.contract_type')  for i in data]
    details_exercise_style = [i.get('details.exercise_style')  for i in data]
    details_expiration_date = [i.get('details.expiration_date')  for i in data]
    details_shares_per_contract = [i.get('details.shares_per_contract')  for i in data]
    details_strike_price = [i.get('details.strike_price')  for i in data]
    greeks_delta = [i.get('greeks.delta')  for i in data]
    greeks_gamma = [i.get('greeks.gamma')  for i in data]
    greeks_theta = [i.get('greeks.theta')  for i in data]
    greeks_vega = [i.get('greeks.vega')  for i in data]
    implied_volatility = [i.get('implied_volatility')  for i in data]
    last_quote_ask = [i.get('last_quote.ask')  for i in data]
    last_quote_ask_size = [i.get('last_quote.ask_size')  for i in data]
    last_quote_ask_exchange = [i.get('last_quote.ask_exchange')  for i in data]
    last_quote_bid = [i.get('last_quote.bid')  for i in data]
    last_quote_bid_size = [i.get('last_quote.bid_size')  for i in data]
    last_quote_bid_exchange = [i.get('last_quote.bid_exchange')  for i in data]
    last_quote_last_updated = [i.get('last_quote.last_updated')  for i in data]
    last_quote_midpoint = [i.get('last_quote.midpoint')  for i in data]
    last_quote_timeframe = [i.get('last_quote.timeframe')  for i in data]
    last_trade_sip_timestamp = [i.get('last_trade.sip_timestamp')  for i in data]
    last_trade_conditions = [i.get('last_trade.conditions')  for i in data]
    last_trade_price = [i.get('last_trade.price')  for i in data]
    last_trade_size = [i.get('last_trade.size')  for i in data]
    last_trade_exchange = [i.get('last_trade.exchange')  for i in data]
    last_trade_timeframe = [i.get('last_trade.timeframe')  for i in data]
    open_interest = [i.get('open_interest')  for i in data]
    underlying_asset_change_to_break_even = [i.get('underlying_asset.change_to_break_even')  for i in data]
    underlying_asset_last_updated = [i.get('underlying_asset.last_updated')  for i in data]
    underlying_asset_price = [i.get('underlying_asset.price')  for i in data]
    underlying_asset_ticker = [i.get('underlying_asset.ticker')  for i in data]
    underlying_asset_timeframe = [i.get('underlying_asset.timeframe')  for i in data]
    name = [i.get('name')  for i in data]
    market_status = [i.get('market_status')  for i in data]
    ticker = [i.get('ticker')  for i in data]



    hook = AsyncDiscordWebhook(os.environ.get('main_hook'))

    embed = DiscordEmbed(title=f"Change % - {name[0]} | {details_strike_price[0]} | {details_contract_type[0]} | {details_expiration_date[0]}")
    embed.add_embed_field(name='Greeks:', value=f"> Delta: **{round(float(greeks_delta[0]),2)}**\n> Theta: **{round(float(greeks_theta[0]),2)}**\n> Vega: **{round(float(greeks_vega[0]),2)}**\n> Gamma: **{round(float(greeks_gamma[0]),2)}**")
    embed.add_embed_field(name=f"Pricing:", value=f"> Ask: **${last_quote_ask[0]}**\n> Mid: **${last_quote_midpoint[0]}**\n> Bid: **${last_quote_bid[0]}**")
    embed.add_embed_field(name=f"Underlying:", value=f"> Price: **${underlying_asset_price}**\n> Change to Breakeven: **{underlying_asset_change_to_break_even[0]}**")
    embed.add_embed_field(name=f"Vol / OI:", value=f"> **{session_volume[0]}**// **{open_interest[0]}**")

    embed.add_embed_field(name=f"Day Stats:", value=f"> **${session_open[0]}**\n> High: **{session_high[0]}**\n> Low: **{session_low}**\n> Close: **{session_close[0]}**\n> Prev Close: **${session_previous_close[0]}**")

    embed.add_embed_field(name=f"Change%:", value=f"> **{session_change_percent[0]}%**")
    embed.set_timestamp()
    embed.set_footer(text='Implemented by FUDSTOP | Data by polygon.io', icon_url=os.environ.get('fudstop_logo'))
    hook.add_embed(embed)
    await hook.execute()