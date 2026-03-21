import yfinance as yf
from db_handler import get_all_targets, add_target, remove_target, update_target

FILE_NAME = "targets.json"

rules = ["ceiling", "floor", "bb"]

def help_msg():
    return ("""Command formats: 
    add SYMBOL TYPE TARGET
    set SYMBOL TYPE TARGET
    remove SYMBOL
    list
    help

Actions:
    'add SYMBOL TYPE TARGET'    add a new or edit symbol rule
    'set SYMBOL TYPE TARGET'    edit a symbol rule
    'remove SYMBOL'             remove a symbol
    'list'                      list all symbols and their rules
    'help'                      show this message

TYPE:
    'ceiling'   trigger when price >= target
    'floor'     trigger when price <= target
    'bb'        bollinger band (use TARGET 0)

""")

def symbol_exists(symbol):
    try:
        test = yf.Ticker(symbol).fast_info["last_price"]
        _ = test > 0
        return True
    except Exception:
        return False

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

def calc_bb(symbol):
    hist = yf.Ticker(symbol).history(period="1d", interval="5m")
    closes = hist["Close"].tail(20)

    ma = closes.mean()
    sa = closes.std(ddof=0)

    upper = ma + 2 * sa
    lower = ma - 2 * sa

    return {"upper": upper, "lower": lower}

def run_command(command):

    try:
        targets = get_all_targets()

    except Exception as e:
        return error(str(e), {})

    parts = command.split()

    if not parts:
        return error("Empty command. Type 'help' for usage.", targets)
    
    action = parts[0].lower()

    if action in ("help"):
        return success(help_msg(), targets)

    elif action in ("list"):
        if not targets:
            return success("No targets saved", targets)

        lines = []
        for symbol, data in targets.items():
            lines.append(f"{symbol}: {data['type']} {data['target']}")
        return success("\n".join(lines), targets)

    if action in ("add"):
        
        if len(parts) != 4:
            return error(f"Format: {action} SYMBOL TYPE TARGET", targets)

        _, symbol, rule_type, target_value = parts
        symbol = symbol.upper()

        if symbol_exists(symbol):
            pass
        else:
            return error(f"{symbol} does not exist", targets)
        
        rule_type = rule_type.lower()

        if rule_type not in rules:
            return error(f"not a valid rule.", targets)

        if rule_type == "bb":
            target = calc_bb(symbol)

            if add_target(symbol=symbol, rule_type=rule_type, bb_upper=target["upper"], bb_lower=target["lower"], active=True):
                return success(f"Added {symbol} with {rule_type}", targets)
                
        else:
            try:
                target = float(target_value)

                if add_target(symbol=symbol, rule_type=rule_type, target_value=target, active=True):
                    return success(f"Added {symbol} with {rule_type} target {target}", targets)
            except ValueError:
                return error("Target needd to be a float.", targets)

        return error(f"{symbol} alredy in targets, try 'set' to change it", targets)
    
            
    elif action in ("set"):
        if len(parts) != 4:
            return error(f"Format: {action} SYMBOL TYPE TARGET", targets)

        _, symbol, rule_type, target_value = parts
        symbol = symbol.upper()

        if symbol_exists(symbol):
            pass
        else:
            return error(f"{symbol} does not exist", targets)
        
        rule_type = rule_type.lower()

        if rule_type not in rules:
            return error(f"not a valid rule.", targets)

        if rule_type == "bb":
            target = calc_bb(symbol)

            if update_target(symbol=symbol, rule_type=rule_type, bb_upper=target["upper"], bb_lower=target["lower"], active=True):
                return success(f"Set {symbol} with {rule_type}", targets)
                
        else:
            try:
                target = float(target_value)

                if update_target(symbol=symbol, rule_type=rule_type, target_value=target, active=True):
                    return success(f"Set {symbol} with {rule_type} target {target}", targets)
            except ValueError:
                return error("Target needd to be a float.", targets)
            
        return error(f"{symbol} does not have a target, try adding with 'add'", targets)
 

    elif action in ("remove"):
        if len(parts) != 2:
            return error("Format: remove SYMBOL", targets)

        _, symbol = parts
        symbol = symbol.upper()

        if symbol not in targets:
            return error(f"{symbol} does not exist in targets.", targets)

        remove_target(symbol=symbol)

        return success(f"Removed {symbol}", targets)

    return error(f"Invalid command: {action}. Type 'help' for usage.", targets)

