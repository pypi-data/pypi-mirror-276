from .generator import generate
import PenguinServices as ps

class DataBreach:
    def __init__(self, num: int, destinationFolder: str):
        self.folder = destinationFolder if destinationFolder[-1] == "/" else destinationFolder + "/"
        self.creditCardFile = self.folder + "creditCards.txt"
        self.deviceFile = self.folder + "devices.txt"
        self.peopleFile = self.folder + "people.txt"
        self.amount = int(num)

        if self.amount > 1000:
            self.amount = 1000

        # PenguinServices MAKE FOLDER LATER
        if ps.makeFolder(self.folder) != True:
            raise Exception("Could not create the folder!")

        try:
            self.passwords = generate("Passwords", self.amount)
            self.usernames = generate("Usernames", self.amount)
        except:
            raise Exception("Have to download SecLists and install the required packages!!!")

        self.create()

    def createCreditCards(self) -> None:
        with open(self.creditCardFile, "w") as _file:
            cards = generate("Credit Cards", self.amount)
            pins = generate("Pins", self.amount)

            _file.write("Name\tCredit Card Information\tPin Number\n")
    
            for idx in range(self.amount):
                _file.write(self.usernames[idx] + "\t" + cards[idx] + "\t" + pins[idx] + "\n")

    def createDevices(self) -> None:
        deviceIPv4s = generate("IPv4", self.amount)
        deviceIPv6s = generate("IPv6", self.amount)
        deviceMAC48 = generate("MAC-eui48", self.amount)
        deviceMAC64 = generate("MAC-eui64", self.amount)  

        with open(self.deviceFile, "w") as _file:
            _file.write("IPv4\tIPv6\tMAC-48\tMAC-64\tBIOS Password\n")

            for idx in range(self.amount):           
                _file.write(deviceIPv4s[idx] + "\t" + deviceIPv6s[idx] + "\t" + deviceMAC48[idx] + "\t" + deviceMAC64[idx] + "\t" + self.passwords[idx] +  "\n")        

    def createPeople(self) -> None:
        phones = generate("Phones", self.amount)
        uids = generate("UIDs", self.amount)
        zipCodes = generate("Postal Codes", self.amount)
        companies = generate("Companies", self.amount)
        emails = generate("Emails", self.amount)
        
        with open(self.peopleFile, "w") as _file:
            _file.write("Username\tCompany\tPhone Number\tUID\tZip Code\tEmail\n")

            for idx in range(self.amount):
                _file.write(self.usernames[idx] + "\t" + companies[idx] + "\t" + phones[idx] + "\t" + uids[idx] + "\t" + zipCodes[idx] + "\t" + emails[idx] + "\n")

    def create(self):
        self.createCreditCards()
        self.createDevices()
        self.createPeople()

def dataBreach(amount: int = 1000, dest: str = "./BreachedData") -> bool:
    try:
        DataBreach(amount, dest)
    except Exception as e:
        print(str(e))
        return False
    return True
