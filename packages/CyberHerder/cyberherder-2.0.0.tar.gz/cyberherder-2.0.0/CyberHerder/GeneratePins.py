import random

def generatePins(amount):
    return ["".join([str(random.randint(0,9)) for _ in range(6)]) for _ in range(amount)]
