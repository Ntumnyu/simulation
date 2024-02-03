

import numpy as np

def lognormal(mean, sigma):
    z = np.random.randn()  # Generate a standard normally distributed random variable
    x = np.exp(mean + sigma * z)  # Transform it into a lognormally distributed random variable
    return x

# Create a uniform random number generator function
def uniform():
    return np.random.uniform()


# Create an exponential random number generator function
def expntl(x):
    # Generate a uniform random number from 0 to 1
    z = uniform()
    # Ensure z is not 0 or 1
    while z == 0 or z == 1:
        z = uniform()
    # Compute exponential random variable
    return -x * np.log(z)


def main():

    end_time = 10000  # Total time to simulate
    Ta =6  # Mean time between arrivals
    Tp = 1/Ta
    Ts = 0.1  # Mean service time
    time = 0.0  # Simulation time
    t1 = 0.0  # Time for next event #1 (arrival)
    t2 = end_time  # Time for next event #2 (departure)
    n = 0  # Number of customers in the system
    c = 0  # Number of service completions
    b = 0.0  # Total busy time
    s = 0.0  # Area of number of customers in system
    tn = time  # Variable for "last event time"
    tb = 0.0  # Variable for "last start of busy time"
    x = 0.0  # Throughput
    u = 0.0  # Utilization
    l = 0.0  # Mean number in the system
    w = 0.0  # Mean waiting time
    mean = np.log(Tp)  # Mean of the associated normal distribution (logarithm of the mean)
    sigma = 1.0  # Standard deviation of the associated normal distribution
    next_event_time = lognormal(mean, sigma)  # Generate a lognormally distributed random value

    # Main simulation loop
    while time < end_time:
        if t1 < t2:  # Event #1 (arrival)
            time = t1
            s += n * (time - tn)  # Update area under "s" curve
            n += 1
            tn = time  # tn = "last event time" for next event
            t1 = time + next_event_time  # Schedule next arrival event
            if n == 1:
                tb = time  # Set "last start of busy time"
                t2 = time + expntl(Ts)  # Schedule next departure event
        else:  # Event #2 (departure)
            time = t2
            s += n * (time - tn)  # Update area under "s" curve
            n -= 1
            tn = time  # tn = "last event time" for next event
            c += 1  # Increment number of completions
            if n > 0:
                t2 = time + expntl(Ts)  # Schedule next departure event
            else:
                t2 = end_time
                b += time - tb  # Update busy time sum if empty

    # Compute outputs
    x = c / time  # Compute throughput rate
    u = b / time  # Compute server utilization
    l = s / time  # Compute mean number in system
    w = l / x  # Compute mean residence or system time

    # Output results
    print("===============================================================")
    print("= *** Results from M/M/1 simulation *** =")
    print("===============================================================")
    print("= Total simulated time = %.4f sec" % end_time)
    print("===============================================================")
    print("= INPUTS:")
    print("= Mean time between arrivals = %.4f sec" % Tp)
    print("= Mean service time = %.4f sec" % Ts)
    print("===============================================================")
    print("= OUTPUTS:")
    print("= Number of completions = %d cust" % c)
    print("= Throughput rate = %.4f cust/sec" % x)
    print("= Server utilization = %.4f %%" % (100.0 * u))
    print("= Mean number in system = %.4f cust" % l)
    print("= Mean residence time = %.4f sec" % w)
    print("===============================================================")


if __name__ == "__main__":
    main()
