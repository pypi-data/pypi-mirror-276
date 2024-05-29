from time import time

import os
import re
import multiprocessing as mp

class Search:
    def __init__(self, patterns, patternThreshold, fileOptions, optionThreshold):
        self.patternThreshold = patternThreshold
        self.optionThreshold = optionThreshold
        self.patterns = patterns
        self.optionsList = ["st_mode","st_ino","st_dev","st_nlink","st_uid","st_gid","st_size","st_atime","st_mtime","st_ctime","st_atime_ns","st_mtime_ns","st_ctime_ns","st_blocks","st_rdev","st_flags"]
        self.fileOptions = fileOptions
        self.optionLength = len(self.fileOptions.keys())

    def accept(self, path: str):
        attributes = os.stat(path)
        score = 0
        
        for key, val in self.fileOptions.items():
            idx = self.optionsList.index(key)
            option = val[0]
            number = float(val[1])
            
            if option == ">":
                if attributes[idx] > number:
                    score += 1
            elif option == ">=":
                if attributes[idx] >= number:
                    score += 1
            elif option == "==":
                if int(attributes[idx]) == int(number):
                    score += 1
            elif option == "<":
                if attributes[idx] < number:
                    score += 1
            else:
                if attributes[idx] <= number:
                    score += 1
        
        if ( (score / length) * 100 ) >= self.optionThreshold:
            return True
        
        return False

    def match(self, path: str):
        try:
            count = 0
            length = len(self.patterns)
            for pattern in self.patterns:
                if re.search(pattern, path):
                        count += 1

                if ( (count/length) * 100) >= self.patternThreshold:
                    add = True
                    if len(self.fileOptions):
                        if not self.accept(path):
                            add = False
                    if add:
                        return path
        except:
            print(f"Permission denied for {path}")
        return None
        
class Find(Search):
    def __init__(self, path, patterns = [repr('.*')], patternThreshold = 100, fileOptions = {}, optionThreshold = 100, ignoreHidden = True):
        super().__init__(patterns, patternThreshold, fileOptions, optionThreshold)
        self.files = []
        self.dirSearch(path)

    def dirSearch(self, path):
        try:
            for item in os.listdir(path):
                if item[0] == ".":
                    continue
                    
                itemPath = os.path.join(path, item)

                if os.path.isdir(itemPath):
                    self.dirSearch(itemPath)
                else:
                    self.files.append(itemPath)
        except:
            print(f"Permission denied for {path}")

    def fasterDirSearch(self, top):
        for entry in os.scandir(path):
            pass

    def __call__(self):
        nproc = mp.cpu_count()
        
        with mp.Pool(nproc) as pool:
            processes = [pool.apply_async(self.match, args=(self.files[idx],)) for idx in range(len(self.files))]
            results = list(filter(lambda x: x != None, [p.get() for p in processes]))
            return results
            
if __name__ == "__main__":
    start = time()
    find = Find("/home/parzival/Desktop/Packages/", patterns = ["^.*[.]py$"], patternThreshold = 100, ignoreHidden = True)
    res = find()
    print(f"{ len(res) } files found in { time() - start }")
