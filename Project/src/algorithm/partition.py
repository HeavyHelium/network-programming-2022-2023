def hoare(arr: list[int], start: int, end: int):
    """Hoare partitioning scheme.
    :param array: The array to partition.
    :param start: The start index of the array.
    :param end: The end index of the array.
    :return: The index of the last element, smaller than the pivot.
    """

    pivot = arr[start]
    print(f"Pivot: {pivot}")
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
