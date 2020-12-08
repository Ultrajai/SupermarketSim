import simpy
import random
import matplotlib.pyplot as plt
import numpy as np

RANDOM_SEED = random.randint(0,10000)

# Simulation Constants
LOW_INTENSITY_INTERVAL = 90.0
MEDIUM_INTENTSITY_INTERVAL = 30.0
HIGH_INTENSITY_INTERVAL = 18.0

SHOPPING_TIME = 60.0
RESTOKE_TIME = 300.0
CHECKOUT_SERVICE_TIME = 240.0
OTHER_QUEUE_SERVICE_TIME = 60.0

MAX_STOCK = 200
PRODUCT_LIST = ['Frozen Foods', 'Non-Frozen Foods', 'Beverages', 'Non-Prescription Medicine', 'Prescription Medicine', 'Meat', 'Pasteries']

# Stock Variables
frozenFoodStock = 200
nonFrozenFoodStock = 200
beverageStock = 200
nonPrescriptionMedicineStock = 200
restockingFrozenFood = False
restockingNonFrozenFood = False
restockingBeverage = False
restockingNonPrescriptionMedicine = False

# Store variables
capacity = 500

# Data Variables
arrivalTimes = []
storeCapacity = []

def FrozenFoodRestockProcess(env):
    global frozenFoodStock, restockingFrozenFood
    print('Restocking Frozen Food at %7.4f' % env.now)
    restockTime = random.expovariate(1.0 / RESTOKE_TIME)
    yield env.timeout(restockTime)
    frozenFoodStock = 200
    restockingFrozenFood = False

def NonFrozenFoodRestockProcess(env):
    global nonFrozenFoodStock, restockingNonFrozenFood
    print('Restocking Non-Frozen Food at %7.4f' % env.now)
    restockTime = random.expovariate(1.0 / RESTOKE_TIME)
    yield env.timeout(restockTime)
    nonFrozenFoodStock = 200
    restockingNonFrozenFood = False

def BeverageRestockProcess(env):
    global beverageStock, restockingBeverage
    print('Restocking Beverage at %7.4f' % env.now)
    restockTime = random.expovariate(1.0 / RESTOKE_TIME)
    yield env.timeout(restockTime)
    beverageStock = 200
    restockingBeverage = False

def NonPrescriptionMedicineRestockProcess(env):
    global nonPrescriptionMedicineStock, restockingNonPrescriptionMedicine
    print('Restocking Non-Prescription Medicine at %7.4f' % env.now)
    restockTime = random.expovariate(1.0 / RESTOKE_TIME)
    yield env.timeout(restockTime)
    nonPrescriptionMedicineStock = 200
    restockingNonPrescriptionMedicine = False

def WeekDaySource(env):
    global frozenFoodStock, nonFrozenFoodStock, beverageStock, nonPrescriptionMedicineStock, restockingFrozenFood, restockingNonFrozenFood, restockingBeverage, restockingNonPrescriptionMedicine, capacity
    customerNum = 1
    interArrival = 0.0

    while env.now < 54000.0: # 15 hour work day in seconds

        storeCapacity.append(capacity)

        if capacity == 0:
            print('Customer tried to enter the store but was full')
        else:

            capacity -= 1

            arrivalTimes.append(env.now)

            shoppingList = GenerateShoppingList()

            #print(shoppingList)

            print("customer %02d arrived at %7.4f" % (customerNum, env.now))

            s = Shopping(env, "Customer %02d" % customerNum, shoppingList)

            env.process(s)

            if env.now < 14400.0:
                interArrival = random.expovariate(1.0 / LOW_INTENSITY_INTERVAL)
            elif env.now < 32400.0:
                interArrival = random.expovariate(1.0 / MEDIUM_INTENTSITY_INTERVAL)
            elif env.now < 46800.0:
                interArrival = random.expovariate(1.0 / HIGH_INTENSITY_INTERVAL)
            elif env.now < 50400.0:
                interArrival = random.expovariate(1.0 / MEDIUM_INTENTSITY_INTERVAL)
            elif env.now < 54000.0:
                interArrival = random.expovariate(1.0 / LOW_INTENSITY_INTERVAL)

            #print("interArrival Time %7.4f at %7.4f" % (interArrival, env.now))

            if frozenFoodStock < 50 and not restockingFrozenFood:
                restockingFrozenFood = True
                env.process(FrozenFoodRestockProcess(env))

            if nonFrozenFoodStock < 50 and not restockingNonFrozenFood:
                restockingNonFrozenFood = True
                env.process(NonFrozenFoodRestockProcess(env))

            if beverageStock < 50 and not restockingBeverage:
                restockingBeverage = True
                env.process(BeverageRestockProcess(env))

            if nonPrescriptionMedicineStock < 50 and not restockingNonPrescriptionMedicine:
                restockingNonPrescriptionMedicine = True
                env.process(NonPrescriptionMedicineRestockProcess(env))

            customerNum += 1

        yield env.timeout(interArrival)

