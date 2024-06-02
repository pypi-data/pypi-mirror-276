from imps import *
from discord_webhook import AsyncDiscordWebhook, DiscordEmbed
from fudstop.apis.webull.webull_trading import WebullTrading
from fudstop.apis.webull.webull_option_screener import WebullOptionScreener
from collections import deque
tape_dict = { 
    1: 'NYSE',
    2: 'AMEX',
    3: 'NASDAQ'
}
import pytz
spx_rsi_hook="https://discord.com/api/webhooks/1207045858105888808/kkXrxa9HwL8DEvnIFoWdcw1W7arOWs0zGn9Ss5MqhUPTm8S_qRL1otXXttxap15mvhe3"
c = WebSocketClient(subscriptions=["T.*, A.*"], api_key=os.environ.get('YOUR_POLYGON_KEY'), market=Market.Options)
from fudstop.apis.whale.whale_sdk import WhaleSDK
from datetime import timedelta
from typing import List
screener = WebullOptionScreener()
whale = WhaleSDK()
# Handler function
# Queue and dictionary to handle tickers
trading = WebullTrading()
ticker_queue = asyncio.Queue()
ticker_last_processed = {}
# Function to process subsequent trades
# Dictionary to track the last processed time for each symbol
# Dictionary to track the trades for each symbol
trade_tracker = {}

# Define the maximum number of successive trades to capture
max_successive_trades = 5

# Define the time window within which successive trades are considered
time_window = timedelta(seconds=10)  # Adjust this value as needed
async def screen(ticker, expiry_date, strike):
    pass


