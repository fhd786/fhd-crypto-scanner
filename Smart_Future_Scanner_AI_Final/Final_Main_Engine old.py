"""
=========================================================
Smart Future Scanner AI
FINAL MAIN ENGINE
Version 1

PART 1
Module Connection + System Setup
=========================================================
"""


import time
import logging
from datetime import datetime

# =========================================================
# EXCHANGE CONNECTORS
# =========================================================

from Binance_Bitget_Connector import (
    BinanceConnector,
    BitgetConnector
)# =========================================================
# INTERNAL MODULES
# =========================================================

from Indicator_Engine import IndicatorEngine
from Signal_Engine import SignalEngine
from Alert_System import AlertSystem
from Telegram_Alert import TelegramAlert
from Gmail_Alert import GmailAlert
from Live_Scanner import LiveScanner
# =========================================================
# SETTINGS
# =========================================================


SCANNER_NAME = "Smart Future Scanner AI"

VERSION = "FINAL V1"


TIMEFRAMES = [

    "15m",
    "1h",
    "4h"

]


TOP_GAINERS_LIMIT = 40


SCAN_INTERVAL = 60



# =========================================================
# LOGGER SETUP
# =========================================================


logging.basicConfig(

    level=logging.INFO,

    format=
    "%(asctime)s | %(levelname)s | %(message)s"

)



# =========================================================
# SYSTEM STATUS
# =========================================================


class SystemStatus:


    def __init__(self):

        self.running = False

        self.start_time = None



    def start(self):

        self.running = True

        self.start_time = datetime.now()



    def stop(self):

        self.running = False



    def info(self):

        return {


            "name":
            SCANNER_NAME,


            "version":
            VERSION,


            "running":
            self.running,


            "start_time":
            self.start_time

        }




# =========================================================
# FINAL MAIN ENGINE CLASS
# =========================================================


class FinalMainEngine:


    def __init__(self):


        self.status = SystemStatus()



        logging.info(
            "Final Main Engine Loaded"
        )



    # -----------------------------------------------------
    # Engine Start
    # -----------------------------------------------------


    def start_engine(self):


        self.status.start()


        print(
            "================================="
        )


        print(
            SCANNER_NAME
        )


        print(
            VERSION
        )


        print(
            "SYSTEM STARTED"
        )


        print(
            "================================="
        )




# =========================================================
# TEST START
# =========================================================


if __name__ == "__main__":


    engine = FinalMainEngine()


    engine.start_engine()
    # =========================================================
# V1 FINAL MAIN ENGINE
# PART 2
# CONNECTOR + MARKET DATA MANAGER
# =========================================================


import requests
import time


# =========================================================
# SETTINGS
# =========================================================


BINANCE_URL = "https://fapi.binance.com"

BITGET_URL = "https://api.bitget.com"


TIMEFRAMES = [

    "15m",
    "1h",
    "4h"

]


CANDLE_LIMIT = 200



# =========================================================
# BASE API CONNECTOR
# =========================================================


class APIConnector:


    def __init__(
        self,
        name,
        url
    ):

        self.name = name
        self.url = url



    def get(
        self,
        endpoint,
        params=None
    ):


        try:

            response = requests.get(

                self.url + endpoint,

                params=params,

                timeout=10

            )


            if response.status_code == 200:

                return response.json()



            print(

                self.name,

                "API Error",

                response.status_code

            )


        except Exception as error:


            print(

                self.name,

                "Connection Error",

                error

            )



        return None





# =========================================================
# BINANCE CONNECTOR
# =========================================================


class BinanceAPI:


    def __init__(self):

        self.api = APIConnector(

            "BINANCE",

            BINANCE_URL

        )



    def get_gainers(self):


        data = self.api.get(

            "/fapi/v1/ticker/24hr"

        )


        result = []


        if not data:

            return result



        for coin in data:


            symbol = coin.get(

                "symbol"

            )



            if (

                symbol

                and

                symbol.endswith("USDT")

            ):


                result.append({


                    "symbol":

                    symbol,


                    "change":

                    float(

                        coin.get(

                            "priceChangePercent",

                            0

                        )

                    ),


                    "volume":

                    float(

                        coin.get(

                            "quoteVolume",

                            0

                        )

                    )

                })



        result.sort(

            key=lambda x:

            x["change"],

            reverse=True

        )



        return result[:40]





    def get_candles(

        self,

        symbol,

        timeframe

    ):


        params = {


            "symbol":

            symbol,


            "interval":

            timeframe,


            "limit":

            CANDLE_LIMIT


        }



        data = self.api.get(

            "/fapi/v1/klines",

            params

        )



        candles = []



        if not data:

            return candles



        for item in data:


            candles.append({


                "time":

                item[0],


                "open":

                float(item[1]),


                "high":

                float(item[2]),


                "low":

                float(item[3]),


                "close":

                float(item[4]),


                "volume":

                float(item[5])

            })



        return candles





