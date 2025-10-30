"""
Back-off Decorator: a program that implements exponential backoff with decorators to simulate a strategy for handling
retries of failed network calls
By: Autumn Peterson
Date: 10 March 2023
"""
# Coded with GitHub Copilot; however, it proved to be not super helpful with this one

from random import randint
from time import sleep, asctime


def backoff(initial_delay: float, back_off_factor: float, max_delay: float) -> callable:
    """decorator that implements exponential backoff"""

    def outer(func: callable) -> callable:
        delay = 0  # delay starts at 0 and is in outer scope for inner to access

        def inner(*args, **kwargs):  # accepts whether shaky service is True or False
            nonlocal delay
            if func(*args, **kwargs):  # Every True call from shaky_call_service() resets delay to 0 and returns None
                delay = 0
                oof = None
                return f"{asctime()} will be calling after {oof} sec delay\n True"
            else:
                delay = (delay * back_off_factor) + initial_delay
                sleep(delay)
                if delay > max_delay:
                    delay = max_delay
                return f"{asctime()} will be calling after {delay} sec delay\n False"

        return inner

    return outer


@backoff(initial_delay=0.1, back_off_factor=1.5, max_delay=4.0)  # easily changeable factors for backoff
def call_shaky_service():
    return 6 == randint(1, 6)


while True:
    print(call_shaky_service())  # Simulates strategy for handling retries of failed network calls
