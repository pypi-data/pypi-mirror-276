import re

class CyberValidator:
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
    
    gpsPattern = r"^[\(][+|-]?((90)(\.[0]+)?|(([1-8]?[0-9])(\.\d+)?)),\s[+|-]?((180)(\.[0]+)?|(([1][0-7][0-9])|([1-9]?[0-9]))(\.\d+)?)[\)]$"
    
    options = ["IPv4", "IPv6", "MAC-eui48", "MAC-eui64", "Phone", "Postal Code", "Credit Card", "UID", "GPS"]

    @classmethod
    def terminateProtocol(cls, option: str, data: str):
        if option not in cls.options:
            raise Exception("Not an option, the T-900 does not compute!")

        idx = cls.options.index(option)

        if idx == 0 or idx == 1:
            return not cls.validateIP(option, data)
        elif idx == 2 or idx == 3:
            return not cls.validateMAC(data)
        elif idx == 4:
            return not cls.validatePhone(data)
        elif idx == 5:
            return not cls.validateZip(data)
        elif idx == 6:
            return not cls.validateCreditCard(data)
        elif idx == 7:
            return not cls.validateUID(data)
        else:
            return not cls.validateGPS(data)

    @classmethod
    def validateUID(cls, uid: str) -> bool:
        if re.search(cls.uidPattern, uid):
            return True
        return False
    
    @classmethod
    def validateGPS(cls, data) -> bool:
        if re.search(cls.gpsPattern, data):
            return True
        return False

    @classmethod
    def validateMAC(cls, data):
        if re.search(cls.Mac48, data) or re.search(cls.Mac64, data):
            return True
        else:
            return False
            
    @classmethod
    def validateEmail(cls, email: str) -> bool:
        if re.search(cls.emailPattern, email):
            return True
        return False 

    @classmethod
    def validateCreditCard(cls, card: str) -> bool:
        if re.search(cls.creditCardPattern2, card):
            return False
        elif re.search(cls.creditCardPattern, card):
            return True
        return False

    @classmethod
    def validateZip(cls, zipCode: str) -> bool:
        if re.search(cls.zipCodePattern, zipCode) and not re.search(cls.zipCodePattern2, zipCode):
            return True
        return False

    @classmethod
    def validatePhone(cls, phoneNumber: str) -> bool:
        if re.search(cls.phoneNumberPattern, phoneNumber):
            return True
        return False

    @classmethod
    def validateIP(cls, option: str, ip: str) -> bool:
        if (option == "IPv4" and re.search(cls.ipv4Pattern, ip)) or (option == "IPv6" and re.search(cls.ipv6Pattern, ip)):
            return True
        return False

def terminate(option: str, data: str) -> bool:
    return CyberValidator.terminateProtocol(option, data)
    
if __name__ == "__main__":
    print(f'Terminate 1012345890: {terminate("Phone", "1012345890")}')
    print(f'Terminate 101: {terminate("Phone", "101")}')
