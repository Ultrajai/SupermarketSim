import simpy
import random
import threading
import matplotlib.pyplot as plt
import numpy as np

RANDOM_SEED = random.randint(0,10000)

# Simulation Constants
LOW_INTENSITY_INTERVAL = 90.0
MEDIUM_INTENSITY_INTERVAL = 30.0
HIGH_INTENSITY_INTERVAL = 18.0

COVID_LOW_INTENSITY_INTERVAL = 90.0
COVID_MEDIUM_INTENSITY_INTERVAL = 30.0
COVID_HIGH_INTENSITY_INTERVAL = 12.0

SHOPPING_TIME = 60.0 # 1 min in seconds
RESTOKE_TIME = 300.0 # 5 mins in seconds
CHECKOUT_SERVICE_TIME = 240.0 # 4 mins in seconds
OTHER_QUEUE_SERVICE_TIME = 60.0 # 1 min in seconds
PATIENCE_DURATION = 5400.0 # 1.5 hours in seconds
SIMULATION_DURATION = 54000.0 # 15 hours in seconds

MAX_STOCK = 300
STOCK_DANGER_ZONE = 200
PRODUCT_LIST = ['Frozen Foods', 'Non-Frozen Foods', 'Beverages', 'Non-Prescription Medicine', 'Prescription Medicine', 'Meat', 'Pasteries']

MAX_STORE_CAPACITY = 500
COVID_MAX_STORE_CAPACITY = 250

# Stock Variables
frozenFoodStock = MAX_STOCK
nonFrozenFoodStock = MAX_STOCK
beverageStock = MAX_STOCK
nonPrescriptionMedicineStock = MAX_STOCK
restockingFrozenFood = False
restockingNonFrozenFood = False
restockingBeverage = False
restockingNonPrescriptionMedicine = False

# Store variables
capacity = COVID_MAX_STORE_CAPACITY

# Data Variables
arrivalTimes = []
storeCapacity = []
listOfUncollectedGoods = []
listOfFrozenFoodStock = []
listOfNonFrozenFoodStock = []
listOfBeverageStock = []
listOfMedicineStock = []

# restocking process for frozenFoodStock
def FrozenFoodRestockProcess(env):
    global frozenFoodStock, restockingFrozenFood
    restockTime = random.expovariate(1.0 / RESTOKE_TIME)
    print('Restocking Frozen Food at %7.4f for %7.4f' % (env.now, restockTime))
    yield env.timeout(restockTime)
    frozenFoodStock = MAX_STOCK
    restockingFrozenFood = False

# restocking process for nonFrozenFoodStock
def NonFrozenFoodRestockProcess(env):
    global nonFrozenFoodStock, restockingNonFrozenFood
    restockTime = random.expovariate(1.0 / RESTOKE_TIME)
    print('Restocking Non-Frozen Food at %7.4f for %7.4f' % (env.now, restockTime))
    yield env.timeout(restockTime)
    nonFrozenFoodStock = MAX_STOCK
    restockingNonFrozenFood = False

# restocking process for beverageStock
def BeverageRestockProcess(env):
    global beverageStock, restockingBeverage
    restockTime = random.expovariate(1.0 / RESTOKE_TIME)
    print('Restocking Beverage at %7.4f for %7.4f' % (env.now, restockTime))
    yield env.timeout(restockTime)
    beverageStock = MAX_STOCK
    restockingBeverage = False

# restocking process for nonPrescriptionMedicineStock
def NonPrescriptionMedicineRestockProcess(env):
    global nonPrescriptionMedicineStock, restockingNonPrescriptionMedicine
    restockTime = random.expovariate(1.0 / RESTOKE_TIME)
    print('Restocking Non-Prescription Medicine at %7.4f for %7.4f' % (env.now, restockTime))
    yield env.timeout(restockTime)
    nonPrescriptionMedicineStock = MAX_STOCK
    restockingNonPrescriptionMedicine = False

# main restock process that handles restocking goods at the store
def MainRestockProcess():
    global restockingFrozenFood, restockingNonFrozenFood, restockingBeverage, restockingNonPrescriptionMedicine, env

    while env.now < SIMULATION_DURATION:
        if frozenFoodStock < STOCK_DANGER_ZONE and not restockingFrozenFood:
            restockingFrozenFood = True
            env.process(FrozenFoodRestockProcess(env))

        if nonFrozenFoodStock < STOCK_DANGER_ZONE and not restockingNonFrozenFood:
            restockingNonFrozenFood = True
            env.process(NonFrozenFoodRestockProcess(env))

        if beverageStock < STOCK_DANGER_ZONE and not restockingBeverage:
            restockingBeverage = True
            env.process(BeverageRestockProcess(env))

        if nonPrescriptionMedicineStock < STOCK_DANGER_ZONE and not restockingNonPrescriptionMedicine:
            restockingNonPrescriptionMedicine = True
            env.process(NonPrescriptionMedicineRestockProcess(env))

