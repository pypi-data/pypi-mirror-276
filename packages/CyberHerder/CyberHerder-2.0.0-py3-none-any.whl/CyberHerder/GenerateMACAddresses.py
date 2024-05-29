import random

def pad(string, length):
    while len(string) < length:
        string = "0" + string
    return string
    
def generateMACaddresses(amount, eui48 = True, padding = True):
    macs = []
    # Supposed to be + 2
    extendedLength = 0 if eui48 == True else 1
    for x in range(amount):
        mac = ""
        # This is supposed to be + 2
        for x in range(3+extendedLength):
            for y in range(2):
                if padding == True:
                    mac += pad(hex(random.randint(0,255))[2:], 2) + "-"
                else:
                    mac += hex(random.randint(0,255))[2:] + "-"
        macs.append(mac[:-1])
    return macs
