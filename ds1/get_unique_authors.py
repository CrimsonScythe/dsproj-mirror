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

	authors_lists = []

	df = pd.read_csv("1mio-raw.csv", usecols=['authors'], low_memory=True)

	unique_authors_list = df['authors'].unique()

	num_of_authors = len(unique_authors_list)

	authors_dict = {}
	i = 0
	prog = 0
	for author in unique_authors_list:
		try: 
			authors_dict[author]
			i += 1
		except KeyError:
			authors_dict[author] = i
			i += 1
		
		print(prog / num_of_authors * 100, "%")
		prog += 1

	return authors_dict

