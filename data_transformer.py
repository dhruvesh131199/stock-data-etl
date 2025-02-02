class DataTransformer:

	def __init__(self, data):

		"""
		Pass the dataframe after fetching the data from DataFetcher class to add transformations to the dataframe

		"""
		self.data = data

	def add_moving_average(self, window = 1, column = "close"):
		"""
		This function will add the moving average of passed arguments window and column price.
		default window is set to 1 and column is set to close.
		we group by the symbol and find the column price, then use transform function to keep the format same
		of the original dataframe.
		the lambda function will get the close price of the symbol as x, rolling function will get the last 20 rows
		and find the mean of it to add the value to the newly added column.

		"""


		self.data[f"{column}_MA{window}"] = self.data.groupby("symbol")[column].transform(
			lambda x: x.rolling(window=window).mean())
		print(f"Moving average of {window} of the {column} price is added")
		return self.data

	def add_exponential_moving_average(self, window = 1, column = "close"):

		"""
		-Exponential moving average is by multiplying weighted_multiplier(k) to the current day price
		and multiplying (1-k) to the Simple 
		"""
		self.data[f"{column}_EMA{window}"] = self.data.groupby("symbol")[column].ewm(span = window, adjust = False).mean().reset_index(level=0, drop=True)

		print(f"Exponential moving average of {window} of the {column} price is added")
		return self.data

	def add_percantage_change(self):

		"""
		This function will add a new column to the database, percentage change from the previous day 
		"""
		self.data["change"] = (self.data["close"].diff()/self.data["close"].shift(1)) * 100

		print("Price percentage change is added")
		return self.data

	def add_rsi(self, window = 14, column = "close"):

		"""
		To calculate RSI, a few columns will be created for the better flow and understading of
		the calculation. Once we have the RSI column, all the temporary models will be deleted
		since they are no longer needed.
		default window is 14
		"""

		self.data["abs_change"] = self.data["close"].diff()

		self.data["gain"] = self.data["abs_change"].apply(lambda x: x if x>0 else 0)
		self.data["loss"] = abs(self.data["abs_change"].apply(lambda x: x if x<0 else 0))
		self.data["avg_gain"] = self.data["gain"].rolling(window = window).mean()
		self.data["avg_loss"] = self.data["loss"].rolling(window = window).mean()
		self.data["rs"] = self.data["avg_gain"]/self.data["avg_loss"]
		self.data["rsi"] = 100 - (100 / (1 + self.data['rs']))

		self.data.drop(columns = ["abs_change", "gain", "loss", "avg_gain", "avg_loss", "rs"], inplace = True)

		print(f"RSI is successfully added with window {window}")

		return self.data
		
	def add_macd(self, column = "close"):

		"""
		This function will add Moving average convergence/divergence by subtracting
		26 day EMA from 12 day EMA
		"""

		self.data = self.add_exponential_moving_average(window = 12, column = "close")
		self.data = self.add_exponential_moving_average(window = 26, column = "close")
		self.data["macd"] = self.data["close_EMA12"] - self.data["close_EMA26"]
		self.data.drop(columns = ["close_EMA12", "close_EMA26"], inplace = True)

		print("MACD is successfully added")
		return self.data

	def add_macd_signal_line(self):

		"""
		Signal line used for macd is simply the 9 day exponential moving average of macd.
		therefore, we can use the existing funciton add_exponential_moving_average to derive the signal line
		"""

		self.data = self.add_exponential_moving_average(window = 9, column = "macd")
		self.data.rename(columns = {"macd_EMA9" : "macd_signal_line"}, inplace = True)

		print("MACD signal line is added")
		return self.data

	def add_obv(self):

		self.data["obv"] = self.data["volume"]

		for i in range(1, len(self.data)):
			if self.data.loc[i, "close"] > self.data.loc[i-1, "close"]:
				self.data.loc[i, "obv"] = self.data.loc[i-1, "obv"] + self.data.loc[i, "volume"]
			elif self.data.loc[i, "close"] < self.data.loc[i-1, "close"]:
				self.data.loc[i, "obv"] = self.data.loc[i-1, "obv"] - self.data.loc[i, "volume"]
			else:
				self.data.loc[i, "obv"] = self.data.loc[i-1, "obv"]

		print("On balance value is added")
		return self.data


	def add_standard_deviation(self, window = 20, column = "close"):

		"""
		This will add the standard deviation of the last 20 days(default) of any column(default close)
		"""

		self.data[f"{column}_std{window}"] = self.data[column].rolling(window = window).std()
		print(f"Standard deviation of last {window} days is added for {column} price")
		return self.data

	def add_day_range(self):

		"""
		This will calculate the difference between high and low, to calculate how much stock fluctuated in the day
		"""

		self.data["days_range"] = self.data["high"] - self.data["low"]
		print("Day's range is added")
		return self.data

	def add_day_range_percetange(self):

		"""
		This will add pecentage movement in a day wrt to low of the day
		"""

		self.data["days_range_percetange"] = (self.data["high"] - self.data["low"]) * 100 / self.data["low"]
		print("Day's range percentage is added")
		return self.data

	def add_abs_open_close_percentage(self):
		"""
		This will calculate absolute perctange change from open to close
		"""

		self.data["abs_open_to_close_change_perc"] = abs((self.data["open"] - self.data["close"])*100/self.data["open"])
		print("Absolute percentage change from open to close is added")
		return self.data