async def handle_option_trades(msgs):
    batch = []
    unique_symbols = set()
    for m in msgs:

        components = get_human_readable_string(m.symbol)
        expiry_date = datetime.strptime(components.get('expiry_date'), '%Y-%m-%d').date()
        # if m.event_type == 'T':
        
            

            

        #     ticker = components.get('underlying_symbol')
            
        #     insertion_dict = {
        #         'event': 'option_trade',
        #         'symbol': m.symbol,
        #         'ticker': components.get('underlying_symbol'),
        #         'strike': components.get('strike_price'),
        #         'call_put': components.get('call_put'),
        #         'expiry': expiry_date,
        #         'exchange': m.exchange,
        #         'price': m.price,
        #         'size': m.size,
        #         'conditions': m.conditions[0],
        #         'timestamp': m.timestamp  # Now a datetime object
        #     }

        #     # Prepare a SQL statement
        #     df = pd.DataFrame(insertion_dict, index=[0])
        #     asyncio.create_task(db.batch_insert_dataframe(df, table_name='option_trades', unique_columns='ticker, strike, call_put, expiry', batch_size=1000))

        if m.event_type == 'A':
            print(m)
            strike = components.get('strike_price')
            expiry = components.get('expiry_date')
            call_put = components.get('call_put')
            underlying_symbol = components.get('underlying_symbol')
            us_central = pytz.timezone('US/Central')
            utc = pytz.UTC
            # Check if the symbol was processed recently
            current_time = datetime.now(utc)
            agg_message_data = {}

            agg_message_data['type'] = 'EquityOptionAgg'
            agg_message_data['ticker'] = underlying_symbol
            agg_message_data['strike'] = strike
            agg_message_data['expiry'] = expiry
            agg_message_data['expiry']  = datetime.strptime(expiry, '%Y-%m-%d').date()
            agg_message_data['call_put'] = call_put
            agg_message_data['option_symbol'] = m.symbol
            agg_message_data['total_volume'] = m.accumulated_volume
            agg_message_data['volume'] = m.volume
            agg_message_data['day_vwap'] = m.aggregate_vwap
            agg_message_data['official_open'] = m.official_open_price
            agg_message_data['last_price'] = m.close
            agg_message_data['open'] = m.open
            agg_message_data['end_timestamp'] = m.end_timestamp
            agg_message_data['start_timestamp'] = m.start_timestamp
            df = pd.DataFrame(agg_message_data, index=[0])

            asyncio.create_task(db.batch_insert_dataframe(df, table_name='option_aggs', unique_columns='ticker, strike, call_put, expiry', batch_size=1000))

            if agg_message_data['volume'] >= 5000:
                try:
                    whsym = agg_message_data['option_symbol'].replace('O:', '')
                    
                    whales_data = await whale.historic_chains(whsym)

                    avgprice=whales_data.avg_price[0]
                    sellvol=whales_data.bid_volume[0]
                    crossvol=whales_data.cross_volume[0]
                    floorvol=whales_data.floor_volume[0]
                    highprice=whales_data.high_price[0]
                    lowprice=float(whales_data.low_price[0]) if whales_data.low_price[0] is not None else 0

                    contract_price = float(whales_data.last_price[0]) if whales_data.last_price[0] is not None else 0
                    buyvol = whales_data.ask_volume[0]
                    midvol= whales_data.mid_volume[0]
                    multivol=whales_data.multi_leg_volume[0]
                    stockmultivol=whales_data.stock_multi_leg_volume[0]
                    neutvol=whales_data.neutral_volume[0]
                    nosidevol=whales_data.no_side_volume[0]
                    oi =whales_data.open_interest[0]
                    sweepvol = whales_data.sweep_volume[0]
                    prem=whales_data.total_premium[0]
                    totalvol = whales_data.volume[0]
                    change_percent = ((contract_price - lowprice) / lowprice) * 100 if contract_price is not 0 and lowprice is not 0 else None
                    data_dict = { 
                        'option_symbol': agg_message_data['option_symbol'],
                        'price': contract_price,
                        'high_price': highprice,
                        'low_price': lowprice,
                        'change_percent': change_percent,
                        'ticker': underlying_symbol,
                        'strike': strike,
                        'call_put': call_put,
                        'expiry': expiry,      
                        'avg_price': avgprice,
                        'oi': oi,
                        'total_vol': totalvol,
                        'buy_vol': buyvol,
                        'mid_vol': midvol,
                        'sell_vol': sellvol,
                        'no_side_vol': nosidevol,
                        'neut_vol': neutvol,
                        'sweep_vol': sweepvol,
                        'floor_vol': floorvol,
                        'multi_vol': multivol,
                        'stock_multi_vol': stockmultivol,
                        

                                                   }
                    df = pd.DataFrame(data_dict, index=[0])

                    await db.batch_insert_dataframe(df, table_name='specials', unique_columns='option_symbol')

                    if (buyvol > oi or sweepvol > oi) and (contract_price == lowprice or abs(contract_price - lowprice) <= 0.35 * lowprice) and buyvol > sellvol:


                        embed = DiscordEmbed(title=f"⚡SPECIALS!⚡", description=f"```py\n{agg_message_data['ticker']} | ${strike} | {call_put} | {expiry}```\n# > Vol Breakdown:\n\n> Buy: **{buyvol}** | Mid: **{midvol}** Sell: **{sellvol}**\n> Sweep: **{sweepvol}** Cross: **{crossvol}**\n> Multi: **{multivol}** Stock Multi: **{stockmultivol}**\n> Neut: **{neutvol}** No Side: **{nosidevol}**\n> FLoor: **{floorvol}**\n> Total: **{whales_data.volume[0]}** vs **{oi}** OI.",color=hex_color_dict.get('blue'))

                        embed.add_embed_field(name=f"Contract Price:", value=f"> High: **${highprice}**\n> Now: **${contract_price}**\n> Low: **${lowprice}**\n> Avg: **${avgprice}**")
                        embed.add_embed_field(name=f"Premium:", value=f"> **${prem}**")

                        hook = AsyncDiscordWebhook("https://discord.com/api/webhooks/1207045858105888808/kkXrxa9HwL8DEvnIFoWdcw1W7arOWs0zGn9Ss5MqhUPTm8S_qRL1otXXttxap15mvhe3", content="@everyone")

                        hook.add_embed(embed)

                        await hook.execute()
                except Exception as e:
                    print(e)




def convert_timestamp(timestamp_ms):
    timestamp_seconds = timestamp_ms / 1000.0
    utc_datetime = datetime.fromtimestamp(timestamp_seconds, tz=timezone.utc)
    eastern_datetime = utc_datetime.astimezone(ZoneInfo("America/New_York"))
    return eastern_datetime.strftime('%Y-%m-%d %H:%M:%S')

async def main():
    while True:
        try:
            await db.connect()



            # Connect and set up the message handling
            await c.connect(lambda msgs: asyncio.create_task(handle_option_trades(msgs)))

            # Keep the connection alive
            while True:
                await asyncio.sleep(1)  # Adjust the sleep time as needed

        except Exception as e:
            print(f"Error occurred: {e}. Restarting...")
            await asyncio.sleep(5)  # Wait before restarting

# Run the main function
asyncio.run(main())