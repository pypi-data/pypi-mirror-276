def generateIPv6Addresses(amount):
    import random
    examples = []
    dictionary = {10:'a', 11:'b', 12:'c', 13:'d', 14:'e', 15:'f'}
    for i in range(amount):
        temp = ""
        for x in range(8):
            section = ""
            for y in range(random.randint(1,4)):
                character = random.randint(0,15)
                if character > 9:
                    character = dictionary[character]
                section += str(character)
            temp += section + ":"
        examples.append(temp[:-1])
    return examples