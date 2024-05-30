"""
    This is how you use this function 
"""
import os 

def addition ( NUMBER1, NUMBER2):
    """
    This is how you use this function 
    e.g addition(2,3)
"""
    print(NUMBER1 + NUMBER2)


def multiplication(NUMBER1,NUMBER2):
    """
    This is how you use this function
    e.g multiplication (2,5)
"""
    print(NUMBER1 * NUMBER2)


def filechecker(FILENAME):
    FILENAME = os.path.isfile(FILENAME)
    print("File exists")
    
def divison(NUMBER1,NUMBER2):
    """
    This is how you use this function
    e.g divison (2,5)
    """
    print(NUMBER1 % NUMBER2)    

def substruction(NUMBER1,NUMBER2):
    """
    This is how you use this function
    e.g substruction (2,5)
    """
    print(NUMBER1 - NUMBER2)        

