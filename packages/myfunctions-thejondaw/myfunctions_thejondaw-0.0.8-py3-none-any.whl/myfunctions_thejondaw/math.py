"""
    This is how you use this function
"""

import os

def addition(NUMBER1,NUMBER2):
    """
    This is docs
    """
    print(NUMBER1 + NUMBER2)
    
def multiplication(NUMBER1,NUMBER2):
    """
    This is docs2
    """
    print(NUMBER1 * NUMBER2)

def filechecker(FILENAME):
    FILENAME = os.path.isfile(FILENAME)
    print("File exists")
    