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

	# import data
	df = pd.read_csv("1mio-raw.csv", usecols=['authors'], low_memory=True)

	# get unique author strings from dataframe
	# these are not tokenized and if several authors have 
	# authored an article, they will appear as one here.
	unique_authors_list = df['authors'].unique()

	# we wanna tokenize the authors, so several authors having
	# authored the same article, appear as one author.  
	unique_authors_list_tokenized = []

	for authors in unique_authors_list:
		# make all strings lowercase, split on comma
		if not pd.isna(authors):
			author_list = (authors.lower()).split(",")

			for author in author_list:
				unique_authors_list_tokenized.append(author)


	num_of_authors = len(unique_authors_list_tokenized)

	# make dict to hold mapping between an author and pkey
	authors_dict = {}
	i = 0
	prog = 0
	for author in unique_authors_list_tokenized:
		try:
			# check if author is already added to dict. 
			authors_dict[author]
		except KeyError:
			# at KeyError, author is not added yet. Add and
			# increase pkey / key / i. 
			authors_dict[author] = i
			i += 1
		
		print("Creating author dict:", prog / num_of_authors * 100, "%")
		prog += 1

	return authors_dict

