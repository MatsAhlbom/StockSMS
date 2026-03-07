import yfinance as yf
import time
import json

CHECK_INTERVAL = 20
FILE_NAME = "targets.json"

targets = {}
tickers = {}
triggerd = {}

def trigger_function(symbol, price, rule_type):
    print(f"{symbol} hit its {rule_type} target price: {price}")
    triggerd[symbol] = True

def load_targets():
    with open(FILE_NAME, "r") as f:
        return json.load(f)

while True:
    try:
        new_targets = load_targets()

        # Remove symbols no longer in the JSON file
        for symbol in list(targets):
            if symbol not in new_targets:
                del tickers[symbol]
                del triggerd[symbol]
                print(f"removed {symbol}")

        # Add new symbols and reset triggered if a rule changed
        for symbol, data in new_targets.items():
            if symbol not in tickers:
                tickers[symbol] = yf.Ticker(symbol)
                triggerd[symbol] = False
                print(f"added {symbol} with {data['type']} target {data['target']}")

            elif targets[symbol] != data:
                triggerd[symbol] = False
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
                else:
                    print(f"{symbol} has invalid type: {rule_type}")
                    continue

                if hit_target and not triggerd[symbol]:
                    trigger_function(symbol, price, rule_type)

            except Exception as e:
                print(f"a problem during the check of {symbol}: {e}")

    except Exception as e:
        print(f"could not load targets: {e}")

    time.sleep(CHECK_INTERVAL)