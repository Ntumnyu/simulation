import numpy as np
import math

SIM_TIME = 1000   # Simulation time
ARR_TIME = 0.1      # Mean time between arrivals
SERV_TIME = 0.0667  # Mean service time
C = 3               # Number of servers

def uniform():
    return np.random.rand()

def expntl(x):
    # Generate a uniform random number from 0 to 1
    z = uniform()
    # Ensure z is not 0 or 1
    while z == 0 or z == 1:
        z = uniform()
    # Compute exponential random variable
    return -x * math.log(z)

def main():
    end_time = SIM_TIME  # Total time to simulate
    Ta = ARR_TIME        # Mean time between arrivals
    Ts = SERV_TIME       # Mean service time
    time = 0.0           # Simulation time
    t1 = 0.0             # Time for next event #1 (arrival)
    t2 = [SIM_TIME] * C  # Time for next event #2 (departure) for each server
    n = 0                # Number of customers in the system
    c = 0                # Number of service completions
    b = [0.0] * C        # Total busy time for each server
    s = 0.0              # Area of number of customers in system
    tn = time            # Variable for "last event time"
    x = 0.0              # Throughput
    u = 0.0              # Utilization
    l = 0.0              # Mean number in the system
    w = 0.0              # Mean waiting time

    # Main simulation loop
    while time < end_time:
        # Find the minimum departure time among all servers
        min_t2 = min(t2)

        if t1 < min_t2:  # *** Event #1 (arrival) ***
            time = t1
            s += n * (time - tn)  # Update area under "s" curve
            n += 1
            tn = time  # tn = "last event time" for next event
            t1 = time + expntl(Ta)

            # Find the first available server
            available_server = next((i for i, t in enumerate(t2) if t == min_t2), None)

            if available_server is not None:
                if n == 1:
                    tb = time  # Set "last start of busy time"
                    t2[available_server] = time + expntl(Ts)
        else:  # *** Event #2 (departure) ***
            for i, t in enumerate(t2):
                if t == min_t2:  # Find the server which is departing
                    time = t
                    s += n * (time - tn)  # Update area under "s" curve
                    n -= 1
                    tn = time  # tn = "last event time" for next event
                    c += 1      # Increment number of completions
                    t2[i] = SIM_TIME  # Reset the departure time for the server

                    if n > 0:
                        t2[i] = time + expntl(Ts)
                    else:
                        b[i] += time - tb  # Update busy time sum if empty
                    break

    # Compute outputs
    total_b = sum(b)
    x = c / time        # Compute throughput rate
    u = total_b / time  # Compute server utilization
    l = s / time        # Compute mean number in system
    w = l / x           # Compute mean residence or system time

    # Output results
    print("===============================================================")
    print("= *** Results from M/M/%d simulation *** =" % C)
    print("===============================================================")
    print("= Total simulated time = %3.4f sec" % end_time)
    print("===============================================================")
    print("= INPUTS:")
    print("= Mean time between arrivals = %f sec" % Ta)
    print("= Mean service time = %f sec" % Ts)
    print("= Number of servers = %d" % C)
    print("===============================================================")
    print("= OUTPUTS:")
    print("= Number of completions = %d cust" % c)
    print("= Throughput rate = %f cust/sec" % x)
    print("= Server utilization = %f %%" % (100.0 * u))
    print("= Mean number in system = %f cust" % l)
    print("= Mean residence time = %f sec" % w)
    print("===============================================================")

if __name__ == "__main__":
    main()
