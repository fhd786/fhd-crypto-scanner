# =========================================================
# SMART FUTURE SCANNER AI
# INDICATOR ENGINE
# PART 1
# =========================================================

import pandas as pd
import numpy as np

# =========================================================
# SIGNAL CONSTANTS
# =========================================================

LONG = "LONG"
SHORT = "SHORT"
NO_SIGNAL = "NONE"

BULLISH = "BULLISH"
BEARISH = "BEARISH"

STRONG_VOLUME = "STRONG_VOLUME"
WEAK_VOLUME = "WEAK_VOLUME"

ABOVE_VWAP = "ABOVE_VWAP"
BELOW_VWAP = "BELOW_VWAP"

BULLISH_CVD = "BULLISH_CVD"
BEARISH_CVD = "BEARISH_CVD"

LONG_SUPPORT = "LONG_SUPPORT"
SHORT_SUPPORT = "SHORT_SUPPORT"



# =========================================================
# INDICATOR ENGINE
# =========================================================

class IndicatorEngine:

    def __init__(self):

        print(
            "Indicator Engine Loaded"
        )


    # =====================================================
    # EMA
    # =====================================================

    def calculate_ema(
        self,
        candles,
        period
    ):

        df = pd.DataFrame(candles)

        df["close"] = df["close"].astype(float)

        ema = (
            df["close"]
            .ewm(
                span=period,
                adjust=False
            )
            .mean()
        )

        return ema



    # =====================================================
    # EMA CROSS
    # =====================================================

    def ema_cross(
        self,
        candles
    ):

        ema5 = self.calculate_ema(
            candles,
            5
        )

        ema50 = self.calculate_ema(
            candles,
            50
        )


        previous5 = ema5.iloc[-2]
        previous50 = ema50.iloc[-2]

        current5 = ema5.iloc[-1]
        current50 = ema50.iloc[-1]


        if (
            previous5 < previous50
            and
            current5 > current50
        ):

            return LONG


        elif (
            previous5 > previous50
            and
            current5 < current50
        ):

            return SHORT


        return NO_SIGNAL
        # =========================================================
# KVO ENGINE
# FINAL VERSION
# =========================================================

    def calculate_kvo(
        self,
        candles,
        fast=34,
        slow=55,
        signal=13
    ):

        df = pd.DataFrame(candles)

        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)

        hlc = (
            df["high"]
            + df["low"]
            + df["close"]
        ) / 3

        trend = []

        for i in range(len(df)):

            if i == 0:

                trend.append(1)

            else:

                if hlc.iloc[i] > hlc.iloc[i - 1]:

                    trend.append(1)

                else:

                    trend.append(-1)

        df["trend"] = trend

        df["dm"] = (
            df["high"]
            - df["low"]
        )

        df["vf"] = (
            df["volume"]
            * df["trend"]
            * df["dm"]
        )

        fast_ema = (
            df["vf"]
            .ewm(
                span=fast,
                adjust=False
            )
            .mean()
        )

        slow_ema = (
            df["vf"]
            .ewm(
                span=slow,
                adjust=False
            )
            .mean()
        )

        kvo = fast_ema - slow_ema

        signal_line = (
            kvo
            .ewm(
                span=signal,
                adjust=False
            )
            .mean()
        )

        return kvo, signal_line


# =========================================================
# VOLUME MA20
# =========================================================

    def volume_ma20(
        self,
        candles
    ):

        df = pd.DataFrame(candles)

        df["volume"] = df["volume"].astype(float)

        return (
            df["volume"]
            .rolling(20)
            .mean()
        )


# =========================================================
# FINAL KVO CONFIRMATION
# =========================================================

    def kvo_confirmation(
        self,
        candles
    ):

        kvo, signal = self.calculate_kvo(
            candles
        )

        volume_ma = self.volume_ma20(
            candles
        )

        previous_kvo = kvo.iloc[-2]
        current_kvo = kvo.iloc[-1]

        previous_signal = signal.iloc[-2]
        current_signal = signal.iloc[-1]

        current_volume_ma = volume_ma.iloc[-1]

        # LONG CONDITION
        if (

            previous_kvo < previous_signal

            and

            current_kvo > current_signal

            and

            current_kvo > 0

            and

            current_signal > 0

            and

            current_kvo > current_volume_ma

            and

            current_signal > current_volume_ma

        ):

            return LONG

        # SHORT CONDITION
        if (

            previous_kvo > previous_signal

            and

            current_kvo < current_signal

            and

            current_kvo < 0

            and

            current_signal < 0

            and

            current_kvo < current_volume_ma

            and

            current_signal < current_volume_ma

        ):

            return SHORT

        return NO_SIGNAL
        # =========================================================
