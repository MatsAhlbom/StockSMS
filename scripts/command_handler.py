import json

FILE_NAME = "targets.json"

rules = ["ceiling", "floor"]

def help_msg():
    return ("""Command formats: 
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


def error(message, targets):
    return {
        "ok": False,
        "message": message,
        "targets": targets
    }


def success(message, targets):
    return {
        "ok": True,
        "message": message,
        "targets": targets
    }

def load_targets():
    try:
        with open(FILE_NAME, "r") as f:
                targets = json.load(f)
    except FileNotFoundError:
        return {}

    return targets

def save_targets(targets):
    with open(FILE_NAME, "w") as f:
        json.dump(targets, f, indent=4)


def run_command(command):

    try:
        targets = load_targets()

    except Exception as e:
        return error(str(e), {})

    parts = command.split()

    if not parts:
        return error("Empty command. Type 'help' for usage.", targets)
    
    action = parts[0].lower()

    if action == "help":
        return success(help_msg(), targets)

    elif action == "list":
        if not targets:
            return success("Inga targets sparade.", targets)

        lines = []
        for symbol, data in targets.items():
            lines.append(f"{symbol}: {data['type']} {data['target']}")
        return success("\n".join(lines), targets)


    if action in ("add", "set"):

        if len(parts) != 4:
            return error(f"Format: {action} SYMBOL TYPE TARGET", targets)

        _, symbol, rule_type, target_value = parts
        symbol = symbol.upper()
        rule_type = rule_type.lower()

        if rule_type not in rules:
            return error(f"not a valid rule.", targets)

        try:
            target = float(target_value)
        except ValueError:
            return error("Target needd to be a float.", targets)

        targets[symbol] = {
            "type": rule_type,
            "target": target
        }

        save_targets(targets)

        if action == "add":
            return success(f"Added {symbol} with {rule_type} target {target}", targets)
        else:
            return success(f"Updated {symbol} to {rule_type} target {target}", targets)

    elif action == "remove":
        if len(parts) != 2:
            return error("Format: remove SYMBOL", targets)

        _, symbol = parts
        symbol = symbol.upper()

        if symbol not in targets:
            return error(f"{symbol} does not exist in targets.", targets)

        del targets[symbol]

        save_targets(targets)

        return success(f"Removed {symbol}", targets)

    return error(f"Invalid command: {action}. Type 'help' for usage.", targets)

