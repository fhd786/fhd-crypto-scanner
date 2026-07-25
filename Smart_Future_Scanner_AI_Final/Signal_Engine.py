# =========================================================
# SMART FUTURE SCANNER AI
# SIGNAL ENGINE - FINAL FIXED VERSION
# DEVELOPED FOR: Smart Future Scanner AI by FHD Crypto Royal Zone
# =========================================================

from Indicator_Engine import *

STRONG_LONG = "STRONG_LONG"
LONG = "LONG"
STRONG_SHORT = "STRONG_SHORT"
SHORT = "SHORT"
NO_SIGNAL = "NONE"

VERY_STRONG = "VERY_STRONG"
STRONG = "STRONG"
MEDIUM = "MEDIUM"
WEAK = "WEAK"


class RiskManager:

    def __init__(self):
        print("Risk Manager Loaded")

    def calculate_stop_loss(self, entry, atr, signal):
        if signal in [LONG, STRONG_LONG]:
            return entry - (atr * 1.5)
        elif signal in [SHORT, STRONG_SHORT]:
            return entry + (atr * 1.5)
        return entry

    def calculate_take_profit(self, entry, atr, signal):
        if signal in [LONG, STRONG_LONG]:
            return entry + (atr * 3)
        elif signal in [SHORT, STRONG_SHORT]:
            return entry - (atr * 3)
        return entry

    def risk_reward(self, entry, sl, tp):
        risk = abs(entry - sl)
        reward = abs(tp - entry)
        if risk == 0:
            return 0
        return round(reward / risk, 2)

    def suggested_leverage(self, confidence):
        if confidence == VERY_STRONG:
            return 20
        elif confidence == STRONG:
            return 15
        elif confidence == MEDIUM:
            return 10
        return 5

    def build_trade(self, signal, confidence, entry, atr):
        sl = self.calculate_stop_loss(entry, atr, signal)
        tp = self.calculate_take_profit(entry, atr, signal)
        rr = self.risk_reward(entry, sl, tp)
        leverage = self.suggested_leverage(confidence)

        return {
            "entry": round(entry, 6),
            "stop_loss": round(sl, 6),
            "take_profit": round(tp, 6),
            "risk_reward": rr,
            "leverage": leverage
        }


class SignalEngine:

    def __init__(self):
        self.risk_manager = RiskManager()
        print("Signal Engine Loaded Successfully")

    def generate_base_score(self, indicators):
        long_score = 0
        short_score = 0

        if indicators.get("ema") == LONG:
            long_score += 20
        elif indicators.get("ema") == SHORT:
            short_score += 20

        if indicators.get("kvo") == LONG:
            long_score += 20
        elif indicators.get("kvo") == SHORT:
            short_score += 20

        if indicators.get("rsi") == LONG:
            long_score += 10
        elif indicators.get("rsi") == SHORT:
            short_score += 10

        if indicators.get("adx"):
            long_score += 10
            short_score += 10

        return long_score, short_score

    def update_scores(self, indicators, long_score, short_score):
        if indicators.get("vwap") == ABOVE_VWAP:
            long_score += 10
        elif indicators.get("vwap") == BELOW_VWAP:
            short_score += 10

        if indicators.get("volume") == STRONG_VOLUME:
            long_score += 5
            short_score += 5

        if indicators.get("cvd") == BULLISH_CVD:
            long_score += 10
        elif indicators.get("cvd") == BEARISH_CVD:
            short_score += 10

        if indicators.get("oi") == LONG_SUPPORT:
            long_score += 10
        elif indicators.get("oi") == SHORT_SUPPORT:
            short_score += 10

        if indicators.get("timeframe") == LONG:
            long_score += 15
        elif indicators.get("timeframe") == SHORT:
            short_score += 15

        return long_score, short_score

    def confidence_level(self, long_score, short_score):
        score = max(long_score, short_score)
        if score >= 90:
            return VERY_STRONG
        elif score >= 75:
            return STRONG
        elif score >= 60:
            return MEDIUM
        return WEAK

    def final_signal(self, long_score, short_score):
        if long_score >= 80:
            return STRONG_LONG
        elif long_score >= 60:
            return LONG
        elif short_score >= 80:
            return STRONG_SHORT
        elif short_score >= 60:
            return SHORT
        return NO_SIGNAL

    def build_signal(self, indicators):
        long_score, short_score = self.generate_base_score(indicators)
        long_score, short_score = self.update_scores(indicators, long_score, short_score)

        signal = self.final_signal(long_score, short_score)
        confidence = self.confidence_level(long_score, short_score)

        return {
            "signal": signal,
            "confidence": confidence,
            "long_score": long_score,
            "short_score": short_score
        }

    def validate_signal(self, signal_data):
        if signal_data["signal"] == NO_SIGNAL or signal_data["confidence"] == WEAK:
            return False
        return True

    def process(self, indicators):
        signal_data = self.build_signal(indicators)

        if not self.validate_signal(signal_data):
            return None

        entry_price = indicators.get("entry", 0)
        atr = indicators.get("atr", 0)

        trade = self.risk_manager.build_trade(
            signal_data["signal"],
            signal_data["confidence"],
            entry_price,
            atr
        )

        if trade["risk_reward"] < 1.5:
            return None

        return {
            "signal": signal_data["signal"],
            "confidence": signal_data["confidence"],
            "entry": trade["entry"],
            "stop_loss": trade["stop_loss"],
            "take_profit": trade["take_profit"],
            "risk_reward": trade["risk_reward"],
            "leverage": trade["leverage"],
            "long_score": signal_data["long_score"],
            "short_score": signal_data["short_score"]
        }


if __name__ == "__main__":
    print("Signal Engine Final Loaded")