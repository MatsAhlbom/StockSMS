import yfinance as yf
import time
import os
from dotenv import load_dotenv
from .db_handler import get_all_targets, set_target_inactive
from .discord_notifier import send_notifier

load_dotenv()
DISCORD_ID = os.getenv("MASSE22_DISCORD_ID")

CHECK_INTERVAL = 20
FILE_NAME = "targets.json"
tickers = {}
targets = {}

def trigger_function(symbol, price, rule_type):
    set_target_inactive(symbol=symbol)
    print(f"{symbol} hit its {rule_type} target price: {price}")
    send_notifier(DISCORD_ID, f"${symbol} hit its {rule_type} target. Current price: {price}")

while True:
    try:
        new_targets = get_all_targets()

        for symbol in list(targets):
            if symbol not in new_targets:
                del tickers[symbol]
                print(f"removed {symbol}")

        for symbol, data in new_targets.items():
            if symbol not in tickers:
                tickers[symbol] = yf.Ticker(symbol)
                print(f"added {symbol} with {data['type']} target {data['target']}")

        targets = new_targets

        for symbol, data in targets.items():
            try:
                price = tickers[symbol].fast_info["lastPrice"]
                target = data["target"]
                rule_type = data["type"]

                if rule_type == "ceiling":
                    hit_target = price >= target
                elif rule_type == "floor":
                    hit_target = price <= target
                elif rule_type == "bb":
                    hit_target = (price < target["lower"] or price > target["upper"])
                else:
                    print(f"{symbol} has invalid type: {rule_type}")
                    continue

                if hit_target and targets[symbol]["active"]:
                    trigger_function(symbol, price, rule_type)

            except Exception as e:
                print(f"a problem during the check of {symbol}: {e}")

    except Exception as e:
        print(f"could not load targets: {e}")

    time.sleep(CHECK_INTERVAL)