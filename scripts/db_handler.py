import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "stocksms.db"

def get_connection():
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS targets(
                            symbol TEXT PRIMARY KEY, 
                            type TEXT NOT NULL,  
                            target_value REAL, 
                            bb_upper REAL, 
                            bb_lower REAL, 
                            active INTEGER NOT NULL DEFAULT 1
                    )""")
        
def row_to_target(row):
    if row["type"] == "bb":
        target = {
            "upper": row["bb_upper"],
            "lower": row["bb_lower"]
        }
    else:
        target = row["target_value"]

    return {
        "type": row["type"],
        "target": target,
        "active": bool(row["active"])
    }

def get_all_targets():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM targets")
        rows = cursor.fetchall()

        targets = {}
        for row in rows:
            targets[row["symbol"]] = row_to_target(row)

        return targets
    
def get_target(symbol):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM targets WHERE symbol = ?", (symbol,))
        row = cursor.fetchone()

        if row is None:
            return None
        
        return row_to_target(row)

def add_target(symbol, rule_type, target_value=None, bb_upper=None, bb_lower=None, active=True):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO targets (symbol, type, target_value, bb_upper, bb_lower, active) 
                            VALUES (?, ?, ?, ?, ?, ?)""", 
                            (symbol, rule_type, target_value, bb_upper, bb_lower, int(active)))
        return True
    except sqlite3.IntegrityError:
        return False

def update_target(symbol, rule_type, target_value=None, bb_upper=None, bb_lower=None, active=True):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""UPDATE targets
                            SET type = ?,
                                target_value = ?,
                                bb_upper = ?,
                                bb_lower = ?,
                                active = ?
                            WHERE symbol = ?
                        """, (rule_type, target_value, bb_upper, bb_lower, int(active), symbol))
        return cursor.rowcount > 0
        
def set_target_inactive(symbol):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""UPDATE targets SET active = 0 WHERE symbol = ?""", (symbol,))
        return cursor.rowcount > 0
    
def remove_target(symbol):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM targets WHERE symbol = ?""", (symbol,))
        return cursor.rowcount > 0


