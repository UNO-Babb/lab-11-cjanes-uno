#GroceryStoreSim.py
#Name: Colton Janes
#Date: 04/27/2025
#Assignment: Lab 11

import simpy
import random

eventLog = []
waitingShoppers = []
idleTime = 0

def shopper(env, id):
    arrive = env.now
    items = random.triangular(5, 100, 25) #I like the idea of a "weighted" item count here.
    shoppingTime = items // 2 # shopping takes 1/2 a minute per item.
    yield env.timeout(shoppingTime)
    # join the queue of waiting shoppers
    waitingShoppers.append((id, items, arrive, env.now))

def checker(env):
    global idleTime
    while True:
        while len(waitingShoppers) == 0:
            idleTime += 1
            yield env.timeout(1) # wait a minute and check again

        customer = waitingShoppers.pop(0)
        items = customer[1]
        checkoutTime = items // 10 + 1
        yield env.timeout(checkoutTime)

        eventLog.append((customer[0], customer[1], customer[2], customer[3], env.now))

def customerArrival(env):
    customerNumber = 0
    while True:
        customerNumber += 1
        env.process(shopper(env, customerNumber))
        yield env.timeout(2) #New shopper every two minutes

def processResults():
    totalWait = 0
    totalShoppers = 0
    totalItems = 0 #New/used for results of total and average items
    maxWait = 0 #New/used to illustrate growth/improvement

    for e in eventLog:
        items = e[1]
        waitTime = e[4] - e[3] #depart time - done shopping time
        totalWait += waitTime
        totalShoppers += 1
        totalItems += items

        if waitTime > maxWait:
            maxWait = waitTime

    avgWait = totalWait / totalShoppers
    avgItems = totalItems / totalShoppers

    print(len(waitingShoppers), "shoppers were still waiting after this simulation expired.")
    print("The average wait time was %.2f minutes." % avgWait)
    print("The maximum wait time was %.2f minutes." % maxWait)
    print("The total idle time was %d minutes" % idleTime)
    print("The total number of items purchased was %d." % totalItems)
    print("The average number of items per shopper was %.2f" % avgItems)

def main():
    numberCheckers = 6

    env = simpy.Environment()

    env.process(customerArrival(env))
    for i in range(numberCheckers):
        env.process(checker(env))

    env.run(until=180 )
    print("Based on", numberCheckers, "cashiers, the following experience may occur:")
    processResults()

if __name__ == '__main__':
    main()