# =========================================================
# BITGET CONNECTOR
# =========================================================


class BitgetAPI:


    def __init__(self):

        self.api = APIConnector(

            "BITGET",

            BITGET_URL

        )




    def get_gainers(self):


        params = {


            "productType":

            "USDT-FUTURES"

        }



        data = self.api.get(

            "/api/v2/mix/market/tickers",

            params

        )



        result = []



        if not data:

            return result



        for coin in data.get(

            "data",

            []

        ):


            symbol = coin.get(

                "symbol"

            )



            if symbol:


                result.append({


                    "symbol":

                    symbol,


                    "change":

                    float(

                        coin.get(

                            "change24h",

                            0

                        )

                    ),


                    "volume":

                    float(

                        coin.get(

                            "baseVolume",

                            0

                        )

                    )


                })



        result.sort(

            key=lambda x:

            x["change"],

            reverse=True

        )



        return result[:40]





# =========================================================
# MARKET DATA MANAGER
# =========================================================


class MarketDataManager:


    def __init__(
        self,
        binance,
        bitget
    ):

        self.binance = binance

        self.bitget = bitget


        print(
            "Market Data Manager Loaded"
        )

    def get_top_coins(self):

        coins = []

        coins.extend(
            self.binance.get_gainers()
        )

        coins.extend(
            self.bitget.get_gainers()
        )

        unique = {}

        for coin in coins:

            symbol = coin["symbol"]

            if symbol not in unique:
                unique[symbol] = coin

        final = list(unique.values())

        final.sort(
            key=lambda x: x["change"],
            reverse=True
        )

        return final[:40]

    def load_multi_timeframe(
        self,
        symbol
    ):

        return {
            "symbol": symbol,

            "15m": self.binance.get_candles(
                symbol,
                "15m"
            ),

            "1h": self.binance.get_candles(
                symbol,
                "1h"
            ),

            "4h": self.binance.get_candles(
                symbol,
                "4h"
            )
        }

    def get_multi_timeframe_data(
        self,
        symbol
    ):
        return self.load_multi_timeframe(symbol)
# =========================================================
# V1 MAIN ENGINE
# PART C
# FINAL SIGNAL PROCESSING ENGINE
# =========================================================


class FinalSignalProcessor:


    def __init__(
        self,
        indicator_engine,
        signal_engine,
        confidence_manager,
        risk_manager
    ):

        self.indicators = indicator_engine

        self.signal_engine = signal_engine

        self.confidence = confidence_manager

        self.risk = risk_manager



    # -----------------------------------------------------
    # Process Single Timeframe
    # -----------------------------------------------------

    def analyze_timeframe(
        self,
        candles
    ):


        result = {}


        closes = [
            x["close"]
            for x in candles
        ]


        highs = [
            x["high"]
            for x in candles
        ]


        lows = [
            x["low"]
            for x in candles
        ]


        volumes = [
            x["volume"]
            for x in candles
        ]



        # EMA Confirmation

        ema_signal = (
            self.indicators
            .check_ema_cross(
                candles
            )
        )



        # RSI

        rsi_value = (
            self.indicators
            .calculate_rsi(
                candles
            )
        )



        # ADX

        adx_value = (
            self.indicators
            .calculate_adx(
                candles
            )
        )



        # ATR

        atr_value = (
            self.indicators
            .calculate_atr(
                candles
            )
        )



        # Volume

        volume_status = (
            self.indicators
            .check_volume_strength(
                candles
            )
        )



        # VWAP

        vwap_status = (
            self.indicators
            .check_vwap_position(
                candles
            )
        )



        # KVO

        kvo_status = (
            self.indicators
            .check_kvo_signal(
                candles
            )
        )



        result = {


            "ema":

            ema_signal,


            "rsi":

            rsi_value,


            "adx":

            adx_value,


            "atr":

            atr_value,


            "volume":

            volume_status,


            "vwap":

            vwap_status,


            "kvo":

            kvo_status

        }


        return result




    # -----------------------------------------------------
    # Multi Timeframe Confirmation
    # -----------------------------------------------------

    def multi_timeframe_check(
        self,
        timeframe_results
    ):


        bullish = 0

        bearish = 0



        for item in timeframe_results:


            if item["ema"] == "LONG":

                bullish += 1



            if item["ema"] == "SHORT":

                bearish += 1




        if bullish >= 2:

            return "BULLISH CONFIRMED"



        if bearish >= 2:

            return "BEARISH CONFIRMED"



        return "NO CONFIRMATION"




    # -----------------------------------------------------
    # Final Coin Analysis
    # -----------------------------------------------------

    def process_coin(
        self,
        market_data
    ):


        timeframe_results = []
    def process(self, market_data):
        return self.process_coin(market_data)


        for timeframe in [

            "15m",
            "1H",
            "4H"

        ]:


            candles = (
                market_data
                .get(timeframe, [])
            )



            if len(candles) > 50:


                analysis = (
                    self.analyze_timeframe(
                        candles
                    )
                )


                timeframe_results.append(
                    analysis
                )




        confirmation = (
            self.multi_timeframe_check(
                timeframe_results
            )
        )



        return {


            "confirmation":

            confirmation,


            "timeframes":

            timeframe_results

        }
        # =========================================================
