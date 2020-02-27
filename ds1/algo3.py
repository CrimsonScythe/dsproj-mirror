

# K = [[0 for x in range(W+1)] for x in range(n+1)]
# p = [2, 3, 2, 1, 4]
# C = 5


p = [2 ,2, 4, 3, 1]
C = 4
q=0
ways=0
n=5
K = [[0 for x in range(C+1)] for x in range(n+1)]
def N(C, n, q, ways, K):

    for i in range(n):
        # reset q before considering every subproblem
        q=0
        for j in range(C):
            # jump over iteration if j reaches max of n
            if j >= n:
                continue
            # if j == i:
                # continue
            # if K[i][j] > 0:
                # print("WW")
                # q = K[i][j]
                # ways += 1
                # continue
            q = p[i] + p[j]
            # if excess money has been used, means the combination did not work, reset q and jump to next iteration
            if ((C - q) < 0):
                q = 0
                continue
            # if money has been used exactly, a successful combination has been found. reset q.
            if (C == q):
                ways += 1
                q = 0
        K[i][j] = ways
        # When we are down  here, we are done with a subproblem of size i,
        # this is where values can be written to a table
    return ways

result = N(C, n, q, ways, K)
print(result)
