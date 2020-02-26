import numpy
import big_o

p = [2, 3, 7, 2, 8, 9, 1, 10]
# = [1, 2, 2, 3, 7, 8, 9, 10]

def N(C, i):
	if C == 0:
		return 1

	# Assumptions:
	# - We ran out of items.
	# - We didn't succed at using all money, 
	#   otherwise if statement above would catch.
	elif i < 0:
		return 0

	return N(C-p[i], i-1) + N(C, i-1)

print("Recursive formula:")
print(N(10, len(p)-1))
# returns 7

def DP(C, p):
    mem = numpy.zeros((len(p), C))
    if mem.size > 0:
        for beer in range(len(p)):
            for coin in range(C):
                # +1 for offsetting 0-index.
                if p[beer] == coin + 1:
                    mem[beer, coin] = mem[beer-1, coin] + 1

                elif coin+1 > p[beer]:
                    mem[beer, coin] = mem[beer-1, coin - p[beer]] + mem[beer-1, coin]

                elif coin+1 < p[beer]:
                    mem[beer, coin] = mem[beer-1, coin]
        return mem[-1, -1]

print("Memoization:")
DP(10, p)


def DPAux(list_of_integers):
    for i, integer in enumerate(list_of_integers):
        DP(integer, p)


positive_int_generator = lambda n: big_o.datagen.integers(n, 0, 10)
best, others = big_o.big_o(DPAux, positive_int_generator, n_repeats=1)
print(best)
