import random

def generateCreditCards(amount):
    creditCards = []

    while len(creditCards) < amount:
        creditCards.append("".join([str(random.randint(0,9)) for num in range(16)]))

    return creditCards
