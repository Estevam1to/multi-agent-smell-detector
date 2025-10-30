"""
The area of a circle is defined as πr^2. Estimate π to
 3 decimal places using a Monte Carlo method.

Hint: The basic equation of a circle is x2 + y2 = r2.
"""
import time
import random
import sys
from collections import deque

import numpy as np


# We can estimate pi by inscibing the unit circle inside the
# unit square and randomly dropping dots in the square's area.
# If we compare the ratio of points inside the circle to outside
# we should get an estimate of pi since the area of the unit
# circle is pi and the area of the unit circle is 4; meaning
# the prob. of dropping in the pi/4.


# going to start with a method that runs for a fixed number of
# iterations

def fixed_monte_carlo(n: int):
    """
    This method runs for a fixed number of iterations;

    I'm actually kinda shocked that github copilot actually created this from scratch.
    """
    pi = 0
    inside = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if x ** 2 + y ** 2 <= 1:
            inside += 1
    pi = 4 * inside / n
    return pi


# Want to try another implementation the runs until a certain tolerance is achieved;
# this is more in spirit of the question.  This will run until the first iteration
# gives a value close enough, but there is some error associated

def first_pi_monte_carlo(tolerance: float):
    """
    This method runs until the first iteration gives a value close enough to pi.
    """
    pi = 0
    inside = 0
    n = 0
    while True:
        n += 1
        x = random.random()
        y = random.random()
        if x ** 2 + y ** 2 <= 1:
            inside += 1
        pi = 4 * inside / n
        if abs(pi - np.pi) <= tolerance:
            break
    return n, pi


# because the above method is a bit unpredictable this method will run until the estimate and
# the running error term are below a certain tolerance

def confident_monte_carlo(tolerance: float):
    pi = 0
    inside = 0
    n = 0
    # going to use a simple running average to characterize the error term
    running_error = deque(maxlen=50)
    for i in range(50):
        running_error.append(sys.maxsize)  # This artifically guarantees that it will take at least 50 iterations,
        # but it think thats fine based on the fixed_monte_carlo method
    while True:
        n += 1
        x = random.random()
        y = random.random()
        if x ** 2 + y ** 2 <= 1:
            inside += 1
        pi = 4 * inside / n
        running_error.append(abs(pi - np.pi))
        if sum(running_error) / len(running_error) <= tolerance:
            break
    return n, pi, sum(running_error) / len(running_error)


def print_time(t0, t1, opt_str: str = None):
    if opt_str is not None: print(opt_str)
    print(f"Elapsed time since last call: {t1 - t0:0.09f} seconds")


if __name__ == "__main__":
    start = time.perf_counter()
    print("Estimate for n = 10, ", fixed_monte_carlo(10))
    print("Estimate for n = 100, ", fixed_monte_carlo(100))
    print("Estimate for n = 1000, ", fixed_monte_carlo(1000))
    print("Estimate for n = 10000, ", fixed_monte_carlo(10000))
    print("Estimate for n = 100000, ", fixed_monte_carlo(100000))
    print("Estimate for n = 1000000, ", fixed_monte_carlo(1000000))
    t = time.perf_counter()
    print_time(start, t)
    start = time.perf_counter()
    print("After running for %d iterations, pi = %f" % first_pi_monte_carlo(0.0001))
    t = time.perf_counter()
    print_time(start, t)
    start = time.perf_counter()
    print("After running for %d iterations, pi = %f, error term = %f" % confident_monte_carlo(0.0001))
    t = time.perf_counter()
    print_time(start, t)
