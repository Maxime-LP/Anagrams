from collections import defaultdict

def words(file_path):
    with open(file_path,'r') as file:
        output = set(file.read().lower().split('\n'))
    return output

def preprocessing(file_path):
    words_set = words(file_path)
    TotalWords = len(words_set)
    words_by_length = defaultdict(set)
    for word in words_set:
        words_by_length[len(word)].add(word)
    return TotalWords, words_by_length

def dispatcher(min_length,nb_of_processes, TotalWords, words_by_length):
    """
    Retourne nb_of_processes intervalles en veillant à ce que chaque intervalle de longueur de mots corresponde
    à une quantité équivalente de mots
    """
    target_interval_number_of_words = int(TotalWords/nb_of_processes)
    words_max_length = max(words_by_length.keys())
    intervals = []
    sup_bound = min_length
    while sup_bound<=words_max_length:
        inf_bound = sup_bound
        current_number_of_words = 0
        while current_number_of_words<target_interval_number_of_words and sup_bound<=words_max_length:
            current_number_of_words += len(words_by_length[sup_bound])
            sup_bound+=1
        intervals.append([inf_bound,sup_bound])
    return intervals