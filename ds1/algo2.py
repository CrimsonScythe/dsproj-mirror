# K = [[0 for x in range(W+1)] for x in range(n+1)]
# p = [2, 3, 2, 1, 4]
# C = 5

p = [2 ,2, 4, 3, 1]
C = 4
q=0
ways=0
n=5

# p = [5 ,5, 4, 5, 6]
# C = 4
# q=0
# ways=0
# n=5

def N(C, n, q, ways):

    for i in range(n):
        # reset q before considering every subproblem
        # if (C == p[i]):
            # ways += 1

        q=0
        for j in range(n):
            if j == i:
                # if (C == p[j]):
                    # ways += 1
                    # q = 0
                    # continue
                continue
            # jump over iteration if j reaches max of n
            if j >= n:
                continue



            # if (C == p[i]):
            #     ways += 1
            #     q = 0
            #     continue

            q = p[i] + p[j]
            # if excess money has been used, means the combination did not work, reset q and jump to next iteration
            if ((C - q) < 0):
                q = 0
                continue
            # if money has been used exactly, a successful combination has been found. reset q.
            if (C == q):
                ways += 1
                q = 0
        # When we are down  here, we are done with a subproblem of size i,
        # this is where values can be written to a table
    return ways

result = N(C, n, q, ways)
print(result)
