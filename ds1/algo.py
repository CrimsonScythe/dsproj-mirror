
# 5 beers
# Ways to spend 5 DKK: 

#              |			   
# [1, 2, 2, 3, 5]
#        |  |
# [1, 2, 2, 3, 5]
#     |     |
# [1, 2, 2, 3, 5]
#  |  |  |
# [1, 2, 2, 3, 5]

# Total of 4 ways

p = [2, 3, 2, 1, 4]


def N(C, i):

	if C == 0:
		print("We used all our money up, great! Have a 1, will ya??")
		return 1

	elif i < 0:
		print("We're out of beers to buy!")
		return 0

	print("I currently have", C, "money and have the option of buying a beer with price", p[i])
	# Inverted if-statement.
	# No more beers, no more money to spend. 
	# Should be possible to combine them into one.

	if C == p[i]:
		print("Bought beer", i, "with price", p[i])
		return 1 + N(C, i-1)

	if p[i] <= C:
		print("Bought beer nr.", i, "with the cost ", p[i])
		return N(C-p[i], i-1)


	return 0

	"""
	elif p[i] != C: 
		print("didn't buy the beer")
		return 0 + N(C, i-1)
	"""

print(N(5, 4))



