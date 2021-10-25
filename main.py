from time import time
import multiprocessing as mp
from job import job
from preprocessing import preprocessing, dispatcher

if __name__ == '__main__':   
    t0 = time()

    file_path = 'words'
    nb_of_processes = 2
    queue = mp.Queue()
    TotalWords, words_by_length = list(preprocessing(file_path))[0:100000]
    TotalWords=100000
    min_length=2
    intervals = dispatcher(min_length,nb_of_processes, TotalWords, words_by_length)
    tasks = []

    for id_n in range(1,nb_of_processes+1):
        interval = intervals[id_n-1]
        words = set()
        for length in range(interval[0],interval[1]) :
            words.update(words_by_length[length])
        tasks.append(job(id_n,words,queue))

    for task in tasks:
        task.start()
    print('1')
    for task in tasks:
        task.join()
    print(queue.empty())
    output_dict = {}
    while not queue.empty():
        local_dict = queue.get()
        print(local_dict)
        output_dict.update(local_dict)
    print('3')
    output = zip(output_dict.keys(),output_dict.values())
    with open('log.txt','w') as log:
        for group in output:
            log.write(f"{','.join(group)} \n")
        log.write(f"Temps d'exécution : {time()-t0}")
