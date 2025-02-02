from data_fetcher import DataFetcher
from data_transformer import DataTransformer 
import pandas as pd
from datetime import date
import datetime
from loadToMysql import LoadToMysql
from aws_rds_loader import AWSRdsLoader
import os

stock_data = pd.DataFrame()
"""
This code was to test data fetching and loading it to the database

dataFetcher = DataFetcher(["AAPL", "MSFT", "NVDA"], "2024-01-01", date.today())
stock_data = dataFetcher.fetch_data()
dataTransformer = DataTransformer(stock_data)
transformed_stok_data = dataTransformer.add_moving_average(window = 20, column = "close")
transformed_stok_data = dataTransformer.add_moving_average(window = 50, column = "close")
transformed_stok_data = transformed_stok_data.round(2)
ct = datetime.datetime.now()
transformed_stok_data.to_csv(f"csvFiles/transformed_data_{ct.year}{ct.month}{ct.day}{ct.hour}{ct.minute}{ct.second}.csv", index = False)

aws_loader = AWSRdsLoader(
	os.getenv("AWS_DB_HOST"),
	os.getenv("AWS_DB_USER"),
	os.getenv("AWS_DB_PASSWORD"),
	os.getenv("AWS_DB_PORT"),
	os.getenv("AWS_DB_NAME"))

aws_loader.load_to_table(transformed_stok_data, "moving_average_daywise")
"""

dataFetcher = DataFetcher(["AAPL"], "2000-01-01", date.today())
stock_data = dataFetcher.fetch_data()
dataTransformer = DataTransformer(stock_data)

transformed_data = dataTransformer.add_moving_average(window = 10)
transformed_data = dataTransformer.add_moving_average(window = 30)
transformed_data = dataTransformer.add_moving_average(window = 50)

transformed_data = dataTransformer.add_exponential_moving_average(window = 10)
transformed_data = dataTransformer.add_exponential_moving_average(window = 15)
transformed_data = dataTransformer.add_exponential_moving_average(window = 30)

transformed_data = dataTransformer.add_rsi()
transformed_data = dataTransformer.add_percantage_change()
transformed_data = dataTransformer.add_macd()
transformed_data = dataTransformer.add_macd_signal_line()
transformed_data = dataTransformer.add_obv()
transformed_data = dataTransformer.add_standard_deviation()
transformed_data = dataTransformer.add_day_range()
transformed_data = dataTransformer.add_day_range_percetange()
transformed_data = dataTransformer.add_abs_open_close_percentage()


transformed_data = transformed_data.round(2)
ct = datetime.datetime.now()
transformed_data.to_csv(f"csvFiles/transformed_data_{ct.year}{ct.month}{ct.day}{ct.hour}{ct.minute}{ct.second}.csv", index = False)






