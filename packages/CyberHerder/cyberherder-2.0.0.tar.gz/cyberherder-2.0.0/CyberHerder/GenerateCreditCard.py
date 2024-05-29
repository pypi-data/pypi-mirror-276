import random

def generateCreditCards(amount):
    creditCards = []

    while len(arr) < amount:
        creditCards.append("".join([str(random.randint(0,9)) for num in range(16)]))

    return creditCards
