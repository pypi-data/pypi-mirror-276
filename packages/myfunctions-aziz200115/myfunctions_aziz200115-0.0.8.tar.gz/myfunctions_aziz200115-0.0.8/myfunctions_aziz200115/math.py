"""
    This is how you use this function
"""

import os


def addition(NUMBER1,NUMBER2):
    """
    This is how you use this function
    e.g. addition(2,3)
    """
    print(NUMBER1 + NUMBER2) 


def multiplication(NUMBER1,NUMBER2):
    """
    This is how you use this function
    e.g. multiplication(2,3)
    """
    print(NUMBER1 * NUMBER2) 


def division(NUMBER1,NUMBER2):
    """
    This is how you use this function
    e.g. division(2,3)
    """
    print(NUMBER1 / NUMBER2) 


def subtraction(NUMBER1,NUMBER2):
    """
    This is how you use this function
    e.g. subtraction(2,3)
    """
    print(NUMBER1 - NUMBER2) 


def filechecker(FILENAME):
    FILENAME = os.path.isfile(FILENAME)
    print("File exists")

