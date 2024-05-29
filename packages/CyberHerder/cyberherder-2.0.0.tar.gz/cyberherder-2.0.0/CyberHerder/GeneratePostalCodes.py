import random

def generatePostalCodes(amount):
    postalCodes = []

    while len(postalCodes) < amount:
        postalCode = str(random.randint(1,9))
        
        for num in range(5):
            postalCode += str(random.randint(0,9))
        
        postalCodes.append(postalCode)

    return postalCodes
