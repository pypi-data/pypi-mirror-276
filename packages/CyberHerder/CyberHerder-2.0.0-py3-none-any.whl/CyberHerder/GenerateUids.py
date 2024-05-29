import random

def generateUids(amount):
    uids = []

    while len(uids) < amount:
        pool = [chr(num) for num in range(48, 123) if num not in [58,59,60,61,62,63,64,91,92,93,94,95,96]]
        
        uid = ""
        
        while len(uid) < 10:
            idx = random.randint(0,len(pool)-1)
            uid += str(pool[idx])
            del pool[idx]

        uids.append(uid)

    return uids
