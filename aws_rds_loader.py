from sqlalchemy import create_engine, text

class AWSRdsLoader:

	def __init__(self, host, user, password, port, database):

		"""
	    This class will load the data to the aws rds mysql database
	    A user must pass the hostname, username, passowrd, port and database to build a connection

	    """
		self.engine = self.buildconnection(host, user, password, port, database)
		print("Connection is built successfully")


	def buildconnection(self, host, user, password, port, database):

		"""
		This will return a connection to the __init__ function
		"""
		return create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}")


	def load_to_aws_rds(self, data, table):

		"""
		This function will load the data to the aws rds mysql table. The user need to pass dataframe
		and the table name from the database.
		"""
		data.to_sql(
			name = table,
			con = self.engine,
			if_exists = "replace",
			index = False)

		print(f"Successfully added the data to the {table}")

	def run_query(self, query):

		try:
			with self.engine.connect() as connection:
				connection.execute(text(query))
				print("The query is succesfully executed")
		except Exception as e:
			print(f"error occured: {e}")


	def load_to_table(self, data, table_name):

		"""
		This method is used to load datafram to the table
		"""
		data.to_sql(
			name = table_name,
			con = self.engine,
			if_exists = "replace",
			index = False)

		print(f"Successfully added the data to the {table_name}")






