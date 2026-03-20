import yfinance as yf
import time
import json
import math

CHECK_INTERVAL = 20
FILE_NAME = "targets.json"

targets = {}
tickers = {}

def trigger_function(symbol, price, rule_type):
    print(f"{symbol} hit its {rule_type} target price: {price}")
    targets[symbol]["active"] = False
    save_targets(targets)

def load_targets():
    with open(FILE_NAME, "r") as f:
        return json.load(f)
    
def save_targets(targets):
    with open(FILE_NAME, "w") as f:
        json.dump(targets, f, indent=4)


while True:
    try:
        new_targets = load_targets()

        # Remove symbols no longer in the JSON file
        for symbol in list(targets):
            if symbol not in new_targets:
                del tickers[symbol]
                print(f"removed {symbol}")

        # Add new symbols and reset triggered if a rule changed
        for symbol, data in new_targets.items():
            print(data)
            print(targets)
            if symbol not in tickers:
                tickers[symbol] = yf.Ticker(symbol)
                print(f"added {symbol} with {data['type']} target {data['target']}")

            elif targets[symbol] != data:
                print(f"{symbol} has been updated")

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
                    hit_target = (price < target.lower or price > target.upper)
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