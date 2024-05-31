import os
import pandas as pd
from py_alpaca_api.alpaca import PyAlpacaApi

from .src.openai import OpenAIAPI
from .src.yahoo import Yahoo
from .src.global_fuctions import send_message

from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator

from tqdm import tqdm
from dotenv import load_dotenv
from datetime import datetime
from datetime import timedelta
from pytz import timezone

tz = timezone("US/Eastern")
ctime = datetime.now(tz)
today = ctime.strftime("%Y-%m-%d")
previous_day = (ctime - timedelta(days=1)).strftime("%Y-%m-%d")
year_ago = (ctime - timedelta(days=365)).strftime("%Y-%m-%d")

load_dotenv()

api_key = str(os.getenv("API_KEY"))
api_secret = str(os.getenv("API_SECRET"))
api_paper = True if os.getenv("API_PAPER") == "True" else False


class DailyLosers:
    def __init__(self):
        """
        This code initializes an instance of the PyAlpacaApi class with the provided API key and API secret.
        It sets the api_paper parameter to True, indicating that the API should be used in a paper trading environment.

        The value of the production variable is derived from the environment variable "PRODUCTION".
        If the value of "PRODUCTION" is "True", the production variable is set to True.
        Otherwise, it is set to False.

        This code is used to configure and set up the PyAlpacaApi for interacting with the Alpaca API in a Python
        application.
        """
        self.alpaca = PyAlpacaApi(
            api_key=api_key, api_secret=api_secret, api_paper=True
        )
        self.production = True if os.getenv("PRODUCTION") == "True" else False

    def run(self):
        """
        Executes the main logic of the program.

        This method performs the following steps:
        1. Sells the positions based on the sell criteria.
        2. Liquidates the positions to make cash 10% of the portfolio.
        3. Checks for buy opportunities.
        """

        self.sell_positions_from_criteria()
        self.liquidate_positions_for_capital()
        self.check_for_buy_opportunities()

    ########################################################
    # Define the sell_positions_from_criteria method
    ########################################################
    def sell_positions_from_criteria(self):
        """
        Sell Positions from Criteria

        This method is used to sell positions based on sell criteria. It retrieves sell opportunities, current
        positions, and then iterates through the sell opportunities to sell the stocks.

        Parameters:
            - None

        Returns:
            - None

        """
        print("Selling positions based on sell criteria")

        sell_opportunities = self.get_sell_opportunities()
        if not sell_opportunities:
            send_message("No sell opportunities found.")
            return

        current_positions = self.alpaca.position.get_all()
        sold_positions = []

        for symbol in sell_opportunities:
            try:
                qty = current_positions[current_positions["symbol"] == symbol][
                    "qty"
                ].values[0]

                self.alpaca.position.close(symbol_or_id=symbol, percentage=100)
            except Exception as e:
                send_message(f"Error selling {symbol}: {e}")
                continue
            else:
                sold_positions.append({"symbol": symbol, "qty": qty})

        self._send_position_messages(sold_positions, "sell")

    ########################################################
    # Define the get_sell_opportunities method
    ########################################################
    def get_sell_opportunities(self) -> list:
        """
        Retrieves a list of symbols representing potential sell opportunities based on specified criteria.

        Returns:
            sell_list (list): A list of symbols representing potential sell opportunities.
        """
        current_positions = self.alpaca.position.get_all()
        if current_positions[current_positions["symbol"] != "Cash"].empty:
            return []

        current_positions_symbols = current_positions[
            current_positions["symbol"] != "Cash"
        ]["symbol"].tolist()

        assets_history = self.get_ticker_data(current_positions_symbols)

        sell_criteria = (
            (assets_history[["rsi14", "rsi30", "rsi50", "rsi200"]] >= 70).any(
                axis=1
            )
        ) | (
            (
                assets_history[["bbhi14", "bbhi30", "bbhi50", "bbhi200"]] == 1
            ).any(axis=1)
        )

        sell_filtered_df = assets_history[sell_criteria]
        sell_list = sell_filtered_df["symbol"].tolist()

        percentage_change_list = current_positions[
            current_positions["profit_pct"] > 0.1
        ]["symbol"].tolist()

        for symbol in percentage_change_list:
            if symbol not in sell_list:
                sell_list.append(symbol)

        return sell_list

    ########################################################
    # Define the liquidate_positions_for_capital method
    ########################################################
    def liquidate_positions_for_capital(self):
        """
        Liquidates positions to ensure cash is 10% of the portfolio.

        This method calculates the current cash available and compares it to the total holdings in the portfolio.
        If the cash is less than 10% of the total holdings, it sells the top 25% performing stocks to make cash
        10% of the portfolio.

        Returns:
            None
        """
        print("Liquidating positions to make Cash 10% of the portfolio...")

        current_positions = self.alpaca.position.get_all()
        if current_positions[current_positions["symbol"] != "Cash"].empty:
            send_message("No positions available to liquidate for capital")
            return

        cash_row = current_positions[current_positions["symbol"] == "Cash"]

        total_holdings = current_positions["market_value"].sum()
        sold_positions = []

        if cash_row["market_value"][0] / total_holdings < 0.1:
            current_positions = current_positions[
                current_positions["symbol"] != "Cash"
            ].sort_values(by="profit_pct", ascending=False)

            top_performers = current_positions.iloc[
                : int(len(current_positions) // 2)
            ]
            top_performers_market_value = top_performers["market_value"].sum()
            cash_needed = (
                total_holdings * 0.1 - cash_row["market_value"][0]
            ) + 5.00

            for index, row in top_performers.iterrows():
                print(
                    f"Selling {row['symbol']} to make cash 10% portfolio cash requirement"
                )
                amount_to_sell = int(
                    (row["market_value"] / top_performers_market_value)
                    * cash_needed
                )
                if amount_to_sell == 0:
                    continue
                try:
                    self.alpaca.order.market(
                        symbol=row["symbol"],
                        notional=amount_to_sell,
                        side="sell",
                    )
                except Exception as e:
                    send_message(f"Error selling {row['symbol']}: {e}")
                    continue
                else:
                    sold_positions.append(
                        {
                            "symbol": row["symbol"],
                            "notional": round(amount_to_sell, 2),
                        }
                    )

        self._send_position_messages(sold_positions, "liquidate")

    ########################################################
    # Define the check_for_buy_opportunities method
    ########################################################
    def check_for_buy_opportunities(self):
        """
        The following code is a method definition that checks for buy opportunities. It performs the following steps:

        1. Calls the `get_daily_losers()` method to get the list of tickers that have performed poorly on a given day.
        2. Calls the `get_ticker_data(losers)` method, passing in the list of losers, to get detailed data for each
        ticker.
        3. Applies buy criteria to the ticker data by calling the `buy_criteria(ticker_data)` method, which returns a
        filtered list of tickers that meet the buy criteria.
        4. Filters the list of tickers with news by calling the `filter_tickers_with_news(filter_tickers)` method.
        5. Opens positions for the filtered tickers by calling the `open_positions()` method.

        This method assumes that the necessary data and methods required for each step are available within the current
        class or its dependencies.

        """
        losers = self.get_daily_losers()
        tickers = self.filter_tickers_with_news(losers)

        if len(tickers) > 0:
            print(
                f"{len(tickers)} buy opportunities found. Opening positions..."
            )
            self.open_positions(tickers=tickers)
        else:
            print("No buy opportunities found")

    ########################################################
    # Define the open_positions method
    ########################################################
    def open_positions(self, tickers: list, ticker_limit=8):
        """
        Opens buying orders based on buy opportunities and openai sentiment.

        Args:
            tickers (list): A list of tickers to buy.
            ticker_limit (int, optional): The maximum number of tickers to buy. Defaults to 8.

        Returns:
            None
        """
        print(
            "Buying orders based on buy opportunities and openai sentiment. Limit to 8 stocks by default"
        )

        available_cash = self.alpaca.account.get().cash

        if len(tickers) == 0:
            send_message("No tickers to buy.")
            return
        else:
            notional = (available_cash / len(tickers[:ticker_limit])) - 1

        bought_positions = []

        for ticker in tickers[:ticker_limit]:
            try:
                self.alpaca.order.market(symbol=ticker, notional=notional)
            except Exception as e:
                send_message(f"Error buying {ticker}: {e}")
                continue
            else:
                bought_positions.append(
                    {"symbol": ticker, "notional": round(notional, 2)}
                )

        self._send_position_messages(bought_positions, "buy")

    ########################################################
    # Define the update_or_create_watchlist method
    ########################################################
    def update_or_create_watchlist(self, name, symbols):
        """
        Updates or creates a watchlist with the given name and symbols.

        Parameters:
        - name (str): The name of the watchlist.
        - symbols (list): A list of symbols to include in the watchlist.

        Returns:
        None

        Raises:
        ValueError: If an error occurs while updating the watchlist, a new watchlist will be created instead.
        """
        try:
            self.alpaca.watchlist.update(watchlist_name=name, symbols=symbols)
        except Exception:
            self.alpaca.watchlist.create(name=name, symbols=symbols)

    ########################################################
    # Define the filter_tickers_with_news method
    ########################################################
    def filter_tickers_with_news(self, tickers) -> list:
        """
        Filters tickers based on the presence of news articles using OpenAI and Yahoo Finance APIs.

        :param tickers: A list of tickers to filter.
        :return: A list of tickers that have been filtered through OpenAI and Yahoo Finance.
        """
        yahoo = Yahoo()
        openai = OpenAIAPI()
        filtered_tickers = []

        for i, ticker in tqdm(
            enumerate(tickers),
            desc=f"• Analyzing news for {len(tickers)} tickers, using OpenAI & Yahoo Finance: ",
        ):
            articles = yahoo.get_articles(ticker)

            if len(articles) > 0:
                bullish = 0
                bearish = 0
                for art in articles[:3]:
                    sentiment = openai.get_sentiment_analysis(
                        title=art["title"],
                        symbol=art["symbol"],
                        article=art["content"],
                    )
                    if sentiment == "BULLISH":
                        bullish += 1
                    else:
                        bearish += 1

                if bullish > bearish:
                    filtered_tickers.append(ticker)

        if len(filtered_tickers) == 0:
            print("No tickers with news found")
            return []

        self.update_or_create_watchlist(
            name="DailyLosers", symbols=filtered_tickers
        )

        return self.alpaca.watchlist.get_assets(watchlist_name="DailyLosers")

    ########################################################
    # Define the get_daily_losers method
    ########################################################
    def get_daily_losers(self) -> list:
        """
        This function is used to retrieve a list of daily losers from the stock market. It uses the Alpaca API to get a
        list of loser symbols and performs some criteria checks on them before returning the final list of symbols.

        Parameters:
        - None

        Returns:
        - A list of stock symbols representing the daily losers.

        Note:
        - This function relies on the 'Yahoo' class and its associated methods.
        - This function depends on the 'get_ticker_data()', 'buy_criteria()', 'send_message()', 'get_sentiment()',
        'update_or_create_watchlist()', and 'get_assets()' methods from other parts of the code.
        - The 'send_message()' function is responsible for sending a message/notification.
        - The 'tqdm' library is used to display a progress bar while processing the symbols.
        """
        yahoo = Yahoo()
        losers = self.alpaca.screener.losers(total_losers_returned=130)[
            "symbol"
        ].to_list()

        losers = self.get_ticker_data(losers)
        losers = self.buy_criteria(losers)

        if len(losers) == 0:
            send_message("No daily losers found.")
            return []

        for i, ticker in tqdm(
            enumerate(losers),
            desc=f"• Getting recommendations for {len(losers)} tickers, from Yahoo Finance: ",
        ):
            sentiment = yahoo.get_sentiment(ticker)
            if sentiment == "NEUTRAL" or sentiment == "BEARISH":
                losers.remove(ticker)

        self.update_or_create_watchlist(name="DailyLosers", symbols=losers)

        return self.alpaca.watchlist.get_assets(watchlist_name="DailyLosers")

    ########################################################
    # Define the buy_criteria method
    ########################################################
    def buy_criteria(self, data: pd.DataFrame) -> list:
        """
        This function is used to filter and select specific stock tickers based on certain criteria.
        The filtered tickers are then added to a watchlist and returned.

        Parameters:
        - self: Instance of the class containing this method.
        - data: Pandas DataFrame containing stock data.

        Returns:
        - A list of stock assets that meet the buy criteria.

        Example Usage:
        buy_criteria(data)

        """

        buy_criteria = (
            (data[["bblo14", "bblo30", "bblo50", "bblo200"]] == 1).any(axis=1)
        ) | ((data[["rsi14", "rsi30", "rsi50", "rsi200"]] <= 30).any(axis=1))

        buy_filtered_data = data[buy_criteria]

        filtered_data = list(buy_filtered_data["symbol"])

        if len(filtered_data) == 0:
            print("No tickers meet the buy criteria")
            return []

        self.update_or_create_watchlist(
            name="DailyLosers", symbols=filtered_data
        )

        return self.alpaca.watchlist.get_assets(watchlist_name="DailyLosers")

    ########################################################
    # Define the get_ticker_data method
    ########################################################
    def get_ticker_data(self, tickers) -> pd.DataFrame:
        """
        Retrieves technical data for the given list of tickers using the Alpaca API.

        Args:
            tickers (list): List of ticker symbols.

        Returns:
            pd.DataFrame: DataFrame containing technical data for the tickers.

        """
        df_tech = []

        for i, ticker in tqdm(
            enumerate(tickers),
            desc="• Analyzing ticker data for "
            + str(len(tickers))
            + " symbols from Alpaca API",
        ):
            try:
                history = self.alpaca.history.get_stock_data(
                    symbol=ticker, start=year_ago, end=previous_day
                )
            except ValueError:
                continue

            try:
                for n in [14, 30, 50, 200]:
                    history["rsi" + str(n)] = RSIIndicator(
                        close=history["close"], window=n
                    ).rsi()
                    history["bbhi" + str(n)] = BollingerBands(
                        close=history["close"], window=n, window_dev=2
                    ).bollinger_hband_indicator()
                    history["bblo" + str(n)] = BollingerBands(
                        close=history["close"], window=n, window_dev=2
                    ).bollinger_lband_indicator()
                df_tech_temp = history.tail(1)
                df_tech.append(df_tech_temp)
            except KeyError:
                pass

        if df_tech:
            df_tech = [x for x in df_tech if not x.empty]
            df_tech = pd.concat(df_tech)
        else:
            df_tech = pd.DataFrame()

        return df_tech

    ########################################################
    # Define the _send_position_messages method
    ########################################################
    def _send_position_messages(self, positions: list, pos_type: str):
        """
        Sends position messages based on the type of position.
        Args:
            positions (list): List of position dictionaries.
            pos_type (str): Type of position ("buy", "sell", or "liquidate").
        Returns:
            bool: True if message was sent successfully, False otherwise.
        """
        position_names = {
            "sell": "sold",
            "buy": "bought",
            "liquidate": "liquidated",
        }

        try:
            position_name = position_names[pos_type]
        except KeyError:
            raise ValueError(
                'Invalid type. Must be "sell", "buy", or "liquidate".'
            )

        if not positions:
            position_message = f"No positions to {pos_type}"
        else:
            is_market_open = (
                "" if self.alpaca.market.clock().is_open else " pretend"
            )
            position_message = f"Successfully{is_market_open} {position_name} the following positions:\n"

            for position in positions:

                if position_name == "liquidated":
                    qty_key = "notional"
                elif position_name == "sold":
                    qty_key = "qty"
                else:
                    qty_key = "notional"

                qty = position[qty_key]
                symbol = position["symbol"]

                position_message += f"{qty} shares of {symbol}\n"
        return send_message(position_message)
