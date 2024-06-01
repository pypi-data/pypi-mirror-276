"""
This is how you use function
"""
import os

def addition(NUMBER1,NUMBER2):
    """
    This is how you use function
    e.g addition(2,3)
    """
    print(NUMBER1 + NUMBER2)

def multiplication(NUMBER1,NUMBER2):
    """
    This is how you use function
    e.g multiplication(2,5)
    """
    print(NUMBER1 * NUMBER2)

def division(NUMBER1,NUMBER2):
    """
    This is how you use function
    e.g division(2,5)
    """
    print(NUMBER1 / NUMBER2)

def subscription(NUMBER1,NUMBER2):
    """
    This is how you use function
    e.g subscription(10-5)
    """
    print(NUMBER1 - NUMBER2)

def filechecker(FILENAME):
    FILENAME = os.path.isfile(FILENAME)
    print("File Exiests")
