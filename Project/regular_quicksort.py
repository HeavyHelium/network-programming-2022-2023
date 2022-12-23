import multiprocessing


def hoare(array: list[int], start: int, end: int):
    """Hoare partitioning scheme.
    :param array: The array to partition.
    :param start: The start index of the array.
    :param end: The end index of the array.
    :return: The index of the last element, smaller than the pivot.
    """

    pivot = arr[start]
    print("Pivot: ", pivot)
    i = start - 1
    j = end + 1
 
    while (True):
        i += 1
        while (arr[i] < pivot):
            i += 1

        j -= 1
        while (arr[j] > pivot):
            j -= 1
 
        if (i >= j):
            return j
 
        arr[i], arr[j] = arr[j], arr[i]
 

arr = [13, 19, 9, 5, 12, 8, 7, 4, 11, 2, 6, 21]
print(arr[hoare(arr, 0, len(arr) - 1)])
print(arr)


def quicksort_helper(array: list[int], low: int, high: int):
    if low < high: 
        pi = hoare(array, low, high)
        quicksort_helper(array, low, pi)
        quicksort_helper(array, pi + 1, high)

def quicksort(array: list[int]):
    quicksort_helper(array, 0, len(array) - 1)     

arr = [10, 7, 8, 9, 1, 5]
quicksort(arr)
print(arr)