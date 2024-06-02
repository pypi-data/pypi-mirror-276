from .file_handlers import open_file, File_AsyncIterator

import re
            
####### No Async Section #######
### Modify uses native re methods... requires access to whole file
### Delete is not really used in practice, sub(pattern, '') is probably more efficient
### Search is written for giggles, the re.search is probably more efficient
class RegexManager:
    def __init__(self, loc = "./supporting/test_patterns.txt"):
        self.compiled_regexes = {}
        self.loc = loc
        
        for line in open_file(self.loc):
            line = line.split(' = ')
            self.add(line[0], line[1])

    def add(self, term, regex, permanent = False):
        try:
            self.compiled_regexes[term] = re.compile(regex)
        except:
            print(f"{term} could not be compiled as a regex: {regex}")

        if permanent:
            with open(self.loc, "a") as appender:
                appender.write(f"{term}~{regex}")

    def remove(self, term):
        lines = open_file(self.loc)
        line_count = len(lines)
        idx = -1
            
        for line_no, line in enumerate(lines):
            if term == line.split('~')[0]:
                idx = lineNo
                break

        if idx != -1:
            with open(self.loc, "w") as writer:
                for line_no in range(line_count):
                    if line_no != idx:
                        writer.write(lines[line_no])
                    if line_no != (line_count - 1):
                        writer.write('\n')
        else:
            print(f"Could not find {term} in file provided")

    def check_if_term_exists(self, term):
        if term not in self.compiled_regexes.keys():
            raise Exception("Term does not exist!")

    def search_file(self, file_loc, term, find_all = False):
        self.check_if_term_exists(term)

        if find_all:
            data = open_file(file_loc, split_lines=False)
            return self.compiled_regexes[term].findall(data)
        else:
            res = {}
            
            for idx, line in enumerate(open_file(file_loc)):
                if (found := self.compiled_regexes[term].findall(line)):
                    res[idx + 1] = found

            return res
            
    async def a_search_file(self, file_loc, term):
        res = {}
        loc = File_AsyncIterator(file_loc, enumerated=True)
        
        async for idx, line in loc:
            if (found := self.compiled_regexes[term].findall(line)):
                res[idx] = found
                
        return res
        
    # write_to_file = replace file with new contents
    def modify_file(self, file_loc, term, option, pattern, write_to_file = False):
        self.check_if_term_exists(term)
        options = ['split', 'sub', 'subn']
        
        if option not in options:
            raise Exception(f"Need to choose one of the following options {options}")

        data = open_file(file_loc, split_lines = False)

        if option == 'split':
            res = self.compiled_regexes[term].split(pattern, data)
        elif option == 'sub':
            res = self.compiled_regexes[term].sub(pattern, data)
        else:
            res = self.compiled_regexes[term].subn(pattern, data)

        return res
        
if __name__ == "__main__":
    regex_manager = RegexManager()
    
    print(regex_manager.search_file('./supporting/test_file.txt', 'phoneNumberPattern'))
    # print(regex_manager.search_file('./supporting/test_file.txt', 'phoneNumberPattern', find_all=True))
    
    import asyncio
    
    async def main():
        print(await regex_manager.a_search_file('./supporting/test_file.txt', 'phoneNumberPattern'))
        
    asyncio.run(main())