# V1 MAIN ENGINE
# PART 4
# STRATEGY DECISION ENGINE
# =========================================================


class StrategyDecisionEngine:


    def __init__(self):

        self.minimum_score = 80



    # -----------------------------------------------------
    # Calculate Strategy Score
    # -----------------------------------------------------

    def calculate_score(
        self,
        conditions
    ):

        score = 0


        # EMA Confirmation

        if conditions.get(
            "ema"
        ) == "LONG":

            score += 15



        # KVO Confirmation

        if conditions.get(
            "kvo"
        ) == "LONG":

            score += 20



        # KVO Zero Line

        if conditions.get(
            "kvo_zero"
        ):

            score += 10



        # Volume Confirmation

        if conditions.get(
            "volume"
        ):

            score += 15



        # VWAP Confirmation

        if conditions.get(
            "vwap"
        ) == "ABOVE":

            score += 15



        # CVD Confirmation

        if conditions.get(
            "cvd"
        ) == "BULLISH":

            score += 10



        # Open Interest Confirmation

        if conditions.get(
            "oi"
        ) == "LONG_SUPPORT":

            score += 15



        return score



    # -----------------------------------------------------
    # Generate Final Signal
    # -----------------------------------------------------

    def generate_signal(
        self,
        conditions
    ):


        score = self.calculate_score(
            conditions
        )


        if score >= self.minimum_score:


            return {


                "signal":
                "STRONG_LONG",


                "score":
                score,


                "status":
                "CONFIRMED"

            }



        return {


            "signal":
            "NO_SIGNAL",


            "score":
            score,


            "status":
            "WAIT"

        }




# =========================================================
# STRATEGY ENGINE READY
# =========================================================


print(
    "Strategy Decision Engine Loaded"
)
# =========================================================
# V1 MAIN ENGINE
# PART 5
# BINANCE + BITGET GAINER SCANNER
# =========================================================


import requests


