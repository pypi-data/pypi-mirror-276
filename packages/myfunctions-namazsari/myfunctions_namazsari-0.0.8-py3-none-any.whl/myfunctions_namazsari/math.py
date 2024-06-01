"""
    this is how you use this function
"""

import os

def addition(NUMBER1,NUMBER2):
    print(NUMBER1 + NUMBER2)


def multiplication(NUMBER1,NUMBER2):
    """
    this is how you use this function
    e.g multiplication(2,5)
    """
    print(NUMBER1 * NUMBER2)


def filechecker(FILENAME):
    FILENAME = os.path.isfile(FILENAME)
    print("file exist")