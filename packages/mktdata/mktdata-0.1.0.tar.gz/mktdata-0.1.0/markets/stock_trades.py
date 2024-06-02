from imps import *

tape_dict = { 
    1: 'NYSE',
    2: 'AMEX',
    3: 'NASDAQ'
}


c = WebSocketClient(subscriptions=["T.*"], api_key=os.environ.get('YOUR_POLYGON_KEY'))

# Handler function
async def handle_stock_trades(msgs: List[WebSocketMessage]):
    try:
        for m in msgs:
            # Convert timestamp from milliseconds since Unix epoch to UTC
            utc_time = datetime.fromtimestamp(m.timestamp / 1000, tz=timezone.utc)
            
            # Convert UTC time to Eastern Time
            eastern_time = utc_time.astimezone(ZoneInfo("America/New_York"))
            
            # Format datetime without timezone information
            m.timestamp = eastern_time.strftime('%Y-%m-%d %H:%M:%S')
            conditions_string = ','.join(map(str, m.conditions))
        
            insertion_dict = {
                'event': 'stock_trade',
                'ticker': m.symbol,
                'exchange': m.exchange,
                'id': m.id,
                'tape': m.tape,
                'price': m.price,
                'size': m.size,
                'conditions': conditions_string,
                'timestamp': pd.to_datetime(m.timestamp)  # Now a datetime object
            }

            df = pd.DataFrame(insertion_dict, index=[0])

            await db.batch_insert_dataframe(df, table_name='stock_aggs', unique_columns='ticker')
    except Exception as e:
        print("Error occurred:", e)

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
            await c.connect(lambda msgs: asyncio.create_task(handle_stock_trades(msgs)))

            # Keep the connection alive
            while True:
                await asyncio.sleep(1)  # Adjust the sleep time as needed

        except Exception as e:
            print(f"Error occurred: {e}. Restarting...")
            await asyncio.sleep(5)  # Wait before restarting

# Run the main function
asyncio.run(main())