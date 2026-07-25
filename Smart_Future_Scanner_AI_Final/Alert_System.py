# =========================================================
# SMART FUTURE SCANNER AI
# ALERT SYSTEM
# PART 1
# =========================================================

from datetime import datetime

# =========================================================
# ALERT TYPES
# =========================================================

LONG = "LONG"

SHORT = "SHORT"

STRONG_LONG = "STRONG_LONG"

STRONG_SHORT = "STRONG_SHORT"

NO_SIGNAL = "NONE"


# =========================================================
# ALERT SYSTEM
# =========================================================

class AlertSystem:

    def __init__(self):

        print(

            "Alert System Loaded"

        )


    # -----------------------------------------------------
    # CREATE ALERT
    # -----------------------------------------------------

    def create_alert(

        self,

        trade

    ):

        if trade is None:

            return None


        alert = {

            "time":

            datetime.now(),

            "signal":

            trade["signal"],

            "confidence":

            trade["confidence"],

            "entry":

            trade["entry"],

            "stop_loss":

            trade["stop_loss"],

            "take_profit":

            trade["take_profit"],

            "risk_reward":

            trade["risk_reward"],

            "leverage":

            trade["leverage"]

        }

        return alert


# =========================================================
# PART 1 END
# =========================================================
# =========================================================
# ALERT SYSTEM
# PART 2
# MESSAGE BUILDER
# =========================================================

    # -----------------------------------------------------
    # FORMAT ALERT MESSAGE
    # -----------------------------------------------------

    def build_message(self, alert):

        if alert is None:
            return None

        message = f"""
==================================

SMART FUTURE SCANNER AI

==================================

SIGNAL      : {alert['signal']}

CONFIDENCE  : {alert['confidence']}

ENTRY       : {alert['entry']}

STOP LOSS   : {alert['stop_loss']}

TAKE PROFIT : {alert['take_profit']}

R:R         : {alert['risk_reward']}

LEVERAGE    : {alert['leverage']}X

TIME        : {alert['time']}

==================================
"""

        return message


    # -----------------------------------------------------
    # CONSOLE ALERT
    # -----------------------------------------------------

    def print_alert(self, alert):

        message = self.build_message(alert)

        if message is None:
            return

        print(message)


    # -----------------------------------------------------
    # ALERT LOG
    # -----------------------------------------------------

    def save_log(self, message):

        if message is None:
            return

        with open("scanner_alert_log.txt", "a", encoding="utf-8") as file:

            file.write(message)

            file.write("\n\n")
            # =========================================================
# ALERT SYSTEM
# PART 3
# ALERT FILTER
# =========================================================

    # -----------------------------------------------------
    # CONFIDENCE FILTER
    # -----------------------------------------------------

    def confidence_filter(
        self,
        alert
    ):

        if alert is None:

            return False

        if alert["confidence"] == "WEAK":

            return False

        return True


    # -----------------------------------------------------
    # RISK FILTER
    # -----------------------------------------------------

    def risk_filter(
        self,
        alert
    ):

        if alert is None:

            return False

        if alert["risk_reward"] < 2:

            return False

        return True


    # -----------------------------------------------------
    # LEVERAGE FILTER
    # -----------------------------------------------------

    def leverage_filter(
        self,
        alert
    ):

        if alert is None:

            return False

        if alert["leverage"] > 20:

            return False

        return True


    # -----------------------------------------------------
    # FINAL FILTER
    # -----------------------------------------------------

    def validate_alert(
        self,
        alert
    ):

        if not self.confidence_filter(alert):

            return False

        if not self.risk_filter(alert):

            return False

        if not self.leverage_filter(alert):

            return False

        return True


    # -----------------------------------------------------
    # PROCESS ALERT
    # -----------------------------------------------------

    def process_alert(
        self,
        alert
    ):

        if not self.validate_alert(alert):

            return

        message = self.build_message(alert)

        self.print_alert(alert)

        self.save_log(message)
        # -----------------------------------------------------
    # SEND ALL ALERTS
    # -----------------------------------------------------

    def send_all(self, message):

        if message is None:
            return

        print(message)

        self.save_log(message)