# generates the shopping list for a customer
def GenerateShoppingList():
    shoppingList = []

    for i in range(0,7):

        RANDOM_SEED = random.randint(0,10000)
        random.seed(RANDOM_SEED)
        randomVal = random.random()

        if i == 0 and randomVal < 0.50:
            shoppingList.append(PRODUCT_LIST[0])
        elif i == 1 and randomVal < 0.50:
            shoppingList.append(PRODUCT_LIST[1])
        elif i == 2 and randomVal < 0.50:
            shoppingList.append(PRODUCT_LIST[2])
        elif i == 3 and randomVal < 0.50:
            shoppingList.append(PRODUCT_LIST[3])
        elif i == 4 and randomVal < 0.25:
            shoppingList.append(PRODUCT_LIST[4])
        elif i == 5 and randomVal < 0.25:
            shoppingList.append(PRODUCT_LIST[5])
        elif i == 6 and randomVal < 0.25:
            shoppingList.append(PRODUCT_LIST[6])

    return shoppingList

# shopping process for customers so that they can enter queues and collect goods
def Shopping(env, name, shoppingList):

    global frozenFoodStock, nonFrozenFoodStock, beverageStock, nonPrescriptionMedicineStock, capacity
    numOfUncollectedGoods = 0

    for i in range(0, len(shoppingList)):

        if shoppingList[i] == "Prescription Medicine":
            print('%s enters pharmacy queue (Queue length: %d)' % (name, len(pharmacy.queue)))
            numOfUncollectedGoods += yield env.process(UseResource(env, name, pharmacy, None, OTHER_QUEUE_SERVICE_TIME))
            print('%s exits pharmacy queue' % name)
            continue
        elif shoppingList[i] == "Meat":
            print('%s enters butcher queue (Queue length: %d)' % (name, len(butcher.queue)))
            numOfUncollectedGoods += yield env.process(UseResource(env, name, butcher, None, OTHER_QUEUE_SERVICE_TIME))
            print('%s exits butcher queue' % name)
            continue
        elif shoppingList[i] == "Pasteries":
            print('%s enters bakery queue (Queue length: %d)' % (name, len(bakery.queue)))
            numOfUncollectedGoods += yield env.process(UseResource(env, name, bakery, None, OTHER_QUEUE_SERVICE_TIME))
            print('%s exits bakery queue' % name)
            continue

        shoppingTime = random.expovariate(1.0 / SHOPPING_TIME)
        yield env.timeout(shoppingTime)

        if shoppingList[i] == "Frozen Foods" and frozenFoodStock > 0:
            print('%s Taking 1 stock of Frozen Foods at %7.4f' % (name, env.now))
            frozenFoodStock -= 1
        elif shoppingList[i] == "Non-Frozen Foods" and nonFrozenFoodStock > 0:
            print('%s Taking 1 stock of Non-Frozen Foods at %7.4f' % (name, env.now))
            nonFrozenFoodStock -= 1
        elif shoppingList[i] == "Beverages" and beverageStock > 0:
            print('%s Taking 1 stock of Beverages at %7.4f' % (name, env.now))
            beverageStock -= 1
        elif shoppingList[i] == "Non-Prescription Medicine" and nonPrescriptionMedicineStock > 0:
            print('%s Taking 1 stock of Non-Prescription Medicine at %7.4f' % (name, env.now))
            nonPrescriptionMedicineStock -= 1
        else:
            numOfUncollectedGoods += 1

    yield env.process(Checkout(env, name, shoppingList))
    capacity += 1
    print("%s couldn't collect %d" % (name, numOfUncollectedGoods))
    listOfUncollectedGoods.append(numOfUncollectedGoods)

# final process for customers after having finished shopping to enter checkout queues
# picks the best queue for the customer in their perspective
def Checkout(env, name, shoppingList):

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


    yield env.process(UseResource(env, name, selectedStation, shoppingList, CHECKOUT_SERVICE_TIME))
    print('%s Exiting checkout queue' % name)