def WeekEndSource(env):
    global frozenFoodStock, nonFrozenFoodStock, beverageStock, nonPrescriptionMedicineStock, restockingFrozenFood, restockingNonFrozenFood, restockingBeverage, restockingNonPrescriptionMedicine, capacity
    customerNum = 1
    interArrival = 0.0

    while env.now < 54000.0: # 15 hour work day in seconds

        storeCapacity.append(capacity)

        if capacity == 0:
            print('Customer tried to enter the store but was full')
        else:

            capacity -= 1

            arrivalTimes.append(env.now)

            shoppingList = GenerateShoppingList()

            #print(shoppingList)

            print("customer %d arrived at %7.4f" % (customerNum, env.now))

            s = Shopping(env, "Customer %02d" % customerNum, shoppingList)

            env.process(s)

            if env.now < 3600.0:
                interArrival = random.expovariate(1.0 / LOW_INTENSITY_INTERVAL)
            elif env.now < 14400.0:
                interArrival = random.expovariate(1.0 / MEDIUM_INTENTSITY_INTERVAL)
            elif env.now < 43200.0:
                interArrival = random.expovariate(1.0 / HIGH_INTENSITY_INTERVAL)
            elif env.now < 50400.0:
                interArrival = random.expovariate(1.0 / MEDIUM_INTENTSITY_INTERVAL)
            elif env.now < 54000.0:
                interArrival = random.expovariate(1.0 / LOW_INTENSITY_INTERVAL)

            #print("interArrival Time %7.4f at %7.4f" % (interArrival, env.now))

            if frozenFoodStock < 50 and not restockingFrozenFood:
                restockingFrozenFood = True
                env.process(FrozenFoodRestockProcess(env))

            if nonFrozenFoodStock < 50 and not restockingNonFrozenFood:
                restockingNonFrozenFood = True
                env.process(NonFrozenFoodRestockProcess(env))

            if beverageStock < 50 and not restockingBeverage:
                restockingBeverage = True
                env.process(BeverageRestockProcess(env))

            if nonPrescriptionMedicineStock < 50 and not restockingNonPrescriptionMedicine:
                restockingNonPrescriptionMedicine = True
                env.process(NonPrescriptionMedicineRestockProcess(env))

            customerNum += 1

        yield env.timeout(interArrival)

def GenerateShoppingList():
    shoppingList = []
    rngList = [random.random(),random.random(),random.random(),random.random(),random.random(),random.random(),random.random()]

    for i in range(0,6):
        if i == 0 and rngList[i] < 0.50:
            shoppingList.append(PRODUCT_LIST[0])
        elif i == 1 and rngList[i] < 0.50:
            shoppingList.append(PRODUCT_LIST[1])
        elif i == 2 and rngList[i] < 0.50:
            shoppingList.append(PRODUCT_LIST[2])
        elif i == 3 and rngList[i] < 0.50:
            shoppingList.append(PRODUCT_LIST[3])
        elif i == 4 and rngList[i] < 0.25:
            shoppingList.append(PRODUCT_LIST[4])
        elif i == 5 and rngList[i] < 0.25:
            shoppingList.append(PRODUCT_LIST[5])
        elif i == 6 and rngList[i] < 0.25:
            shoppingList.append(PRODUCT_LIST[6])

    return shoppingList

