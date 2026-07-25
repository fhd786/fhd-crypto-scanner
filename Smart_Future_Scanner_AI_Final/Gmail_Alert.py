# =========================================================
# SMART FUTURE SCANNER AI
# GMAIL ALERT
# PART 1
# =========================================================

import smtplib

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart


# =========================================================
# GMAIL CONFIG
# =========================================================

class GmailAlert:

    def __init__(self):

        # بعد میں اپنا Gmail ڈالیں گے
        self.email = ""

        # بعد میں App Password ڈالیں گے
        self.password = ""

        self.smtp_server = "smtp.gmail.com"

        self.smtp_port = 587

        print("Gmail Alert Loaded")


    # -----------------------------------------------------
    # BUILD EMAIL
    # -----------------------------------------------------

    def build_email(

        self,

        subject,

        body

    ):

        msg = MIMEMultipart()

        msg["From"] = self.email

        msg["To"] = self.email

        msg["Subject"] = subject

        msg.attach(

            MIMEText(

                body,

                "plain"

            )

        )

        return msg


    # -----------------------------------------------------
    # SEND EMAIL
    # -----------------------------------------------------

    def send_email(

        self,

        subject,

        body

    ):

        if self.email == "":

            return False

        if self.password == "":

            return False

        try:

            server = smtplib.SMTP(

                self.smtp_server,

                self.smtp_port

            )

            server.starttls()

            server.login(

                self.email,

                self.password

            )

            message = self.build_email(

                subject,

                body

            )

            server.sendmail(

                self.email,

                self.email,

                message.as_string()

            )

            server.quit()

            return True

        except Exception:

            return False
            # =========================================================
# GMAIL ALERT
# PART 2
# FINAL TRADE ALERT
# =========================================================


    # -----------------------------------------------------
    # SEND TRADE ALERT
    # -----------------------------------------------------

    def send_trade_alert(

        self,

        trade

    ):

        if trade is None:

            return False


        subject = (

            "SMART FUTURE SCANNER AI SIGNAL"

        )


        body = f"""

==================================

SMART FUTURE SCANNER AI

==================================


SIGNAL      : {trade['signal']}

CONFIDENCE  : {trade['confidence']}

ENTRY       : {trade['entry']}

STOP LOSS   : {trade['stop_loss']}

TAKE PROFIT : {trade['take_profit']}

RISK REWARD : {trade['risk_reward']}

LEVERAGE    : {trade['leverage']}X


TIME:

{trade.get('time','')}


==================================

"""


        return self.send_email(

            subject,

            body

        )


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    gmail = GmailAlert()

    print(

        "Gmail Alert Final Loaded"

    )