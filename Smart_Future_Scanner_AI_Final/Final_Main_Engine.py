# =========================================================
# SMART FUTURE SCANNER AI
# FINAL MAIN ENGINE
# DEVELOPED BY: FHD Crypto Royal Zone
# VERSION: FINAL V2
# =========================================================

import time
import logging
import requests
from datetime import datetime

from Indicator_Engine import IndicatorEngine
from Signal_Engine import SignalEngine

# Dummy Alert imports for safety (if available)
try:
    from Telegram_Alert import TelegramAlert
    from Gmail_Alert import GmailAlert
except ImportError:
    TelegramAlert = None
    GmailAlert = None

# =========================================================
# GLOBAL SETTINGS & TELEGRAM INTEGRATION
# =========================================================

SCANNER_NAME = "Smart Future Scanner AI"
AUTHOR = "FHD Crypto Royal Zone"
VERSION = "FINAL V2"

TIMEFRAMES = ["15m", "1h", "4h"]
TOP_GAINERS_LIMIT = 40
SCAN_INTERVAL = 60
CANDLE_LIMIT = 200

BINANCE_URL = "https://fapi.binance.com"
BITGET_URL = "https://api.bitget.com"

# --- TELEGRAM CONFIGURATION ---
TELEGRAM_BOT_TOKEN = "8419234517:AAGT_drJE3YWuw1_Fkr-JUhS2iLrqrvDqCE"
TELEGRAM_CHAT_ID = "8371862467"

