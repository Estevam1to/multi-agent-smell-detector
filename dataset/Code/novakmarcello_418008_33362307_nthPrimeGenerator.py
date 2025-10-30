# Disclaimer: GitHub Copilot was used for this program
# Created by Marcello Novak, 1/29/2023, CS 399
# Description: Tests if a given nth number is prime, and equal to a test value

# Import square root for prime function
# Import process time for timing
from math import sqrt
from time import process_time


# Function to check if a number is prime
def isPrime(n):
    if n < 2:
        return False
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


# Generator function to generate prime numbers
def primeGenerator():
    n = 1
    while True:
        n += 1
        if isPrime(n):
            yield n


if __name__ == '__main__':
    # All the below code was taken from the "Programming Assignment Clarification" discussion on Canvas
    # Just a test to see if the nth prime number is correct, and how long it takes to run
    # Testing if the nth number is prime (1,000,000th prime number is 15485863)
    knownPrime = (1000000, 15485863)

    # Start timer
    t0 = process_time()

    # Generate prime numbers
    primes = primeGenerator()

    # Check if the nth prime number is correct
    for k, prime in enumerate(primes, 1):
        if k == knownPrime[0]:
            print(f"The {k:,}th prime number is {prime}")
            assert prime == knownPrime[1]
            primes.close()

    # Stop timer and print time elapsed
    print("Time elapsed: ", round((process_time() - t0), 2), " seconds")
