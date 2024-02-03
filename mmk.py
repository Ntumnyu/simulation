import simpy
import random
import matplotlib.pyplot as plt
import numpy as np


def exponential_distribution(n, lmbda):
  y = np.random.uniform(0, 1, n)
  x = [-np.log(1 - y[i]) / lmbda for i in range(len(y))]
  return x

def poisson_distribution(n, lmbda):
  inter_event_duration = exponential_distribution(n-1, lmbda)
  event_dates = [0] * n
  for c in range(1,n):
    event_dates[c] = event_dates[c-1] + inter_event_duration[c-1]
  return event_dates

def mm1K(arrivals, services, K):

  actual_arrivals = arrivals[:K] # List of arrival times of people who actually entered
  n = len(arrivals)
  exits = [arrivals[0] + services[0]]
  evolution_of_rejected_clients = [0]*K

  for i in range (1, K): # Calculation of the first K exits (because K = client in service + queue capacity)
    if exits[-1] > arrivals[i]:
      exits.append(exits[-1] + services[i])
    else:
      exits.append(arrivals[i] + services[i])

  c = 0 # Counter of rejected persons
  for i in range(K, n):
    if exits[-K] < arrivals[i] : # Test on entries in the queue: The Kth person must have exited for a new person to enter
      actual_arrivals.append(arrivals[i]) # If the condition is met: Add the new client to the list of actual entries
      if exits[-1] > arrivals[i]:
        exits.append(exits[-1] + services[i])
      else:
        exits.append(arrivals[i] + services[i])
    else :
      c = c + 1
    evolution_of_rejected_clients.append(c)
  return actual_arrivals, exits, evolution_of_rejected_clients

lmbda = 3
mu = 4
K = 10
n = 10000

arrivals = poisson_distribution(n, lmbda)
services = exponential_distribution(n, mu)

exit_mm1k = mm1K(arrivals, services, K)

plt.plot(range(len(exit_mm1k[2])), exit_mm1k[2])
plt.xlabel("Arrival of customers")
plt.ylabel("Cumulative number of rejected customers")
plt.title("Cumulative number of rejected customers as customers arrive over time")
plt.show()