def send_telegram_message(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        logging.error(f"Telegram Notification Error: {e}")

def format_telegram_signal(symbol: str, exchange: str, sig: dict) -> str:
    action_type = sig.get('signal', 'BUY/SELL')
    action_emoji = "🟢 BUY / LONG" if "BUY" in action_type.upper() or "LONG" in action_type.upper() else "🔴 SELL / SHORT"
    
    msg = f"""
🚨 **SMART FUTURE SCANNER AI** 🚨
━━━━━━━━━━━━━━━━━━━━━
📊 **Symbol:** `{symbol}`
🏢 **Exchange:** `{exchange}`
🚦 **Action:** **{action_emoji}**
🎯 **Confidence:** `{sig.get('confidence', 'N/A')}`

📌 **Entry Price:** `{sig.get('entry', 'N/A')}`
🛡️ **Stop Loss:** `{sig.get('stop_loss', 'N/A')}`
🎯 **Take Profit:** `{sig.get('take_profit', 'N/A')}`
⚖️ **Risk/Reward:** `{sig.get('risk_reward', 'N/A')}`
⚡ **Leverage:** `{sig.get('leverage', 'N/A')}X`

⏰ **Time:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`
━━━━━━━━━━━━━━━━━━━━━
👑 *FHD Crypto Royal Zone*
"""
    return msg

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# =========================================================
# CONNECTORS & MARKET DATA
# =========================================================

class APIConnector:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def get(self, endpoint, params=None):
        try:
            response = requests.get(self.url + endpoint, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            logging.error(f"{self.name} API ERROR {response.status_code}")
        except Exception as error:
            logging.error(f"{self.name} CONNECTION ERROR {error}")
        return None


class BinanceConnector:
    def __init__(self):
        self.api = APIConnector("BINANCE", BINANCE_URL)

    def get_gainers(self, limit=40):
        data = self.api.get("/fapi/v1/ticker/24hr")
        coins = []
        if not data:
            return coins

        for item in data:
            symbol = item.get("symbol", "")
            if symbol.endswith("USDT"):
                coins.append({
                    "symbol": symbol,
                    "exchange": "BINANCE",
                    "change": float(item.get("priceChangePercent", 0)),
                    "volume": float(item.get("quoteVolume", 0))
                })

        coins.sort(key=lambda x: x["change"], reverse=True)
        return coins[:limit]

    def get_candles(self, symbol, timeframe):
        params = {"symbol": symbol, "interval": timeframe, "limit": CANDLE_LIMIT}
        data = self.api.get("/fapi/v1/klines", params)
        candles = []
        if not data:
            return candles

        for item in data:
            candles.append({
                "time": item[0],
                "open": float(item[1]),
                "high": float(item[2]),
                "low": float(item[3]),
                "close": float(item[4]),
                "volume": float(item[5])
            })
        return candles


class BitgetConnector:
    def __init__(self):
        self.api = APIConnector("BITGET", BITGET_URL)

    def get_gainers(self, limit=40):
        params = {"productType": "USDT-FUTURES"}
        data = self.api.get("/api/v2/mix/market/tickers", params)
        coins = []
        if not data:
            return coins

        for item in data.get("data", []):
            symbol = item.get("symbol", "")
            if symbol.endswith("USDT"):
                coins.append({
                    "symbol": symbol,
                    "exchange": "BITGET",
                    "change": float(item.get("change24h", 0))
                })

        coins.sort(key=lambda x: x["change"], reverse=True)
        return coins[:limit]


class MarketDataManager:
    def __init__(self, binance, bitget):
        self.binance = binance
        self.bitget = bitget

    def get_top_coins(self, limit=40):
        coins = []
        coins.extend(self.binance.get_gainers(limit))
        coins.extend(self.bitget.get_gainers(limit))

        unique = {}
        for coin in coins:
            symbol = coin["symbol"]
            if symbol not in unique:
                unique[symbol] = coin

        final = list(unique.values())
        final.sort(key=lambda x: x["change"], reverse=True)
        return final[:limit]

    def get_multi_timeframe_data(self, symbol):
        return {
            "symbol": symbol,
            "15m": self.binance.get_candles(symbol, "15m"),
            "1h": self.binance.get_candles(symbol, "1h"),
            "4h": self.binance.get_candles(symbol, "4h")
        }


# =========================================================
# MAIN SCANNER SYSTEM
# =========================================================

class SmartFutureScannerAI:

    def __init__(self):
        self.binance = BinanceConnector()
        self.bitget = BitgetConnector()
        self.market = MarketDataManager(self.binance, self.bitget)

        self.indicators = IndicatorEngine()
        self.signal_engine = SignalEngine()

    def scan_coin(self, coin_info):
        symbol = coin_info["symbol"]
        try:
            data = self.market.get_multi_timeframe_data(symbol)
            if not data["15m"] or len(data["15m"]) < 60:
                return None

            package = self.indicators.build_indicator_package(
                data["15m"], data["1h"], data["4h"], symbol
            )

            trade_signal = self.signal_engine.process(package)

            if trade_signal:
                return {
                    "symbol": symbol,
                    "exchange": coin_info.get("exchange", "BINANCE"),
                    "signal": trade_signal
                }
        except Exception as e:
            logging.error(f"Error Scanning {symbol}: {e}")

        return None

    def start(self):
        print("=" * 70)
        print(f"{SCANNER_NAME} | Developed By: {AUTHOR}")
        print(f"Version: {VERSION} | Status: RUNNING...")
        print("=" * 70)

        # Send Startup Alert to Telegram
        send_telegram_message("🚀 **Smart Future Scanner AI Started!**\nTelegram Alerts Connected Successfully!")

        while True:
            try:
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Fetching Top 40 Gainers...")
                top_coins = self.market.get_top_coins(40)

                signals_found = 0
                for coin in top_coins:
                    result = self.scan_coin(coin)
                    if result:
                        signals_found += 1
                        sig = result["signal"]
                        
                        # Terminal Console Print
                        print(f"\n🚀 [SIGNAL DETECTED] {result['symbol']} ({result['exchange']})")
                        print(f"Type: {sig['signal']} | Confidence: {sig['confidence']}")
                        print(f"Entry: {sig['entry']} | SL: {sig['stop_loss']} | TP: {sig['take_profit']}")
                        print(f"RR: {sig['risk_reward']} | Leverage: {sig['leverage']}X")
                        print("-" * 50)

                        # Telegram Notification Send
                        telegram_msg = format_telegram_signal(result['symbol'], result['exchange'], sig)
                        send_telegram_message(telegram_msg)

                if signals_found == 0:
                    print("No Valid Signals Found in this Scan Cycle.")

                print(f"Scan Finished. Waiting for {SCAN_INTERVAL} Seconds...")
                time.sleep(SCAN_INTERVAL)

            except KeyboardInterrupt:
                print("Scanner Stopped By User.")
                break
            except Exception as e:
                print(f"Main Loop Error: {e}")
                time.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    app = SmartFutureScannerAI()
    app.start()