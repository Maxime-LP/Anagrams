from collections import defaultdict
from time import time,sleep
import multiprocessing as mp
from job import job
from preprocessing import preprocessing, dispatcher

if __name__ == '__main__':   
    t0 = time()

    file_path = 'words'
    nb_of_processes = 2
    queue = mp.Queue()
    TotalWords, words_by_length = preprocessing(file_path)
    min_length = 2
    intervals = dispatcher(min_length,nb_of_processes, TotalWords, words_by_length)
    
    tasks = set()
    for id_n in range(1,nb_of_processes+1):  #a simplifier
        interval = intervals[id_n-1]
        words = set()
        for length in range(interval[0],interval[1]) :
            words.update(words_by_length[length])
        tasks.add(job(id_n,words,queue))

    for task in tasks:
        task.start()
    sleep(2)
    #pb avec le join
    """for task in tasks:
        task.join()"""

    output_dict = {}
    while not queue.empty():
        local_dict = queue.get()
        output_dict.update(local_dict)

    output = output_dict.values() #list((key : {set of anagrams of key}))
    count_groups = defaultdict(int)
      
    with open('log.txt','w') as log:
        for group in output:
            count_groups[len(group)]+=1
            log.write(f"{','.join(group)} \n")
        
    for length,nb in sorted(count_groups.items(),key=lambda x:x[0]):
        print(f"{nb} ensembles de {length} anagrames")
    
    with open('log.txt','w') as log:
        log.write(f"Temps d'exécution : {time()-t0}")
    print(f"Temps d'exécution : {time()-t0}")