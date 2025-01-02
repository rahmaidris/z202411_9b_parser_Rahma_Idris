import asyncio
import json

import websockets

async def connect_to_binance():
    uri = "wss://stream.binance.com:9443/ws/!bookTicker"
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                try:
                    response = await websocket.recv()
                    data = json.loads(response)
                    print(data)  # For now, just print the data
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                except websockets.exceptions.ConnectionClosed as e:
                    print(f"WebSocket closed: {e}")
                    break
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    asyncio.run(connect_to_binance())


order_book = {"bid": {}, "ask": {}}

def update_order_book(data):
    bid_price = float(data['b'])
    bid_qty = float(data['B'])
    ask_price = float(data['a'])
    ask_qty = float(data['A'])

    order_book["bid"][bid_price] = bid_qty
    order_book["ask"][ask_price] = ask_qty

async def connect_to_binance():
    uri = "wss://stream.binance.com:9443/ws/!bookTicker"
    async with websockets.connect(uri) as websocket:
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            update_order_book(data)

asyncio.get_event_loop().run_until_complete(connect_to_binance())




def calculate_average_price(order_book, quantity, side):
    if side not in ["bid", "ask"]:
        raise ValueError("Side must be 'bid' or 'ask'")

    total_qty = 0
    total_cost = 0

    sorted_prices = sorted(order_book[side].keys(), reverse=(side == "bid"))

    for price in sorted_prices:
        available_qty = order_book[side][price]
        if total_qty + available_qty >= quantity:
            total_cost += (quantity - total_qty) * price
            total_qty = quantity
            break
        else:
            total_cost += available_qty * price
            total_qty += available_qty

    if total_qty < quantity:
        raise ValueError("Not enough liquidity to fulfill the order")

    return total_cost / total_qty

# Example usage
bid_order_book = {90000: 0.5, 90100: 0.6, 90200: 1.0, 90300: 1.8, 90400: 2.3}
ask_order_book = {90500: 2.2, 90600: 1.9, 90700: 0.8, 90800: 0.5, 90900: 0.5}
order_book = {"bid": bid_order_book, "ask": ask_order_book}

average_price = calculate_average_price(order_book, 5.54, "bid")
print(f"Average Trading Price: {average_price}")