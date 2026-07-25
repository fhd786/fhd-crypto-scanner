# =========================================================
# SMART FUTURE SCANNER AI
# SIGNAL ENGINE
# PART 1
# =========================================================

from Indicator_Engine import *

# =========================================================
# SIGNAL CONSTANTS
# =========================================================

STRONG_LONG = "STRONG_LONG"
LONG = "LONG"

STRONG_SHORT = "STRONG_SHORT"
SHORT = "SHORT"

NO_SIGNAL = "NONE"

VERY_STRONG = "VERY_STRONG"
STRONG = "STRONG"
MEDIUM = "MEDIUM"
WEAK = "WEAK"


# =========================================================
# SIGNAL ENGINE
# =========================================================

class SignalEngine:

    def __init__(self):

        print(
            "Signal Engine Loaded"
        )


    # -----------------------------------------------------
    # FINAL SIGNAL DECISION
    # -----------------------------------------------------

    def generate_signal(
        self,
        indicators
    ):

        long_score = 0
        short_score = 0


        # EMA
        if indicators["ema"] == LONG:
            long_score += 20

        elif indicators["ema"] == SHORT:
            short_score += 20


        # KVO
        if indicators["kvo"] == LONG:
            long_score += 20

        elif indicators["kvo"] == SHORT:
            short_score += 20


        # RSI
        if indicators["rsi"] == LONG:
            long_score += 10

        elif indicators["rsi"] == SHORT:
            short_score += 10


        # ADX
        if indicators["adx"]:
            long_score += 10
            short_score += 10


        return {

            "long_score": long_score,

            "short_score": short_score

        }
        # =========================================================
# SIGNAL ENGINE
# PART 2
# VWAP + VOLUME + CVD + OI + FUNDING + MTF
# =========================================================

    # -----------------------------------------------------
    # VWAP SCORE
    # -----------------------------------------------------

    def vwap_score(
        self,
        indicators,
        long_score,
        short_score
    ):

        if indicators["vwap"] == ABOVE_VWAP:

            long_score += 10

        elif indicators["vwap"] == BELOW_VWAP:

            short_score += 10

        return long_score, short_score


    # -----------------------------------------------------
    # VOLUME SCORE
    # -----------------------------------------------------

    def volume_score(
        self,
        indicators,
        long_score,
        short_score
    ):

        if indicators["volume"] == STRONG_VOLUME:

            long_score += 5
            short_score += 5

        return long_score, short_score


    # -----------------------------------------------------
    # CVD SCORE
    # -----------------------------------------------------

    def cvd_score(
        self,
        indicators,
        long_score,
        short_score
    ):

        if indicators["cvd"] == BULLISH_CVD:

            long_score += 10

        elif indicators["cvd"] == BEARISH_CVD:

            short_score += 10

        return long_score, short_score


    # -----------------------------------------------------
    # OPEN INTEREST SCORE
    # -----------------------------------------------------

    def oi_score(
        self,
        indicators,
        long_score,
        short_score
    ):

        if indicators["oi"] == LONG_SUPPORT:

            long_score += 10

        elif indicators["oi"] == SHORT_SUPPORT:

            short_score += 10

        return long_score, short_score


    # -----------------------------------------------------
    # MULTI TIMEFRAME SCORE
    # -----------------------------------------------------

    def timeframe_score(
        self,
        indicators,
        long_score,
        short_score
    ):

        if indicators["timeframe"] == LONG:

            long_score += 15

        elif indicators["timeframe"] == SHORT:

            short_score += 15

        return long_score, short_score


    # -----------------------------------------------------
    # UPDATE FINAL SCORES
    # -----------------------------------------------------

    def update_scores(
        self,
        indicators,
        long_score,
        short_score
    ):

        long_score, short_score = self.vwap_score(
            indicators,
            long_score,
            short_score
        )

        long_score, short_score = self.volume_score(
            indicators,
            long_score,
            short_score
        )

        long_score, short_score = self.cvd_score(
            indicators,
            long_score,
            short_score
        )

        long_score, short_score = self.oi_score(
            indicators,
            long_score,
            short_score
        )

        long_score, short_score = self.timeframe_score(
            indicators,
            long_score,
            short_score
        )

        return long_score, short_score
        # =========================================================
# SIGNAL ENGINE
# PART 3
# CONFIDENCE + FINAL DECISION
# =========================================================

    # -----------------------------------------------------
    # CONFIDENCE SCORE
    # -----------------------------------------------------

    def confidence_level(
        self,
        long_score,
        short_score
    ):

        if long_score >= short_score:

            score = long_score

        else:

            score = short_score


        if score >= 90:

            return VERY_STRONG

        elif score >= 75:

            return STRONG

        elif score >= 60:

            return MEDIUM

        return WEAK


    # -----------------------------------------------------
    # FINAL SIGNAL
    # -----------------------------------------------------

    def final_signal(
        self,
        long_score,
        short_score
    ):

        if long_score >= 80:

            return STRONG_LONG

        elif long_score >= 60:

            return LONG

        elif short_score >= 80:

            return STRONG_SHORT

        elif short_score >= 60:

            return SHORT

        return NO_SIGNAL


    # -----------------------------------------------------
    # BUILD FINAL SIGNAL
    # -----------------------------------------------------

    def build_signal(
        self,
        indicators
    ):

        scores = self.generate_signal(
            indicators
        )

        long_score = scores["long_score"]
        short_score = scores["short_score"]

        long_score, short_score = self.update_scores(
            indicators,
            long_score,
            short_score
        )

        signal = self.final_signal(
            long_score,
            short_score
        )

        confidence = self.confidence_level(
            long_score,
            short_score
        )

        return {

            "signal": signal,

            "confidence": confidence,

            "long_score": long_score,

            "short_score": short_score

        }
        # =========================================================
