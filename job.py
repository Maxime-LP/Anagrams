import multiprocessing as mp
from collections import defaultdict

class job(mp.Process):
    def __init__(self,id_n,words,queue):
        mp.Process.__init__(self)
        self.id_n = id_n
        self.words = words
        self.queue = queue
        self.dict = defaultdict(set)

    def run(self):
        for word in self.words:
            letters = ''.join(sorted(word))
            self.dict[letters].add(word)

        self.dict = {key: val for key, val in self.dict.items()}
        self.queue.put(self.dict)
        print(self.id_n,'terminé') 
        self.terminate()      
