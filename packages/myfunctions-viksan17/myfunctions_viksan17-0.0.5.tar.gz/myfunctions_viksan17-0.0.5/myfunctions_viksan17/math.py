"""
    This is how you use this function.
"""
import OS

def addition(NUMBER1,NUMBER2):
    print(NUMBER1 + NUMBER2)
    """
    This is how you use this function.
    e.g addition(2,3)
    """


def multiplication(NUMBER1, NUMBER2):
    print(NUMBER1 * NUMBER2)
    """
    This is how you use this function.
    e.g multiplication(2,5)
    """

def filechecker(FILENAME):
    FILENAME=os.path.isfile(FILENAME)
    print("File Exists")