import multiprocessing
from regular_quicksort import hoare

def quicksort_helper(arr: list[int], low: int, high: int) -> None:
    """Quicksort algorithm using multiprocessing.
    :param arr: The array to sort.
    :param low: The start index of the array.
    :param high: The end index of the array.
    """
    if low < high:
        pi = hoare(arr, low, high)
        p1 = multiprocessing.Process(target=quicksort_helper, args=(arr, low, pi))
        p2 = multiprocessing.Process(target=quicksort_helper, args=(arr, pi + 1, high))
        p1.start()
        p2.start()
        p1.join()
        p2.join()

def quicksort(arr: list[int]): 
    """Quicksort algorithm using multiprocessing.
    :param arr: The array to sort.
    """ 
    quicksort_helper(arr, 0, len(arr) - 1)


if __name__ == "__main__":
    arr = [7, 8, 9, 1, 5]
    quicksort(arr)
    print(arr)