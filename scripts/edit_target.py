import json

FILE_NAME = "targets.json"

def print_help():
    print("""
Command formats:
    add SYMBOL TYPE TARGET
    set SYMBOL TYPE TARGET
    remove SYMBOL
    list
    help

Actions:
    add SYMBOL TYPE TARGET    add a new symbol rule
    set SYMBOL TYPE TARGET    create or update a symbol rule
    remove SYMBOL             remove a symbol
    list                      list all symbols and their rules
    help                      show this message

TYPE:
    ceiling   trigger when price >= target
    floor     trigger when price <= target

""")

with open(FILE_NAME, "r") as f:
    targets = json.load(f)

command = input("command: ")

try:
    parts = command.split()
    action = parts[0].lower()

    if action == "help":
        print_help()

    elif action == "list":
        for symbol, data in targets.items():
            print(f"{symbol}: {data['type']} {data['target']}")

    else:
        action, symbol, *rest = parts
        symbol = symbol.upper()

        if action in ("add", "set"):
            rule_type = rest[0].lower()
            target = float(rest[1])

            if rule_type not in ("ceiling", "floor"):
                raise ValueError("invalid type")

            targets[symbol] = {
                "type": rule_type,
                "target": target
            }

            if action == "add":
                print(f"Added {symbol} with {rule_type} target {target}")
            else:
                print(f"Updated {symbol} to {rule_type} target {target}")

        elif action == "remove":
            del targets[symbol]
            print(f"Removed {symbol}")

        else:
            raise ValueError("invalid action")

        with open(FILE_NAME, "w") as f:
            json.dump(targets, f, indent=4)

except Exception:
    print("Invalid command. Type 'help' for usage.")