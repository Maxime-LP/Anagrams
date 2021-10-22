from collections import Counter, defaultdict
from time import time
from job import job
import multiprocessing as mp

if __name__ == '__main__':   
    t0 = time()
    nb_of_processes = mp.cpu_count() - 1
    queue = mp.Queue()
    
    tasks = [job(id_n,nb_of_processes,queue) for id_n in range(1,nb_of_processes+1)]

    for task in tasks:
        task.start()
    for task in tasks:
        task.join()
    
    output_dict = {}
    while not queue.empty():
        local_dict = queue.get()
        output_dict.update(local_dict)

    output = zip(output_dict.keys(),output_dict.values())
    with open('log.txt','w') as log:
        for group in output:
            log.write(f"{','.join(group)} \n")
        log.write(f"Temps d'exécution : {time()-t0}")