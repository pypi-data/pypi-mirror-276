import random

companies = ["Sigcryptal", "Cybersploit", "Liberty-Crypto"]

def generateCompanies(amount):
    return [companies[random.randint(0,len(companies)-1)]  for _ in range(amount)]
