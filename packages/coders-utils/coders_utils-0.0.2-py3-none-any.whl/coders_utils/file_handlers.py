from aiofile import async_open as a_open

# options = r, a, w
# more sophisticated replacements later
def open_file(file_loc, split_lines = True, option = "r", new_text = ""):
    if option not in ["r", "a", "w"]:
        raise Exception("File option not supported")

    if option == "r":
        try:
            with open(file_loc) as reader:
                data = reader.read().strip()
                if split_lines:
                    return data.split("\n")
                else:
                    return data
        except:
            raise Exception("Could not open file: {fileLoc}!")
    else:
        try:
            with open(file_loc, option) as writer:
                writer.write(new_text)
        except:
            raise Exception("Could not modify file: {fileLoc}!")
            
def verify_folder(file_loc):
    return file_loc if file_loc[-1] == "/" else file_loc + "/"
            
class File_Iterator:
    def __init__(self, location, enumerated: bool = False, fxn_ptr = None):
        with open(location) as reader:
            self.data = reader.read().strip().split('\n')
        
        self.index = 0
        self.length = len(self.data)
        self.enumerated = enumerated
        self.fxn_ptr = fxn_ptr
        
        if self.enumerated:
            self.line = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        ans = found = False
        
        while not found and self.index < self.length:
            if self.enumerated:
                self.line += 1
                
            match self.fxn_ptr:
                case True:
                    if self.fxn_ptr( (value := self.data[self.index]) ):
                        found = True
                        ans = value
                case _:
                    if (value := self.data[self.index]):
                        found = True
                        ans = value
                        
            self.index += 1
            
        if self.index >= self.length and not found:
            raise StopIteration()
        
        return ans if not self.enumerated else self.line, ans
        
class File_AsyncIterator:
    def __init__(self, location, enumerated: bool = False, fxn_ptr = None):
        self.location = location
        self.file = None
        self.enumerated = enumerated
        self.fxn_ptr = fxn_ptr
        
        if self.enumerated:
            self.line = 0
        
    async def read_line(self):
        return await self.file.readline()
        
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.file == None:
            self.file = await a_open(self.location)

        while (val := await self.read_line()).strip():
            if self.enumerated:
                self.line += 1
            
            found = None
            
            match self.fxn_ptr:
                case True:
                    if self.fxn_ptr(val):
                        found = True
                case _:
                    found = True
                    
            if found:
                return val if not self.enumerated else self.line, val
                
        raise StopAsyncIteration
        
if __name__ == "__main__":
    import asyncio
    
    
    class Get_Users_Async:
        def __aiter__(self):
            return File_AsyncIterator('/etc/group')
        
    async def main():
        async for item in Get_Users_Async():
            print(item) # display_item(item)
            
    asyncio.run(main())
    
    ### Chicken and the egg problem below
    def check_valid_group(item):
        try:
            if int((val := item.split(':'))[2]) >= 1000 and val[0] != 'nogroup':
                return True
        except:
            pass
        
        return False
        
    import subprocess

    def shell(string):
        return subprocess.run(string, capture_output=True, shell=True)
        
    def shell_extract(string, _return=True):
        ret = shell(string)
        
        if _return:
            return ret.stdout.decode().strip()
        
    def check_associated_groups(username):
        try:
            return shell_extract(f'groups {username}').split(' : ')[1]
        except:
            return 'NONE'

    def display_item(item):
        try:
            username, password, uid, _ = item[0].split(':')
        except:
            username = item

        print(f'{ username } is associated with the following groups: { check_associated_groups(username) }')
        
    print("Trying Sync")
    class Get_Users:
        def __iter__(self):
            return File_Iterator('/etc/group', fxn_ptr=check_valid_group)
        
    for item in Get_Users():
        display_item(item)
    
    print("\nTrying Async")
    class Get_Users_Async:
        def __aiter__(self):
            return File_AsyncIterator('/etc/group', fxn_ptr=check_valid_group)
        
    async def main():
        async for item in Get_Users_Async():
            display_item(item)
            
    asyncio.run(main())
