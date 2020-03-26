import pandas as pd
import numpy as np
from cleantext import clean
from datetime import datetime
import datefinder
import re
import psycopg2
import time
import math
from io import StringIO

def get_authors_dict():

	authors_list = []
	chunksize = 2000

	df_reader = pd.read_csv("1mio-raw.csv", chunksize=chunksize, usecols=['authors'], low_memory=True)

	i = 0
	for df in df_reader:
		authors_list.append(df['authors'].to_list())

		print(i * chunksize / 1000000 * 100)
		i += 1


	authors_list_unique = []

	for author in authors_list:
		if author not in authors_list_unique:
			authors_list_unique.append(author)

	i = 0
	author_dict = {}

	for author in authors_list_unique:
		if not author_dict[author]:
			author_dict[author] = i
			i += 1

	print(author_dict['Sean Martin'])


get_authors_dict()


