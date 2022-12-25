#import random

def seq_quicksort(arr: list[int]) -> list[int]:
    """
        Sorts a list of integers using the quicksort algorithm.
        This version of quicksort uses linear amounts of memory, 
        since it returns a new list for the sorted values.
    
        :param arr: The list of integers to sort.
        :return: The sorted list of integers.
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    lesser = seq_quicksort([x for x in arr[1:] if x < pivot])
    greater = seq_quicksort([x for x in arr[1:] if x >= pivot])
    return lesser + [pivot] + greater