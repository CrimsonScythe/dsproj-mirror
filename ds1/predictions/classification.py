import pandas as pd
import numpy as np
import csv

df_chunk = pd.read_csv("..yolo.csv", chunksize=2000, usecols = ['content', 'type'], nrows=10000)
