from partition import hoare 

def quicksort_helper(array: list[int], low: int, high: int):
    if low < high: 
        pi = hoare(array, low, high)
        quicksort_helper(array, low, pi)
        quicksort_helper(array, pi + 1, high)

def quicksort(array: list[int]):
    quicksort_helper(array, 0, len(array) - 1)     


if __name__ == "__main__":
    arr = [13, 19, 9, 5, 12, 8, 7, 4, 11, 2, 6, 21]
    print(arr[hoare(arr, 0, len(arr) - 1)])
    print(arr)

    arr = [10, 7, 8, 9, 1, 5]
    quicksort(arr)
    print(arr)