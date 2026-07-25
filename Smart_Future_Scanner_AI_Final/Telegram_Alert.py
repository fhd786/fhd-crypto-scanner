# =========================================================
# SMART FUTURE SCANNER AI
# TELEGRAM ALERT
# PART 1
# =========================================================

import requests

# =========================================================
# TELEGRAM CONFIG
# =========================================================

class TelegramAlert:

    def __init__(self):

        # بعد میں یہاں اپنا اصل Token ڈالیں گے
        self.bot_token = ""

        # بعد میں یہاں اپنا Chat ID ڈالیں گے
        self.chat_id = ""

        print("Telegram Alert Loaded")


    # -----------------------------------------------------
    # BUILD TELEGRAM URL
    # -----------------------------------------------------

    def telegram_url(self):

        return (
            f"https://api.telegram.org/bot"
            f"{self.bot_token}/sendMessage"
        )


    # -----------------------------------------------------
    # SEND MESSAGE
    # -----------------------------------------------------

    def send_message(self, message):

        if self.bot_token == "":
            return False

        if self.chat_id == "":
            return False

        payload = {

            "chat_id": self.chat_id,

            "text": message,

            "parse_mode": "HTML"

        }

        try:

            requests.post(

                self.telegram_url(),

                data=payload,

                timeout=10

            )

            return True

        except Exception:

            return False
            # =========================================================
# TELEGRAM ALERT
# PART 2
# FINAL
# =========================================================

    # -----------------------------------------------------
    # SEND TRADE ALERT
    # -----------------------------------------------------

    def send_trade_alert(self, trade):

        if trade is None:
            return False

        message = f"""
🚀 <b>SMART FUTURE SCANNER AI</b>

━━━━━━━━━━━━━━━━━━

📈 Signal : <b>{trade['signal']}</b>

🎯 Confidence : <b>{trade['confidence']}</b>

💰 Entry : <b>{trade['entry']}</b>

🛑 Stop Loss : <b>{trade['stop_loss']}</b>

🎯 Take Profit : <b>{trade['take_profit']}</b>

⚖ Risk Reward : <b>{trade['risk_reward']}</b>

⚡ Leverage : <b>{trade['leverage']}X</b>

━━━━━━━━━━━━━━━━━━
"""

        return self.send_message(message)


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    telegram = TelegramAlert()

    print(

        "Telegram Alert Final Loaded"

    )