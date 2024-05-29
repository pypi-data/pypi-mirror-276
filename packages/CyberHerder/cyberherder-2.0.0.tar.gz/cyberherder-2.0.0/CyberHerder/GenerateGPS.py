import random

def generateGPS(amount):
    coords = []

    for _ in range(amount):
        _lat = random.randint(-90, 90)
        _long = random.randint(-180, 180)
        firstSign = "+" if _lat >= 0 else ""
        secondSign = "+" if _long >= 0 else ""

        coords.append(f"({firstSign}{_lat},{secondSign}{_long})")

    return coords