# Generic function that handles waiting in a queue for a resource and using a resource
def UseResource(env, name, resource, shoppingList, serviceTime):
    global frozenFoodStock, nonFrozenFoodStock, beverageStock, nonPrescriptionMedicineStock

    with resource.request() as req:

        results = yield req | env.timeout(PATIENCE_DURATION) # customer can wait 1.5 hr

        if req in results:
            tis = random.expovariate(1.0 / serviceTime)
            yield env.timeout(tis)
        else:
            print('Customer %s left the Queue' % name)
            if resource == bakery or resource == butcher or resource == pharmacy:
                return 1
            else:
                for i in range(0, len(shoppingList)):
                    if shoppingList[i] == "Frozen Foods":
                        frozenFoodStock += 1
                    elif shoppingList[i] == "Non-Frozen Foods" and nonFrozenFoodStock > 0:
                        nonFrozenFoodStock += 1
                    elif shoppingList[i] == "Beverages" and beverageStock > 0:
                        beverageStock += 1
                    elif shoppingList[i] == "Non-Prescription Medicine" and nonPrescriptionMedicineStock > 0:
                        nonPrescriptionMedicineStock += 1
                return 0
    return 0

# weekday simulation driver
def WeekDaySource(env):
    global frozenFoodStock, nonFrozenFoodStock, beverageStock, nonPrescriptionMedicineStock, capacity
    customerNum = 1
    interArrival = 0.0

    while env.now < SIMULATION_DURATION: # 15 hour work day in seconds

        storeCapacity.append(capacity)

        listOfFrozenFoodStock.append(frozenFoodStock)
        listOfNonFrozenFoodStock.append(nonFrozenFoodStock)
        listOfBeverageStock.append(beverageStock)

        if capacity == 0:
            print('Customer tried to enter the store but was full')
        else:

            capacity -= 1

            arrivalTimes.append(env.now)

            shoppingList = GenerateShoppingList()

            print("customer %02d arrived at %7.4f" % (customerNum, env.now))

            s = Shopping(env, "Customer %02d" % customerNum, shoppingList)

            env.process(s)



            customerNum += 1

        # setting up new interarrival time
        if env.now < 14400.0:
            interArrival = random.expovariate(1.0 / LOW_INTENSITY_INTERVAL)
        elif env.now < 32400.0:
            interArrival = random.expovariate(1.0 / MEDIUM_INTENSITY_INTERVAL)
        elif env.now < 46800.0:
            interArrival = random.expovariate(1.0 / HIGH_INTENSITY_INTERVAL)
        elif env.now < 50400.0:
            interArrival = random.expovariate(1.0 / MEDIUM_INTENSITY_INTERVAL)
        elif env.now < 54000.0:
            interArrival = random.expovariate(1.0 / LOW_INTENSITY_INTERVAL)

        yield env.timeout(interArrival)

# weekend simulation driver
def WeekEndSource(env):
    global frozenFoodStock, nonFrozenFoodStock, beverageStock, nonPrescriptionMedicineStock, restockingFrozenFood, restockingNonFrozenFood, restockingBeverage, restockingNonPrescriptionMedicine, capacity
    customerNum = 1
    interArrival = 0.0

    while env.now < SIMULATION_DURATION: # 15 hour work day in seconds

        storeCapacity.append(capacity)

        listOfFrozenFoodStock.append(frozenFoodStock)
        listOfNonFrozenFoodStock.append(nonFrozenFoodStock)
        listOfBeverageStock.append(beverageStock)

        if capacity == 0:
            print('Customer tried to enter the store but was full')
        else:

            capacity -= 1

            arrivalTimes.append(env.now)

            shoppingList = GenerateShoppingList()

            print("customer %d arrived at %7.4f" % (customerNum, env.now))

            s = Shopping(env, "Customer %02d" % customerNum, shoppingList)

            env.process(s)

            customerNum += 1

        if env.now < 3600.0:
            interArrival = random.expovariate(1.0 / LOW_INTENSITY_INTERVAL)
        elif env.now < 14400.0:
            interArrival = random.expovariate(1.0 / MEDIUM_INTENSITY_INTERVAL)
        elif env.now < 43200.0:
            interArrival = random.expovariate(1.0 / HIGH_INTENSITY_INTERVAL)
        elif env.now < 50400.0:
            interArrival = random.expovariate(1.0 / MEDIUM_INTENSITY_INTERVAL)
        elif env.now < 54000.0:
            interArrival = random.expovariate(1.0 / LOW_INTENSITY_INTERVAL)

        yield env.timeout(interArrival)

