import random

def generateUsernames(amount):
    with open("/usr/wordlists/SecLists/Usernames/Names/familynames-usa-top1000.txt", "r") as reader:
        usernames = reader.read().strip().split('\n')
        length = len(usernames) - 1
        names = []

        for idx in range(amount):
            names.append(usernames[random.randint(0, length)])

        return names