def Shopping(env, name, shoppingList):

    global frozenFoodStock, nonFrozenFoodStock, beverageStock, nonPrescriptionMedicineStock, capacity

    for i in range(0, len(shoppingList)):

        if shoppingList[i] == "Prescription Medicine":
            print('%s enters pharmacy queue (Queue length: %d)' % (name, len(pharmacy.queue)))
            yield env.process(UseResource(env, name, pharmacy, OTHER_QUEUE_SERVICE_TIME))
            print('%s exits pharmacy queue' % name)
            continue
        elif shoppingList[i] == "Meat":
            print('%s enters butcher queue (Queue length: %d)' % (name, len(butcher.queue)))
            yield env.process(UseResource(env, name, butcher, OTHER_QUEUE_SERVICE_TIME))
            print('%s exits butcher queue' % name)
            continue
        elif shoppingList[i] == "Pasteries":
            print('%s enters bakery queue (Queue length: %d)' % (name, len(bakery.queue)))
            yield env.process(UseResource(env, name, bakery, OTHER_QUEUE_SERVICE_TIME))
            print('%s exits bakery queue' % name)
            continue

        shoppingTime = random.expovariate(1.0 / SHOPPING_TIME)
        yield env.timeout(shoppingTime)

        if shoppingList[i] == "Frozen Foods":
            print('%s Taking 1 stock of Frozen Foods at %7.4f' % (name, env.now))
            frozenFoodStock -= 1
        elif shoppingList[i] == "Non-Frozen Foods":
            print('%s Taking 1 stock of Non-Frozen Foods at %7.4f' % (name, env.now))
            nonFrozenFoodStock -= 1
        elif shoppingList[i] == "Beverages":
            print('%s Taking 1 stock of Beverages at %7.4f' % (name, env.now))
            beverageStock -= 1
        elif shoppingList[i] == "Non-Prescription Medicine":
            print('%s Taking 1 stock of Non-Prescription Medicine at %7.4f' % (name, env.now))
            nonPrescriptionMedicineStock -= 1

    env.process(Checkout(env, name))
    capacity += 1

def Checkout(env, name):

    currentMin = len(cashiers[0].queue)
    selectedStation = cashiers[0]

    for station in cashiers:
        if currentMin > len(station.queue):
            currentMin = len(station.queue)
            selectedStation = station

    if currentMin > len(selfCheckout.queue):
        selectedStation = selfCheckout
        print('%s Entering self-checkout queue (Queue Length: %d)' % (name, len(selectedStation.queue)))
    elif (len(selfCheckout.queue) - currentMin) < 10:
        selectedStation = selfCheckout
        print('%s Entering self-checkout queue (Queue Length: %d)' % (name, len(selectedStation.queue)))
    else:
        print('%s Entering cashier checkout queue (Queue Length: %d)' % (name, len(selectedStation.queue)))


    yield env.process(UseResource(env, name, selectedStation, CHECKOUT_SERVICE_TIME))
    print('%s Exiting checkout queue' % name)

def UseResource(env, name, resource, serviceTime):
    with resource.request() as req:

        results = yield req | env.timeout(5400.0) # customer can wait 1.5 hr

        if req in results:
            tis = random.expovariate(1.0 / serviceTime)
            yield env.timeout(tis)
        else:
            print('Customer %s left the Queue' % name)


random.seed(RANDOM_SEED)
env = simpy.Environment()

# resources
cashiers = [simpy.Resource(env, capacity=1),simpy.Resource(env, capacity=1),simpy.Resource(env, capacity=1),simpy.Resource(env, capacity=1),simpy.Resource(env, capacity=1),simpy.Resource(env, capacity=1)]
selfCheckout = simpy.Resource(env, capacity=4)
bakery = simpy.Resource(env, capacity=1)
butcher = simpy.Resource(env, capacity=1)
pharmacy = simpy.Resource(env, capacity=1)

env.process(WeekEndSource(env))
env.run()

plt.subplot(2,2,1)
counts, bins = np.histogram(arrivalTimes,50)
plt.hist(bins[:-1], bins, weights=counts)
plt.title('Arrival Times')

plt.subplot(2,2,2)
plt.plot(storeCapacity)
plt.title('Capacity')

plt.show()
