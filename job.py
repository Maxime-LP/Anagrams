import multiprocessing as mp
from collections import Counter, defaultdict
from time import time

def isAnagramme(word1,word2):
    return Counter(word1) == Counter(word2)

def words():
    output = set()
    with open('words','r') as file:
        for line in file:
            output.add(line.replace('\n','').lower())
    return output

words_set = words()
words_by_length = defaultdict(set)
for word in words_set:
    words_by_length[len(word)].add(word)

def dispatcher(nb_of_processes):
    #dispatch les mots en ensembles de même taille
    N = len(words_set)
    target_interval_number_of_words = int(N/nb_of_processes)
    words_max_length = max(words_by_length.keys())
    intervals = []
    sup_bound = 1
    while sup_bound<=words_max_length:
        inf_bound = sup_bound
        current_number_of_words = 0
        while current_number_of_words<target_interval_number_of_words and sup_bound<=words_max_length:
            current_number_of_words += len(words_by_length[sup_bound])
            sup_bound+=1
        intervals.append([inf_bound,sup_bound])
    return intervals

class job(mp.Process):
    def __init__(self,id_n,nb_of_processes,queue):
        mp.Process.__init__(self)
        self.id_n = id_n
        
        self.interval = dispatcher(nb_of_processes)[id_n-1]

        self.queue = queue
        self.dict = defaultdict(set)

    def run(self):
        for length in range(self.interval[0],self.interval[1]):
            while words_by_length[length]:
                print(self.id_n,len(words_by_length[length]))
                word1 = words_by_length[length].pop()
                aux = words_by_length[length].copy()

                for word2 in aux:
                    if isAnagramme(word1,word2) and word1!=word2:
                        self.dict[word1].add(word2)
                        words_by_length[length].discard(word2)

        self.queue.put(self.dict)
