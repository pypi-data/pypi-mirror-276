from random import randint

class UUID:
    hexMap = {idx: str(idx) for idx in range(10)}
    hexMap[10] = 'a'
    hexMap[11] = 'b'
    hexMap[12] = 'c'
    hexMap[13] = 'd'
    hexMap[14] = 'e'
    hexMap[15] = 'f'

    def __init__(self, version = 4, n = 4):
        if version > 4 or version < 0:
            raise Exception("Version outside the range!")

        if n > 15 or n < 0:
            raise Exception("Variant amount is outside the range!")

        self.n = n
        self.version = version
        self.uuid = ""

    def getHexRange(self, num):
        return "".join(self.getNextHex() for _ in range(num))

    def getUuid(self):
        result = self.getHexRange(8) + "-" + self.getHexRange(4)
        result += "-" + self.getNextHex(bitsLeft = 0, val = self.version) + self.getHexRange(3)
        
        bitAmount = self.n
        count = 1
        while bitAmount > 1:
            bitAmount >>= 1
            count += 1

        result += "-" + self.getNextHex(bitsLeft = 4 - count, val = self.n) + self.getHexRange(3)
        result += "-" + self.getHexRange(12)

        return result

    def str2Hex(self, binString):
        hexString = ""

        for idx in range(0, len(binString), 4):
            hexString += self.hexMap[int(binString[idx:idx+4], 2)]

        return hexString

    def getNextHex(self, bitsLeft = 4, val = -1):
        binString = "".join([str(randint(0, 1)) for _ in range(bitsLeft)])
        if val != -1:
            binString = bin(val)[2:] + binString
        return self.str2Hex(binString)

### - Collection -> sized, iterable, container
class UUID_Handler:
    # Variant 4 -> access to all four bits in N encoding
    # N must be less than 16
    def __init__(self, amount = 10, version = 4, n = 1):
        try:
            self.uuidObj = UUID(version = version, n = n)
        except Exception as e:
            raise Exception(e.str)

        self.amount = amount
        
    def __iter__(self):
        return self

    def __next__(self):
        if self.amount:
            self.amount -= 1
            return self.uuidObj.getUuid()
        else:
            raise StopIteration()
    
class Controlled_UUID:
    uuids_given = {}
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Controlled_UUID, cls).__new__(cls)
        return cls.instance
        
    def get_uuid(self):
        new, res = False, False
        
        while not new:
            res = UUID().getUuid()
            
            try:
                self.uuids_given[res]
            except:
                new = True
                self.uuids_given[res] = True
        
        return res
        
def get_new_uuid() -> str:
    return Controlled_UUID().get_uuid()
    
if __name__ == "__main__":
    print(get_new_uuid())
    
    print(Controlled_UUID().get_uuid())
    
    print(Controlled_UUID.uuids_given.keys())