# covid weekday simulation driver
def CovidWeekDaySource(env):
    global frozenFoodStock, nonFrozenFoodStock, beverageStock, nonPrescriptionMedicineStock, capacity
    customerNum = 1
    interArrival = 0.0

    while env.now < SIMULATION_DURATION: # 15 hour work day in seconds

        storeCapacity.append(capacity)

        listOfFrozenFoodStock.append(frozenFoodStock)
        listOfNonFrozenFoodStock.append(nonFrozenFoodStock)
        listOfBeverageStock.append(beverageStock)

        if capacity == 0:
            print('Customer tried to enter the store but was full')
        else:

            capacity -= 1

            arrivalTimes.append(env.now)

            shoppingList = GenerateShoppingList()

            print("customer %02d arrived at %7.4f" % (customerNum, env.now))

            s = Shopping(env, "Customer %02d" % customerNum, shoppingList)

            env.process(s)

            customerNum += 1

        # setting up new interarrival time
        if env.now < 14400.0:
            interArrival = random.expovariate(1.0 / COVID_LOW_INTENSITY_INTERVAL)
        elif env.now < 32400.0:
            interArrival = random.expovariate(1.0 / COVID_MEDIUM_INTENSITY_INTERVAL)
        elif env.now < 46800.0:
            interArrival = random.expovariate(1.0 / COVID_HIGH_INTENSITY_INTERVAL)
        elif env.now < 50400.0:
            interArrival = random.expovariate(1.0 / COVID_MEDIUM_INTENSITY_INTERVAL)
        elif env.now < 54000.0:
            interArrival = random.expovariate(1.0 / COVID_LOW_INTENSITY_INTERVAL)

        yield env.timeout(interArrival)

def CovidWeekEndSource(env):
    global frozenFoodStock, nonFrozenFoodStock, beverageStock, nonPrescriptionMedicineStock, restockingFrozenFood, restockingNonFrozenFood, restockingBeverage, restockingNonPrescriptionMedicine, capacity
    customerNum = 1
    interArrival = 0.0

    while env.now < SIMULATION_DURATION: # 15 hour work day in seconds

        storeCapacity.append(capacity)

        listOfFrozenFoodStock.append(frozenFoodStock)
        listOfNonFrozenFoodStock.append(nonFrozenFoodStock)
        listOfBeverageStock.append(beverageStock)
        listOfMedicineStock.append(nonPrescriptionMedicineStock)

        if capacity == 0:
            print('Customer tried to enter the store but was full')
        else:

            capacity -= 1

            arrivalTimes.append(env.now)

            shoppingList = GenerateShoppingList()

            print("customer %d arrived at %7.4f" % (customerNum, env.now))

            s = Shopping(env, "Customer %02d" % customerNum, shoppingList)

            env.process(s)

            customerNum += 1

        if env.now < 3600.0:
            interArrival = random.expovariate(1.0 / COVID_LOW_INTENSITY_INTERVAL)
        elif env.now < 14400.0:
            interArrival = random.expovariate(1.0 / COVID_MEDIUM_INTENSITY_INTERVAL)
        elif env.now < 43200.0:
            interArrival = random.expovariate(1.0 / COVID_HIGH_INTENSITY_INTERVAL)
        elif env.now < 50400.0:
            interArrival = random.expovariate(1.0 / COVID_MEDIUM_INTENSITY_INTERVAL)
        elif env.now < 54000.0:
            interArrival = random.expovariate(1.0 / COVID_LOW_INTENSITY_INTERVAL)

        yield env.timeout(interArrival)

random.seed(RANDOM_SEED)
env = simpy.Environment()

# starting restocking process in background
restockThread = threading.Thread(target=MainRestockProcess, name="Restock_Process")
restockThread.start()

# resources
cashiers = [simpy.Resource(env, capacity=1),simpy.Resource(env, capacity=1),simpy.Resource(env, capacity=1),simpy.Resource(env, capacity=1),simpy.Resource(env, capacity=1),simpy.Resource(env, capacity=1)]
selfCheckout = simpy.Resource(env, capacity=4)
bakery = simpy.Resource(env, capacity=1)
butcher = simpy.Resource(env, capacity=1)
pharmacy = simpy.Resource(env, capacity=1)

env.process(CovidWeekDaySource(env))
env.run()

#plt.subplot(2,2,1)
#counts, bins = np.histogram(arrivalTimes,50)
#plt.hist(bins[:-1], bins, weights=counts)
#plt.title('Arrival Times')

plt.subplot(2,2,1)
plt.plot(storeCapacity)
plt.title('Capacity')

plt.subplot(2,2,2)
plt.plot(listOfFrozenFoodStock)
plt.title('Frozen Foods')

plt.subplot(2,2,3)
plt.plot(listOfNonFrozenFoodStock)
plt.title('Non Frozen Foods')

plt.subplot(2,2,4)
plt.plot(listOfBeverageStock)
plt.title('Beverage Foods')

plt.show()
