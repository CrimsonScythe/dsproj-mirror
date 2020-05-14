"""
Queries N articles from each type in the database
and saves it to a csv file.

Future features: Randomize which N articles are chosen of each type?

INPUT : NONE
OUTPUT : CSV FILE (OR DATAFRAME?)
"""

import psycopg2
import pandas as pd

class LimitDataSet():

	def createDataFrame(n_of_each_type):

		# # # ESTABLISH DB CONN. # # #
		conn1 = psycopg2.connect(
			host = "localhost",
			 dbname="postgres",
			  user="postgres",
			   password="root")
		cur1 = conn1.cursor() 
		# # # # # # # # # # # # # # # # # # #


		# # # PREPARE DATAFRAME TO BE APPENDED TO # # #

		col_names = ['content', 'type_id']
		df = pd.DataFrame(columns = col_names)
		# # # # # # # # # # # # # # # # # # # # # # # #



		cur1.execute('SELECT * FROM fakenewscorp.article_type')
		is_type_table = cur1.fetchall()

		get_articles_query = (
		"""
		SELECT content, type_id FROM fakenewscorp.article
		INNER JOIN fakenewscorp.is_type
		ON article.article_id = is_type.article_id
		WHERE type_id = {}
		LIMIT {}
		""")

		cur_index = 0
		for tp in is_type_table:
			cur1.execute(get_articles_query.format(tp[0], n_of_each_type))
			# result is on form [('content', type_id), ('content', type_id), ..., ()]
			# list of tuples. each tuple is an article. 
			result = cur1.fetchall()
			size = len(result)
			for i in range(size):
				df.loc[cur_index + i] = [result[i][0], result[i][1]]
				cur_index += size

		return df


		def ToCSV(n_of_each_type = 1000):
			df = createDataFrame(n_of_each_type)
			df.to_csv("DataSet{}".format(n_of_each_type), headers=False)

		def ToDataFrame(n_of_each_type = 1000):
			return createDataFrame(n_of_each_type)











