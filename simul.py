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
MAX_CAPACITY = 500
MAX_CAPACITY_COVID = 250
MAX_STOCK = 200
PRODUCT_LIST = ['Frozen Foods', 'Non-Frozen Foods', 'Beverages', 'Non-Prescription Medicine', 'Prescription Medicine', 'Meat', 'Pasteries']

# Stock Variables
frozenFoodStock = 200
nonFrozenFoodStock = 200
beverageStock = 200
nonPresecriptionMedicineStock = 200
prescriptionMedicineStock = 200
meatStock = 200
pasteryStock = 200

# Data Variables
arrivalTimes = []

def WeekDaySource(env):
    customerNum = 1
    interArrival = 0.0
    while env.now < 54000.0: # 15 hour work day in seconds

        arrivalTimes.append(env.now)

        shoppingList = random.sample(PRODUCT_LIST, random.randint(1,7))

        #print(shoppingList)

        #print("customer %d arrived at %7.4f" % (customerNum, env.now))

        if env.now < 14400.0:
            interArrival = random.expovariate(1.0/LOW_INTENSITY_INTERVAL)
        elif env.now < 32400.0:
            interArrival = random.expovariate(1.0/MEDIUM_INTENTSITY_INTERVAL)
        elif env.now < 46800.0:
            interArrival = random.expovariate(1.0/HIGH_INTENSITY_INTERVAL)
        elif env.now < 50400.0:
            interArrival = random.expovariate(1.0/MEDIUM_INTENTSITY_INTERVAL)
        elif env.now < 54000.0:
            interArrival = random.expovariate(1.0/LOW_INTENSITY_INTERVAL)

        #print("interArrival Time %7.4f at %7.4f" % (interArrival, env.now))

        customerNum += 1

        yield env.timeout(interArrival)

def WeekEndSource(env):
    customerNum = 1
    interArrival = 0.0
    while env.now < 54000.0: # 15 hour work day in seconds

        arrivalTimes.append(env.now)

        shoppingList = random.sample(PRODUCT_LIST, random.randint(1,7))

        #print(shoppingList)

        #print("customer %d arrived at %7.4f" % (customerNum, env.now))

        if env.now < 3600.0:
            interArrival = random.expovariate(1.0/LOW_INTENSITY_INTERVAL)
        elif env.now < 14400.0:
            interArrival = random.expovariate(1.0/MEDIUM_INTENTSITY_INTERVAL)
        elif env.now < 43200.0:
            interArrival = random.expovariate(1.0/HIGH_INTENSITY_INTERVAL)
        elif env.now < 50400.0:
            interArrival = random.expovariate(1.0/MEDIUM_INTENTSITY_INTERVAL)
        elif env.now < 54000.0:
            interArrival = random.expovariate(1.0/LOW_INTENSITY_INTERVAL)

        #print("interArrival Time %7.4f at %7.4f" % (interArrival, env.now))

        customerNum += 1

        yield env.timeout(interArrival)

def Shopping(env, name, shoppingList):
    for i in range(0, len(shoppingList)):
        shoppingTime = random.expovariate(1.0/SHOPPING_TIME)
        yield env.timeout()

        if shoppingList[i] == "Frozen Foods":
            frozenFoodStock -= 1
        elif shoppingList[i] == "Non-Frozen Foods":
            nonFrozenFoodStock -= 1
        elif shoppingList[i] == "Beverages":
            beverageStock -= 1
        elif shoppingList[i] == "Non-Prescription Medicine":
            nonPresecriptionMedicineStock -= 1
        elif shoppingList[i] == "Prescription Medicine":
            prescriptionMedicineStock -= 1
        elif shoppingList[i] == "Meat":
            meatStock -= 1
        elif shoppingList[i] == "Pasteries":
            pasteryStock -= 1

random.seed(RANDOM_SEED)
env = simpy.Environment()

env.process(WeekDaySource(env))
env.run()


plt.subplot(1,1,1)
counts, bins = np.histogram(arrivalTimes,16)
plt.hist(bins[:-1], bins, weights=counts)
plt.title('Arrival Times')

plt.show()
