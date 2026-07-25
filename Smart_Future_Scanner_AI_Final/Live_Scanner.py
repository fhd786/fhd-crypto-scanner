# =========================================================
# SMART FUTURE SCANNER AI
# LIVE SCANNER
# PART 1
# =========================================================

import time

from datetime import datetime


# =========================================================
# LIVE SCANNER
# =========================================================

class LiveScanner:

    def __init__(self):

        print(
            "Live Scanner Loaded"
        )


    # -----------------------------------------------------
    # SCAN START
    # -----------------------------------------------------

    def start_scan(self):

        print(
            "Scanner Started"
        )

        while True:

            print(
                "Scanning Market...",
                datetime.now()
            )

            time.sleep(300)
            # =========================================================
# LIVE SCANNER
# PART 2
# MARKET DATA CONNECTION
# =========================================================


    # -----------------------------------------------------
    # LOAD MARKET
    # -----------------------------------------------------

    def load_market_data(
        self,
        connector
    ):

        try:

            data = connector.get_gainers()

            return data

        except Exception:

            return []


    # -----------------------------------------------------
    # ANALYZE COINS
    # -----------------------------------------------------

    def analyze_coins(
        self,
        coins,
        indicator_engine,
        signal_engine
    ):

        signals = []


        for coin in coins:

            try:

                indicators = indicator_engine.calculate(

                    coin

                )


                signal = signal_engine.execute(

                    indicators,

                    coin["price"]

                )


                if signal:

                    signals.append(

                        signal

                    )


            except Exception:

                continue


        return signals
        # =========================================================
# LIVE SCANNER
# PART 3
# ALERT INTEGRATION
# =========================================================


    # -----------------------------------------------------
    # SEND SIGNAL ALERTS
    # -----------------------------------------------------

    def send_alerts(

        self,

        signals,

        alert_system,

        telegram,

        gmail

    ):

        if not signals:

            return


        for signal in signals:


            try:

                alert = alert_system.create_alert(

                    signal

                )


                if alert_system.validate_alert(

                    alert

                ):


                    message = alert_system.build_message(

                        alert

                    )


                    telegram.send_trade_alert(

                        signal

                    )


                    gmail.send_trade_alert(

                        signal

                    )


                    print(

                        message

                    )


            except Exception:

                continue
                # =========================================================
# LIVE SCANNER
# PART 4
# MAIN SCANNER LOOP
# =========================================================


    # -----------------------------------------------------
    # RUN SCANNER
    # -----------------------------------------------------

    def run(

        self,

        connector,

        indicator_engine,

        signal_engine,

        alert_system,

        telegram,

        gmail

    ):


        print(

            "Live Scanner Started"

        )


        while True:


            try:

                # Market Data

                coins = self.load_market_data(

                    connector

                )


                # Analysis

                signals = self.analyze_coins(

                    coins,

                    indicator_engine,

                    signal_engine

                )


                # Alerts

                self.send_alerts(

                    signals,

                    alert_system,

                    telegram,

                    gmail

                )


                print(

                    "Scan Completed"

                )


                time.sleep(300)


            except Exception as e:


                print(

                    "Scanner Error:",

                    e

                )


                time.sleep(60)
                # =========================================================
# LIVE SCANNER
# PART 5
# FINAL STARTUP TEST
# =========================================================


    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    def status(self):

        return {

            "scanner":

            "ACTIVE",

            "time":

            datetime.now(),

            "message":

            "Live Scanner Running"

        }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    scanner = LiveScanner()

    print(

        scanner.status()

    )