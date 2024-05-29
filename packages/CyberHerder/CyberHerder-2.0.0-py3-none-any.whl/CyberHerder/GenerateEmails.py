import random
from .GenerateUsernames import generateUsernames

tld = ['.org', '.edu', '.com']
domain = ["sigcryptal", "cybersploit", "libertycrypto"]

def generateEmails(amount: int) -> list:
    usernames = generateUsernames(amount)
    return [usernames[idx] + '@' + domain[random.randint(0,len(domain)-1)] + tld[random.randint(0,len(tld)-1)] for idx in range(amount)]
