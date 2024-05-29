import re

class Validator:
    uidPattern = r'^[0-9a-zA-Z]{10}$'

    Mac48 = r'^([0-9A-Fa-f]{2}[.:-]){5}[0-9A-Fa-f]{2}$'
    Mac64 = r'^([0-9A-Fa-f]{2}[.:-]){7}[0-9A-Fa-f]{2}$'
    
    emailPattern = r'^<[a-zA-Z]{1}([\w\-.])+@[a-zA-Z]{2,}\.[a-zA-Z]{1,3}>$'
    
    creditCardPattern = r'^[456][0-9]{3}[-]?[0-9]{4}[-]?[0-9]{4}[-]?[0-9]{4}$'
    creditCardPattern2 = r'([0-9])\1{3,}'

    zipCodePattern = r"^[1-9][0-9]{5}$"
    zipCodePattern2 = r"(\d)(?=\d\1)"

    phoneNumberPattern = r'^[0-9]{10}$'

    ipv4Pattern = r'^((([1]?[1-9]?[0-9])|([2][0-4][0-9])|([2][0-5][0-5])|([1][0-9][0-9])).){3}(([1]?[1-9]?[0-9])|([2][0-4][0-9])|([2][0-5][0-5])|([1][0-9][0-9]))$'
    ipv6Pattern = r'^([0-9a-fA-F]{1,4}[:]){7}[0-9a-fA-F]{1,4}$'

    gpsPattern = r"^[\(][+|-]?(((90)(\.[0]+)?)|([0-8]?\d(\.\d+)?)),[\s]*[+|-]?(((180)(\.[0]+)?)|(([1][0-7][0-9](\.\d+)?)|([1-9]?[0-9](\.\d+)?))[\)]$"
    
    options = ["IPv4", "IPv6", "MAC-eui48", "MAC-eui64", "Phone", "Postal Code", "Credit Card", "UID"]

    def __init__(self):
        pass

    def protocol(self, option: str, data: str):
        if option not in self.options:
            raise Exception("Not an option, the T-900 does not compute!")

        idx = self.options.index(option)

        if idx == 0 or idx == 1:
            return self.validateIP(option, data)
        elif idx == 2 or idx == 3:
            return self.validateMAC(data)
        elif idx == 4:
            return self.validatePhone(data)
        elif idx == 5:
            return self.validateZip(data)
        elif idx == 6:
            return self.validateCreditCard(data)
        else:
            return self.validateUID(data)

    def validateUID(self, uid: str) -> bool:
        if re.search(self.uidPattern, uid):
            return True
        return False

    def validateMAC(self, data):
        if re.search(self.Mac48, data) or re.search(self.Mac64, data):
            return True
        else:
            return False

    def validateEmail(self, email: str) -> bool:
        if re.search(self.emailPattern, email):
            return True
        return False 

    def validateCreditCard(self, card: str) -> bool:
        if re.search(self.creditCardPattern2, card):
            return False
        elif re.search(self.creditCardPattern, card):
            return True
        return False

    def validateZip(self, zipCode: str) -> bool:
        if re.search(self.zipCodePattern, zipCode) and not re.search(self.zipCodePattern2, zipCode):
            return True
        return False

    def validatePhone(self, phoneNumber: str) -> bool:
        if re.search(self.phoneNumberPattern, phoneNumber):
            return True
        return False

    def validateIP(self, option: str, ip: str) -> bool:
        if (option == "IPv4" and re.search(self.ipv4Pattern, ip)) or (option == "IPv6" and re.search(self.ipv6Pattern, ip)):
            return True
        return False

    def validateGPS(self, gpsCoords):
        if re.search(gpsPattern, gpsCoords):
            return True
        return Falsei

    def closeToPoint(self, longitude, latitude, longitude2, latitude2):
        lat1, lon1 = latitude, longitude
        lat2, lon2 = latitude2, longitude2

        degrees_to_radians = math.pi / 180.0

        phi1 = (90.0 - lat1) * degrees_to_radians
        phi2 = (90.0 - lat2) * degrees_to_radians
        
        theta1 = lon1 * degrees_to_radians
        theta2 = lon2 * degrees_to_radians

        cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) + math.cos(phi1) * math.cos(phi2))
        arc = math.acos(cos)
	
        distance_between_points = arc * 6371

        return distance_between_points < 260

def valid(option: str, data: str) -> bool:
    regexer = Validator()
    return regexer.protocol(option, data)

def terminate(option: str, data: str) -> bool:
    return not valid(option, data)
