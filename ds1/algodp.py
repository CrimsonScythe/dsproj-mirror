
# 5 beers
# Ways to spend 5 DKK:

# p = [2, 3, 2, 1, 4]
# p = [5 ,5, 4, 5, 6]
# C = 4
# q=0
# ways=0
# n=5
# s=0
#
p = [2 ,2, 4, 3, 1]
C = 4

q=0
s=0

def N(C, i, q):

    if (C == 0):
        # q = 0
        return 1

    elif i < 0:
        # q = 0
        return 0

    elif(C < 0):
        # q = 0
        return 0

    for i in range(len(p)-1, -1, -1):
        q = q + N(C - p[i], i-1, q)
        # q = q + N(C-p[i], i-1, q) + N(C, i-1, q)

    return q
	# return N(C-p[i], i-1) + N(C, i-1)

print(N(C, len(p) - 1, q))

# def N(C, i, q):
#
#     if (C == 0):
#         return 1
#
#     elif i < 0:
#         return 0
#
#     for i in range(len(p)-1, -1, -1):
#         q = q + N(C-p[i], i-1, q) + N(C, i-1, q)
#
#     return q
# 	# return N(C-p[i], i-1) + N(C, i-1)
#
# print(N(C, len(p) - 1, q))