# PART 3
# RSI + ADX + ATR
# =========================================================

    # -----------------------------------------------------
    # RSI
    # -----------------------------------------------------

    def calculate_rsi(
        self,
        candles,
        period=14
    ):

        df = pd.DataFrame(candles)

        close = df["close"].astype(float)

        delta = close.diff()

        gain = delta.where(delta > 0, 0)

        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(period).mean()

        avg_loss = loss.rolling(period).mean()

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        return rsi


    # -----------------------------------------------------
    # RSI Confirmation
    # -----------------------------------------------------

    def rsi_confirmation(
        self,
        rsi
    ):

        current = rsi.iloc[-1]

        if current > 55:

            return LONG

        elif current < 45:

            return SHORT

        return NO_SIGNAL


    # -----------------------------------------------------
    # ATR
    # -----------------------------------------------------

    def calculate_atr(
        self,
        candles,
        period=14
    ):

        df = pd.DataFrame(candles)

        high = df["high"].astype(float)

        low = df["low"].astype(float)

        close = df["close"].astype(float)

        tr1 = high - low

        tr2 = (high - close.shift()).abs()

        tr3 = (low - close.shift()).abs()

        tr = pd.concat(
            [tr1, tr2, tr3],
            axis=1
        ).max(axis=1)

        atr = tr.rolling(period).mean()

        return atr


    # -----------------------------------------------------
    # ADX
    # -----------------------------------------------------

    def calculate_adx(
        self,
        candles,
        period=14
    ):

        df = pd.DataFrame(candles)

        high = df["high"].astype(float)

        low = df["low"].astype(float)

        close = df["close"].astype(float)

        plus_dm = high.diff()

        minus_dm = -low.diff()

        plus_dm[plus_dm < 0] = 0

        minus_dm[minus_dm < 0] = 0

        tr = pd.concat(

            [

                high - low,

                (high - close.shift()).abs(),

                (low - close.shift()).abs()

            ],

            axis=1

        ).max(axis=1)

        atr = tr.rolling(period).mean()

        plus_di = 100 * (
            plus_dm.rolling(period).mean() / atr
        )

        minus_di = 100 * (
            minus_dm.rolling(period).mean() / atr
        )

        dx = (
            (
                (plus_di - minus_di).abs()
            )
            /
            (
                plus_di + minus_di
            )
        ) * 100

        adx = dx.rolling(period).mean()

        return adx


    # -----------------------------------------------------
    # ADX Confirmation
    # -----------------------------------------------------

    def adx_confirmation(
        self,
        adx
    ):

        current = adx.iloc[-1]

        if current >= 25:

            return True

        return False
        # =========================================================
# PART 4
# VWAP + VOLUME MA20 + CVD
# =========================================================


# -----------------------------------------------------
# VWAP
# -----------------------------------------------------

    def calculate_vwap(
        self,
        candles
    ):

        df = pd.DataFrame(candles)

        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)

        typical_price = (
            df["high"]
            + df["low"]
            + df["close"]
        ) / 3

        cumulative_volume = (
            df["volume"]
            .cumsum()
        )

        cumulative_price_volume = (
            typical_price
            * df["volume"]
        ).cumsum()

        vwap = (
            cumulative_price_volume
            / cumulative_volume
        )

        return vwap


# -----------------------------------------------------
# VWAP POSITION
# -----------------------------------------------------

    def vwap_confirmation(
        self,
        candles
    ):

        df = pd.DataFrame(candles)

        df["close"] = df["close"].astype(float)

        vwap = self.calculate_vwap(
            candles
        )

        current_price = df["close"].iloc[-1]
        current_vwap = vwap.iloc[-1]

        if current_price > current_vwap:

            return ABOVE_VWAP

        elif current_price < current_vwap:

            return BELOW_VWAP

        return NO_SIGNAL


# -----------------------------------------------------
# VOLUME MA20
# -----------------------------------------------------

    def volume_confirmation(
        self,
        candles
    ):

        df = pd.DataFrame(candles)

        df["volume"] = df["volume"].astype(float)

        volume_ma20 = (
            df["volume"]
            .rolling(20)
            .mean()
        )

        current_volume = df["volume"].iloc[-1]
        current_ma = volume_ma20.iloc[-1]

        if current_volume > current_ma:

            return STRONG_VOLUME

        return WEAK_VOLUME


# -----------------------------------------------------
# CVD
# -----------------------------------------------------

    def calculate_cvd(
        self,
        candles
    ):

        df = pd.DataFrame(candles)

        df["open"] = df["open"].astype(float)
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)

        delta = []

        for i in range(len(df)):

            if df["close"].iloc[i] > df["open"].iloc[i]:

                delta.append(
                    df["volume"].iloc[i]
                )

            elif df["close"].iloc[i] < df["open"].iloc[i]:

                delta.append(
                    -df["volume"].iloc[i]
                )

            else:

                delta.append(0)

        df["delta"] = delta

        cvd = (
            df["delta"]
            .cumsum()
        )

        return cvd


