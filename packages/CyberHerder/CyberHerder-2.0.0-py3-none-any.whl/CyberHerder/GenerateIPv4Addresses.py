def stripLeadingZeros(string):
    while len(string) > 1 and string[0] == '0':
        string = string[1:]
    return string

def generateIPv4Addresses(amount):
    import random
    examples = []
    for i in range(amount):
        temp = ""
        for x in range(4):
            section = ""
            for y in range(random.randint(1,3)):
                if section == "":
                    character = random.randint(0,2)
                elif section[0] == '2' and len(section) == 1:
                    character = random.randint(0,5)
                elif section[0] == '2' and section[1] == '5':
                    character = random.randint(0,5)
                else:
                    character = random.randint(0,9)
                section += str(character)
            temp += stripLeadingZeros(section) + "."
        examples.append(temp[:-1])
    return examples