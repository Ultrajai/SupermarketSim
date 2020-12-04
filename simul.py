import simpy
import random
import matplotlib.pyplot as plt
import numpy as np

LOW_INTENSITY_INTERVAL = 90.0
MEDIUM_INTENTSITY_INTERVAL = 30.0
HIGH_INTENSITY_INTERVAL = 18.0
RANDOM_SEED = random.randint(0,10000)

arrivalTimes = []

def WeekDaySource(env):
    customerNum = 1
    interArrival = 0.0
    while env.now < 54000.0: # 15 hour work day in seconds

        arrivalTimes.append(env.now)

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

random.seed(RANDOM_SEED)
env = simpy.Environment()

env.process(WeekEndSource(env))
env.run()


plt.subplot(1,1,1)
counts, bins = np.histogram(arrivalTimes,100)
plt.hist(bins[:-1], bins, weights=counts)
plt.title('Arrival Times')

plt.show()