# SIGNAL ENGINE
# PART 4
# RISK MANAGEMENT
# =========================================================

class RiskManager:

    def __init__(self):

        print("Risk Manager Loaded")


    # -----------------------------------------------------
    # STOP LOSS
    # -----------------------------------------------------

    def calculate_stop_loss(
        self,
        entry,
        atr,
        signal
    ):

        if signal in ["LONG", "STRONG_LONG"]:

            return entry - (atr * 1.5)

        elif signal in ["SHORT", "STRONG_SHORT"]:

            return entry + (atr * 1.5)

        return entry


    # -----------------------------------------------------
    # TAKE PROFIT
    # -----------------------------------------------------

    def calculate_take_profit(
        self,
        entry,
        atr,
        signal
    ):

        if signal in ["LONG", "STRONG_LONG"]:

            return entry + (atr * 3)

        elif signal in ["SHORT", "STRONG_SHORT"]:

            return entry - (atr * 3)

        return entry


    # -----------------------------------------------------
    # RISK / REWARD
    # -----------------------------------------------------

    def risk_reward(
        self,
        entry,
        sl,
        tp
    ):

        risk = abs(entry - sl)

        reward = abs(tp - entry)

        if risk == 0:

            return 0

        return round(
            reward / risk,
            2
        )


    # -----------------------------------------------------
    # LEVERAGE
    # -----------------------------------------------------

    def suggested_leverage(
        self,
        confidence
    ):

        if confidence == "VERY_STRONG":

            return 20

        elif confidence == "STRONG":

            return 15

        elif confidence == "MEDIUM":

            return 10

        return 5


    # -----------------------------------------------------
    # BUILD TRADE
    # -----------------------------------------------------

    def build_trade(
        self,
        signal,
        confidence,
        entry,
        atr
    ):

        sl = self.calculate_stop_loss(
            entry,
            atr,
            signal
        )

        tp = self.calculate_take_profit(
            entry,
            atr,
            signal
        )

        rr = self.risk_reward(
            entry,
            sl,
            tp
        )

        leverage = self.suggested_leverage(
            confidence
        )

        return {

            "entry": entry,

            "stop_loss": sl,

            "take_profit": tp,

            "risk_reward": rr,

            "leverage": leverage

        }
        # =========================================================
# SIGNAL ENGINE
# PART 5
# FINAL SCANNER FILTER
# =========================================================

    # -----------------------------------------------------
    # VALIDATE SIGNAL
    # -----------------------------------------------------

    def validate_signal(
        self,
        signal_data
    ):

        signal = signal_data["signal"]

        confidence = signal_data["confidence"]

        if signal == NO_SIGNAL:

            return False

        if confidence == WEAK:

            return False

        return True


    # -----------------------------------------------------
    # BUILD FINAL TRADE
    # -----------------------------------------------------

    def create_trade(
        self,
        indicators,
        entry_price
    ):

        signal_data = self.build_signal(
            indicators
        )

        if not self.validate_signal(
            signal_data
        ):

            return None


        risk = RiskManager()

        trade = risk.build_trade(

            signal_data["signal"],

            signal_data["confidence"],

            entry_price,

            indicators["atr"]

        )


        final_trade = {

            "signal":
            signal_data["signal"],

            "confidence":
            signal_data["confidence"],

            "entry":
            trade["entry"],

            "stop_loss":
            trade["stop_loss"],

            "take_profit":
            trade["take_profit"],

            "risk_reward":
            trade["risk_reward"],

            "leverage":
            trade["leverage"],

            "long_score":
            signal_data["long_score"],

            "short_score":
            signal_data["short_score"]

        }

        return final_trade


# -----------------------------------------------------
# FILTER
# -----------------------------------------------------

    def scanner_filter(
        self,
        trade
    ):

        if trade is None:

            return False

        if trade["risk_reward"] < 2:

            return False

        return True
        # =========================================================
# SIGNAL ENGINE
# PART 6
# FINAL EXECUTION
# =========================================================

# -----------------------------------------------------
# FINAL EXECUTION
# -----------------------------------------------------

    def execute(
        self,
        indicators,
        entry_price
    ):

        trade = self.create_trade(

            indicators,

            entry_price

        )

        if not self.scanner_filter(
            trade
        ):

            return None

        return trade


# -----------------------------------------------------
# FINAL REPORT
# -----------------------------------------------------

    def report(
        self,
        trade
    ):

        if trade is None:

            return "NO SIGNAL"

        report = f"""

============================

SMART FUTURE SCANNER AI

============================

SIGNAL      : {trade['signal']}

CONFIDENCE  : {trade['confidence']}

ENTRY       : {trade['entry']}

STOP LOSS   : {trade['stop_loss']}

TAKE PROFIT : {trade['take_profit']}

R:R         : {trade['risk_reward']}

LEVERAGE    : {trade['leverage']}X

LONG SCORE  : {trade['long_score']}

SHORT SCORE : {trade['short_score']}

============================

"""

        return report

# -----------------------------------------------------
    # PROCESS FOR MAIN ENGINE
    # -----------------------------------------------------

    def process(self, market_data):

        indicators = market_data

        entry_price = indicators.get("entry", 0)

        return self.execute(
            indicators,
            entry_price
        )
# -----------------------------------------------------
# TEST
# -----------------------------------------------------

if __name__ == "__main__":

    print(

        "Signal Engine Final Loaded"

    )