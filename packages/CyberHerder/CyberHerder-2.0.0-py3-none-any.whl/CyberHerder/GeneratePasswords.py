import random

def generatePasswords(amount):
    with open("/usr/wordlists/SecLists/Passwords/Common-Credentials/10-million-password-list-top-1000.txt", "r") as reader:
        passwords = reader.read().strip().split('\n')
        length = len(passwords) - 1
        passes = []

        for idx in range(amount):
            passes.append(passwords[random.randint(0, length)])

        return passes
