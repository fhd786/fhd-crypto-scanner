# =========================================================
# SMART FUTURE SCANNER AI
# INDICATOR ENGINE - FINAL FIXED VERSION
# DEVELOPED FOR: Smart Future Scanner AI by FHD Crypto Royal Zone
# =========================================================

import requests
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
# INDICATOR ENGINE CLASS
# =========================================================

class IndicatorEngine:

    def __init__(self):
        print("Indicator Engine Loaded Successfully")

    # =====================================================
    # 1. EMA & EMA GOLDEN CROSS (EMA 5 / EMA 50)
    # =====================================================

    def calculate_ema(self, candles, period):
        df = pd.DataFrame(candles)
        df["close"] = df["close"].astype(float)
        return df["close"].ewm(span=period, adjust=False).mean()

    def ema_cross(self, candles):
        if len(candles) < 50:
            return NO_SIGNAL

        ema5 = self.calculate_ema(candles, 5)
        ema50 = self.calculate_ema(candles, 50)

        previous5 = ema5.iloc[-2]
        previous50 = ema50.iloc[-2]

        current5 = ema5.iloc[-1]
        current50 = ema50.iloc[-1]

        if previous5 < previous50 and current5 > current50:
            return LONG
        elif previous5 > previous50 and current5 < current50:
            return SHORT

        return NO_SIGNAL

    # =====================================================
    # 2. KLINGER VOLUME OSCILLATOR (KVO 38/60) & VOLUME MA 20
    # =====================================================

    def calculate_kvo(self, candles, fast=38, slow=60, signal=13):
        df = pd.DataFrame(candles)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)

        hlc = (df["high"] + df["low"] + df["close"]) / 3
        trend = np.where(hlc > hlc.shift(1), 1, -1)
        trend[0] = 1

        dm = df["high"] - df["low"]
        vf = df["volume"] * trend * dm

        fast_ema = vf.ewm(span=fast, adjust=False).mean()
        slow_ema = vf.ewm(span=slow, adjust=False).mean()

        kvo = fast_ema - slow_ema
        signal_line = kvo.ewm(span=signal, adjust=False).mean()

        # Volume MA 20
        volume_ma20 = df["volume"].rolling(window=20, min_periods=1).mean()

        return kvo, signal_line, volume_ma20

    def kvo_confirmation(self, candles):
        if len(candles) < 65:
            return NO_SIGNAL

        kvo, signal, vol_ma20 = self.calculate_kvo(candles, fast=38, slow=60)
        df = pd.DataFrame(candles)
        current_volume = float(df["close"].iloc[-1])

        previous_kvo = kvo.iloc[-2]
        current_kvo = kvo.iloc[-1]

        previous_signal = signal.iloc[-2]
        current_signal = signal.iloc[-1]

        current_vol_ma = vol_ma20.iloc[-1]
        current_vol = float(df["volume"].iloc[-1])

        # LONG CONDITION:
        # KVO crosses Signal Line, both are above 0, and volume > 20 Volume MA
        if (
            previous_kvo < previous_signal
            and current_kvo > current_signal
            and current_kvo > 0
            and current_signal > 0
            and current_vol > current_vol_ma
        ):
            return LONG

        # SHORT CONDITION:
        if (
            previous_kvo > previous_signal
            and current_kvo < current_signal
            and current_kvo < 0
            and current_signal < 0
            and current_vol > current_vol_ma
        ):
            return SHORT

        return NO_SIGNAL

    # =====================================================
    # 3. RSI & ADX & ATR
    # =====================================================

    def calculate_rsi(self, candles, period=14):
        df = pd.DataFrame(candles)
        close = df["close"].astype(float)
        delta = close.diff()

        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(period, min_periods=1).mean()
        avg_loss = loss.rolling(period, min_periods=1).mean()

        rs = avg_gain / (avg_loss + 1e-10)
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def rsi_confirmation(self, rsi):
        current = rsi.iloc[-1]
        if current > 55:
            return LONG
        elif current < 45:
            return SHORT
        return NO_SIGNAL

    def calculate_atr(self, candles, period=14):
        df = pd.DataFrame(candles)
        high = df["high"].astype(float)
        low = df["low"].astype(float)
        close = df["close"].astype(float)

        tr1 = high - low
        tr2 = (high - close.shift()).abs()
        tr3 = (low - close.shift()).abs()

        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(period, min_periods=1).mean()
        return atr

    def calculate_adx(self, candles, period=14):
        df = pd.DataFrame(candles)
        high = df["high"].astype(float)
        low = df["low"].astype(float)
        close = df["close"].astype(float)

        plus_dm = high.diff()
        minus_dm = -low.diff()

        plus_dm = np.where((plus_dm > minus_dm) & (plus_dm > 0), plus_dm, 0)
        minus_dm = np.where((minus_dm > plus_dm) & (minus_dm > 0), minus_dm, 0)

        tr1 = high - low
        tr2 = (high - close.shift()).abs()
        tr3 = (low - close.shift()).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        atr = tr.rolling(period, min_periods=1).mean()

        plus_di = 100 * (pd.Series(plus_dm).rolling(period, min_periods=1).mean() / (atr + 1e-10))
        minus_di = 100 * (pd.Series(minus_dm).rolling(period, min_periods=1).mean() / (atr + 1e-10))

        dx = ((plus_di - minus_di).abs() / (plus_di + minus_di + 1e-10)) * 100
        adx = dx.rolling(period, min_periods=1).mean()
        return adx

    def adx_confirmation(self, adx):
        current = adx.iloc[-1]
        return current >= 25

    # =====================================================
    # 4. VWAP & VOLUME MA20 & CVD
    # =====================================================

    def calculate_vwap(self, candles):
        df = pd.DataFrame(candles)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)

        typical_price = (df["high"] + df["low"] + df["close"]) / 3
        cumulative_volume = df["volume"].cumsum()
        cumulative_price_volume = (typical_price * df["volume"]).cumsum()

        vwap = cumulative_price_volume / (cumulative_volume + 1e-10)
        return vwap

    def vwap_confirmation(self, candles):
        df = pd.DataFrame(candles)
        df["close"] = df["close"].astype(float)
        vwap = self.calculate_vwap(candles)

        current_price = df["close"].iloc[-1]
        current_vwap = vwap.iloc[-1]

        if current_price > current_vwap:
            return ABOVE_VWAP
        elif current_price < current_vwap:
            return BELOW_VWAP
        return NO_SIGNAL

    def volume_confirmation(self, candles):
        df = pd.DataFrame(candles)
        df["volume"] = df["volume"].astype(float)

        volume_ma20 = df["volume"].rolling(20, min_periods=1).mean()

        current_volume = df["volume"].iloc[-1]
        current_ma = volume_ma20.iloc[-1]

        if current_volume > current_ma:
            return STRONG_VOLUME
        return WEAK_VOLUME

    def calculate_cvd(self, candles):
        df = pd.DataFrame(candles)
        df["open"] = df["open"].astype(float)
        df["close"] = df["close"].astype(float)
        df["volume"] = df["volume"].astype(float)

        delta = np.where(
            df["close"] > df["open"], 
            df["volume"], 
            np.where(df["close"] < df["open"], -df["volume"], 0)
        )

        cvd = pd.Series(delta).cumsum()
        return cvd

    def cvd_confirmation(self, candles):
        cvd = self.calculate_cvd(candles)
        previous = cvd.iloc[-2]
        current = cvd.iloc[-1]

        if current > previous:
            return BULLISH_CVD
        elif current < previous:
            return BEARISH_CVD
        return NO_SIGNAL

    # =====================================================
    # 5. OPEN INTEREST & FUNDING RATE
    # =====================================================

    def get_open_interest(self, symbol):
        try:
            url = "https://fapi.binance.com/fapi/v1/openInterest"
            params = {"symbol": symbol}
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return float(data.get("openInterest", 0))
        except Exception:
            pass
        return 0.0

    def get_funding_rate(self, symbol):
        try:
            url = "https://fapi.binance.com/fapi/v1/premiumIndex"
            params = {"symbol": symbol}
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return float(data.get("lastFundingRate", 0))
        except Exception:
            pass
        return 0.0

    def oi_confirmation(self, current_oi, previous_oi, funding):
        if previous_oi == 0:
            return NO_SIGNAL

        oi_change = ((current_oi - previous_oi) / previous_oi) * 100

        if oi_change >= 5 and funding < 0.05:
            return LONG_SUPPORT
        elif oi_change >= 5 and funding > 0.05:
            return SHORT_SUPPORT

        return NO_SIGNAL

    def multi_timeframe_confirmation(self, data15, data1h, data4h):
        ema15 = self.ema_cross(data15)
        ema1h = self.ema_cross(data1h)
        ema4h = self.ema_cross(data4h)

        if ema15 == LONG and ema1h == LONG and ema4h == LONG:
            return LONG
        elif ema15 == SHORT and ema1h == SHORT and ema4h == SHORT:
            return SHORT

        return NO_SIGNAL

    # =====================================================
    # 6. BUILD COMPLETE INDICATOR PACKAGE
    # =====================================================

    def build_indicator_package(self, data15, data1h, data4h, symbol, previous_oi=0):
        package = {}

        package["ema"] = self.ema_cross(data15)
        package["kvo"] = self.kvo_confirmation(data15)

        rsi = self.calculate_rsi(data15)
        package["rsi"] = self.rsi_confirmation(rsi)

        adx = self.calculate_adx(data15)
        package["adx"] = self.adx_confirmation(adx)

        atr = self.calculate_atr(data15)
        package["atr"] = float(atr.iloc[-1]) if len(atr) > 0 else 0.0

        package["vwap"] = self.vwap_confirmation(data15)
        package["volume"] = self.volume_confirmation(data15)
        package["cvd"] = self.cvd_confirmation(data15)

        current_oi = self.get_open_interest(symbol)
        funding = self.get_funding_rate(symbol)

        package["oi"] = self.oi_confirmation(current_oi, previous_oi, funding)
        package["current_oi"] = current_oi
        package["funding"] = funding

        package["timeframe"] = self.multi_timeframe_confirmation(data15, data1h, data4h)
        
        # Current Price
        df_15m = pd.DataFrame(data15)
        package["entry"] = float(df_15m["close"].iloc[-1]) if len(df_15m) > 0 else 0.0

        return package


if __name__ == "__main__":
    print("Indicator Engine Final Loaded")