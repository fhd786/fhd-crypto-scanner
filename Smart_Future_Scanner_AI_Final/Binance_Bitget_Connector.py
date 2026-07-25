# =========================================================
# SMART FUTURE SCANNER AI
# BINANCE + BITGET CONNECTOR
# PART 1
# =========================================================

import requests
import logging
import time


# =========================================================
# SETTINGS
# =========================================================

BINANCE_BASE_URL = "https://fapi.binance.com"

BITGET_BASE_URL = "https://api.bitget.com"


# =========================================================
# LOGGER
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)



# =========================================================
# BINANCE CONNECTOR
# =========================================================

class BinanceConnector:


    def __init__(self):

        self.name = "BINANCE"

        logging.info(
            "Binance Connector Loaded"
        )



    # -----------------------------------------------------
    # Get Candle Data
    # -----------------------------------------------------

    def get_candles(
        self,
        symbol,
        timeframe,
        limit=200
    ):

        try:

            url = (
                BINANCE_BASE_URL
                +
                "/fapi/v1/klines"
            )


            params = {

                "symbol": symbol,

                "interval": timeframe,

                "limit": limit

            }


            response = requests.get(
                url,
                params=params,
                timeout=10
            )


            data = response.json()


            candles = []


            for candle in data:

                candles.append({

                    "time": candle[0],

                    "open": float(candle[1]),

                    "high": float(candle[2]),

                    "low": float(candle[3]),

                    "close": float(candle[4]),

                    "volume": float(candle[5])

                })


            return candles



        except Exception as error:


            logging.error(
                f"Binance Candle Error: {error}"
            )


            return []




# =========================================================
# BITGET CONNECTOR
# =========================================================

class BitgetConnector:


    def __init__(self):

        self.name = "BITGET"


        logging.info(
            "Bitget Connector Loaded"
        )



    # -----------------------------------------------------
    # Get Candle Data
    # -----------------------------------------------------

    def get_candles(
        self,
        symbol,
        timeframe,
        limit=200
    ):


        try:


            url = (

                BITGET_BASE_URL

                +

                "/api/v2/mix/market/candles"

            )


            params = {

                "symbol": symbol,

                "granularity": timeframe,

                "limit": limit,

                "productType": "USDT-FUTURES"

            }



            response = requests.get(

                url,

                params=params,

                timeout=10

            )


            data = response.json()



            candles = []



            return candles



        except Exception as error:


            logging.error(

                f"Bitget Candle Error: {error}"

            )


            return []



# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":


    binance = BinanceConnector()


    bitget = BitgetConnector()


    print(
        "Binance + Bitget Connector Ready"
    )