# -----------------------------------------------------
# CVD CONFIRMATION
# -----------------------------------------------------

    def cvd_confirmation(
        self,
        candles
    ):

        cvd = self.calculate_cvd(
            candles
        )

        previous = cvd.iloc[-2]
        current = cvd.iloc[-1]

        if current > previous:

            return BULLISH_CVD

        elif current < previous:

            return BEARISH_CVD

        return NO_SIGNAL
        # =========================================================
# =========================================================
# PART 5
# OPEN INTEREST + FUNDING + MULTI TIMEFRAME
# =========================================================


# -----------------------------------------------------
# BINANCE OPEN INTEREST
# -----------------------------------------------------

    def get_open_interest(
        self,
        symbol
    ):

        url = (
            "https://fapi.binance.com/fapi/v1/openInterest"
        )

        params = {
            "symbol": symbol
        }

        response = requests.get(
            url,
            params=params
        )

        data = response.json()

        return data

        url = (
            "https://fapi.binance.com/fapi/v1/openInterest"
        )

        params = {
            "symbol": symbol
        }

        data = requests.get(
            url,
            params=params
        ).json()

        return float(
            data["openInterest"]
        )


# -----------------------------------------------------
# FUNDING RATE
# -----------------------------------------------------

    def get_funding_rate(
        self,
        symbol
    ):

        url = (
            "https://fapi.binance.com/fapi/v1/premiumIndex"
        )

        params = {
            "symbol": symbol
        }

        data = requests.get(
            url,
            params=params
        ).json()

        return float(
            data["lastFundingRate"]
        )


# -----------------------------------------------------
# OI + FUNDING CONFIRMATION
# -----------------------------------------------------

    def oi_confirmation(

        self,

        current_oi,

        previous_oi,

        funding

    ):

        oi_change = (

            (

                current_oi
                -
                previous_oi

            )

            /

            previous_oi

        ) * 100


        if (

            oi_change >= 5

            and

            funding < 0.05

        ):

            return LONG_SUPPORT


        elif (

            oi_change >= 5

            and

            funding > 0.05

        ):

            return SHORT_SUPPORT


        return NO_SIGNAL


# -----------------------------------------------------
# MULTI TIMEFRAME
# -----------------------------------------------------

    def multi_timeframe_confirmation(

        self,

        data15,

        data1h,

        data4h

    ):

        ema15 = self.ema_cross(data15)

        ema1h = self.ema_cross(data1h)

        ema4h = self.ema_cross(data4h)


        if (

            ema15 == LONG

            and

            ema1h == LONG

            and

            ema4h == LONG

        ):

            return LONG


        elif (

            ema15 == SHORT

            and

            ema1h == SHORT

            and

            ema4h == SHORT

        ):

            return SHORT


        return NO_SIGNAL


# =========================================================
# PART 5 END
# =========================================================
# =========================================================
# PART 6
# FINAL INDICATOR PACK
# =========================================================

    def build_indicator_package(
        self,
        data15,
        data1h,
        data4h,
        symbol,
        previous_oi
    ):

        package = {}

        # EMA
        package["ema"] = self.ema_cross(data15)

        # KVO
        package["kvo"] = self.kvo_confirmation(data15)

        # RSI
        rsi = self.calculate_rsi(data15)
        package["rsi"] = self.rsi_confirmation(rsi)

        # ADX
        adx = self.calculate_adx(data15)
        package["adx"] = self.adx_confirmation(adx)

        # ATR
        atr = self.calculate_atr(data15)
        package["atr"] = float(atr.iloc[-1])

        # VWAP
        package["vwap"] = self.vwap_confirmation(data15)

        # Volume
        package["volume"] = self.volume_confirmation(data15)

        # CVD
        package["cvd"] = self.cvd_confirmation(data15)

        # Open Interest
        try:

            current_oi = self.get_open_interest(symbol)

            funding = self.get_funding_rate(symbol)

            package["oi"] = self.oi_confirmation(
                current_oi,
                previous_oi,
                funding
            )

            package["current_oi"] = current_oi
            package["funding"] = funding

        except Exception:

            package["oi"] = NO_SIGNAL

            package["current_oi"] = 0

            package["funding"] = 0

        # Multi Timeframe
        package["timeframe"] = self.multi_timeframe_confirmation(
            data15,
            data1h,
            data4h
        )

        return package


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("Indicator Engine Final Loaded")