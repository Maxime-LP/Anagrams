import multiprocessing as mp
from collections import defaultdict

class job(mp.Process):
    def __init__(self,id_n,words,queue):
        mp.Process.__init__(self)
        self.id_n = id_n
        self.words = words
        self.queue = queue
        self.dict = defaultdict(set)
        self.running = False

    def run(self):
        self.running = True
        for word in self.words:
            letters = ''.join(sorted(word))
            self.dict[letters].add(word)

        self.queue.put(self.dict)
        self.running = False      