class GainerScanner:


    def __init__(self):

        self.binance_url = (
            "https://fapi.binance.com"
            "/fapi/v1/ticker/24hr"
        )


        self.bitget_url = (
            "https://api.bitget.com"
            "/api/v2/mix/market/tickers"
        )



    # -----------------------------------------------------
    # Binance Futures Top Gainers
    # -----------------------------------------------------

    def get_binance_gainers(
        self,
        limit=40
    ):


        try:


            response = requests.get(
                self.binance_url,
                timeout=10
            )


            data = response.json()


            coins = []


            for item in data:


                symbol = item.get(
                    "symbol",
                    ""
                )


                if symbol.endswith(
                    "USDT"
                ):


                    change = float(
                        item.get(
                            "priceChangePercent",
                            0
                        )
                    )


                    volume = float(
                        item.get(
                            "quoteVolume",
                            0
                        )
                    )


                    coins.append({

                        "symbol":
                        symbol,

                        "exchange":
                        "BINANCE",

                        "change":
                        change,

                        "volume":
                        volume

                    })



            coins.sort(
                key=lambda x:
                x["change"],
                reverse=True
            )


            return coins[:limit]



        except Exception as error:


            print(
                "Binance Gainer Error:",
                error
            )


            return []




    # -----------------------------------------------------
    # Bitget Futures Top Gainers
    # -----------------------------------------------------

    def get_bitget_gainers(
        self,
        limit=40
    ):


        try:


            params = {

                "productType":
                "USDT-FUTURES"

            }


            response = requests.get(

                self.bitget_url,

                params=params,

                timeout=10

            )


            result = response.json()


            data = result.get(
                "data",
                []
            )


            coins = []



            for item in data:


                symbol = item.get(
                    "symbol",
                    ""
                )


                if symbol.endswith(
                    "USDT"
                ):


                    change = float(
                        item.get(
                            "change24h",
                            0
                        )
                    )


                    coins.append({

                        "symbol":
                        symbol,

                        "exchange":
                        "BITGET",

                        "change":
                        change

                    })



            coins.sort(

                key=lambda x:
                x["change"],

                reverse=True

            )


            return coins[:limit]



        except Exception as error:


            print(
                "Bitget Gainer Error:",
                error
            )


            return []




    # -----------------------------------------------------
    # Merge Exchange Lists
    # -----------------------------------------------------

    def get_final_coin_list(self):


        binance = (
            self.get_binance_gainers()
        )


        bitget = (
            self.get_bitget_gainers()
        )


        combined = {}



        for coin in binance + bitget:


            symbol = coin["symbol"]


            if symbol not in combined:


                combined[symbol] = coin



        final = list(
            combined.values()
        )


        return final[:40]





# =========================================================
# GAINER SCANNER READY
# =========================================================


print(
    "Gainer Scanner Loaded"
)
# =========================================================
# V1 FINAL MAIN ENGINE
# PART 6
# FINAL SCANNER LOOP + ALERT CONNECTION
# =========================================================


class FinalScannerEngine:


    def __init__(
        self,
        market_manager,
        signal_processor,
        alert_manager
    ):

        self.market_manager = market_manager

        self.signal_processor = signal_processor

        self.alert_manager = alert_manager



    # -----------------------------------------------------
    # Scan Single Symbol
    # -----------------------------------------------------

    def scan_symbol(
        self,
        symbol
    ):

        try:

            market_data = (
                self.market_manager
                .get_multi_timeframe_data(
                    symbol
                )
            )


            signal = (
                self.signal_processor
                .process(
                    market_data
                )
            )


            return {

                "symbol":
                symbol,

                "signal":
                signal

            }


        except Exception as error:


            return {

                "symbol":
                symbol,

                "signal":
                "ERROR",

                "reason":
                str(error)

            }





    # -----------------------------------------------------
    # Scan Multiple Symbols
    # -----------------------------------------------------

    def run_symbols(
        self,
        symbols
    ):


        results = []


        for symbol in symbols:


            result = self.scan_symbol(
                symbol
            )


            results.append(
                result
            )


            if (
                result["signal"]
                and
                result["signal"] != "NONE"
            ):


                message = str(
                    result
                )


                self.alert_manager.send_all(
                    message
                )



        return results





# =========================================================
# SYSTEM BOOT FINAL CONNECTION
# =========================================================
def start_final_scanner():

    print(
        "Smart Future Scanner AI Final Engine Starting..."
    )

    try:

        binance = BinanceConnector()

        bitget = BitgetConnector()

        market_manager = MarketDataManager(
            binance,
            bitget
        )

        indicators = IndicatorEngine()

        signal_engine = SignalEngine()

        processor = FinalSignalProcessor(
            indicators,
            signal_engine,
            None,
            None
        )

        alert_manager = AlertSystem()

        scanner = FinalScannerEngine(
            market_manager,
            processor,
            alert_manager
        )

        print("Smart Future Scanner AI Ready")
        print("Binance Futures Connected")
        print("Bitget Futures Connected")
        print("Scanner Waiting For Market Data...")
        print("DEBUG: Starting Coin Scan")   
        print("DEBUG: Before Gainer Scan")
        print("DEBUG: Reached Before Symbols")
        symbols = [
            coin["symbol"]
            for coin in GainerScanner().get_final_coin_list()
        ]

        results = scanner.run_symbols(symbols)

        print(results)

        return scanner


    except Exception as error:

        print(
            "FINAL ENGINE ERROR:",
            error
        )

        return None
        # =========================================================
# APPLICATION START
# =========================================================

if __name__ == "__main__":

    scanner = start_final_scanner()





            

        



        