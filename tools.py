"""
Extra tools necessary for program.
"""
import random
import math
#import itertools
import bisect
import operator


def accumulate(iterable, func=operator.add):
    """Return running totals
    Examples:
        accumulate([1, 2, 3, 4, 5]) --> 1 3 6 10 15
        accumulate([1, 2, 3, 4, 5], operator.mul) --> 1 2 6 24 120
    """
    iterator = iter(iterable)
    total = next(iterator)
    yield total
    for element in iterator:
        total = func(total, element)
        yield total


def percent_reduce(seqs, percents, total):
    """Return total number of element from each list based on percent.
    Take N seqences, percents and Total number of elements to be return in N sequences.
    It is recursive = trying to pass several time to provide Total number of element
    with respective rates
    """
    #print('total:', total, 'seq:', seqs)

    new_seqs = [[] for i in range(len(seqs))]#create N empty list element in result list

    #actual number of element as size of sequence can be smaller that total
    i_total = 0
    for i_seq, i_percent, i_new_seq in zip(seqs, percents, new_seqs):
        n_seq = int(math.ceil(total*i_percent)) #calculate number of elements for each sequence
        if  n_seq < len(i_seq):
            res_seq = random.sample(i_seq, n_seq)
        elif i_seq:
            res_seq = i_seq[:]
        else:
            res_seq = []
        i_new_seq.extend(res_seq)

        #needs to delete returned elements from original sequence
        for i_res_item in res_seq:
            i_seq.remove(i_res_item)

        #real number of elements: original sequence may be smaller than requested
        n_req = len(res_seq)
        i_total += n_req
        if i_total == total:
            return new_seqs

    #if not enough elements has been taked during first recursion
    #and there are still element = run one more time and concatenate results
    total -= i_total
    if total > 0 and any(seqs):
        list(map(list.extend, new_seqs, percent_reduce(seqs, percents, total)))

    return new_seqs

def weighted_choice(choices, weights, count=1):
    """Random weighted choice of count elements"""
    choices = choices[:]
    weights = weights[:]
    res = []
    for _ in range(count):
        cumdist = list(accumulate(weights))
        random_factor = random.random() * cumdist[-1]
        item = choices[bisect.bisect(cumdist, random_factor)]
        res.append(item)
        index = choices.index(item)
        choices.remove(item)
        weights.pop(index)
    if count == 1:
        return res[0]
    return res

if __name__ == '__main__':

    ITEMS = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
             ['a', 'b', 'c', 'd', 'e', 'f'], ['1', '2', '3', '4', '5']]
    print(ITEMS)
    print(percent_reduce(ITEMS, [0.4, 0.4, 0.2], 15))


    print('weighed choice:', weighted_choice(['repeat', 'answer', 'listen'], [0.3, 0.1, 0.6]))
