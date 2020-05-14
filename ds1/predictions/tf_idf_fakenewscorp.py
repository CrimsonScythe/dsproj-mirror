import numpy as np
import pandas as pd
import re
import math

def get_tokens(string):
	"""
	Source: https://github.com/gearmonkey/tfidf-python/blob/master/tfidf.py
	Break a string into tokens, preserving URL tags as an entire token.
	This implementation does not preserve case.  
	Clients may wish to override this behavior with their own tokenization.
	"""

	assert type(string) == type("") or math.isnan(string), "AssertionError. Function input: {}".format(string)

	if not type(string):
		if math.isnan(string):
			return

	try:
		return re.findall(r"<a.*?/a>|<[^\>]*>|[\w'@#]+", string)
	except Exception as e:
		print(e)
		print(string)



CHUNKSIZE = 2000

# yolo.csv doesn't have headers, so we must accses the content column by index (usecols=[2])
df_reader = pd.read_csv(
	"../fakenewscorp/yolo.csv",
	chunksize=CHUNKSIZE,
	header=None,
	usecols=[2],
	low_memory=True
)

	

i = 0
for df in df_reader:
	content_field = df.to_numpy()
	for content in content_field:
		if type(content[0]) != type(""):
			break
		
		token_count_dict = {}
		tokens = get_tokens(content[0])

		for token in tokens:
			try:
				token_count_dict[token] = token_count_dict[token] + 1
			except KeyError as e:
				token_count_dict[token] = 1
	if i % 5 == 0:	
		print(i * CHUNKSIZE / 1000000 * 100, "%")
	i += 1			

	








