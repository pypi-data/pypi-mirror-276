from aiofiles import open as async_open

class File_Iterator:
    def __init__(self, location, validation_ptr=None):
        with open(location) as reader:
            self.data = reader.read().strip().split('\n')
        
        self.validation_ptr = validation_ptr
        self.index = 0
        self.length = len(self.data)
        
    def __iter__(self):
        return self
    
    def __next__(self):
        ans = found = False
        while not found and self.index < self.length:
            value = self.data[self.index]
            ans = value
            
            if self.validation_ptr:
                if self.validation_ptr(value):
                    found = True
            else:
                found=True
            self.index += 1
            
        if self.index >= self.length and not found:
            raise StopIteration()
        
        return ans
     
class File_AsyncIterator:
    def __init__(self, location, validation_ptr=None):
        self.location = location
        self.file = None
        self.validation_ptr = validation_ptr
        
    async def read_line(self):
        return await self.file.readline()
        
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.file == None:
            self.file = await async_open(self.location)

        while (val := await self.read_line()).strip():
            if self.validation_ptr:
                if self.validation_ptr(val):
                    return val
            else:
                return val
                
        raise StopAsyncIteration
            
if __name__ == "__main__":
    import asyncio
    
    from .linux_admin_ops import *
    
    print("Trying Sync")
    class Get_Users:
        def __iter__(self):
            return File_Iterator('/etc/group', validation_ptr=check_valid_group)
        
    for item in Get_Users():
        display_item(item)
    
    print("\nTrying Async")
    class Get_Users_Async:
        def __aiter__(self):
            return File_AsyncIterator('/etc/group', validation_ptr=check_valid_group)
        
    async def main():
        async for item in Get_Users_Async():
            display_item(item)
            
    asyncio.run(main())
