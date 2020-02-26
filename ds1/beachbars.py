

barPos = [0, 5, 13, 33, 36]

beerStock = [20, 40, 80, 10, 20]

def isPossible(bmax):

    numOfDrivers = 2
    beersPerKm = 1

    dist = 0
    cost = 0
    beersNeeded = 0
    for bar in range(len(barPos)):

        # Keeping track of, if we need to transfer beers backwards, how much would it cost us.
        cost += barPos[bar] * beersPerKm * numOfDrivers
        if beerStock[bar] < bmax:

            # Keeping track of how many beers the bars need, irregardless of which bar.
            beersNeeded += bmax - beerStock[bar]

        dist = barPos[bar]

        # this bar might possibly transfer beers to other bars in need! Possibly!
        if beerStock[bar] >= bmax:
            if beerStock[bar] - cost - beersNeeded >= bmax:
                beerStock[bar] -= cost - beersNeeded
                beerStock[bar-1]  
        

isPossible(21)