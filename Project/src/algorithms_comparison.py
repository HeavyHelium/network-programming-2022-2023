from algorithm.sequential_quicksort import seq_quicksort
from algorithm.parallel_quicksort import parallel_quicksort
import random
import time

def is_sorted(arr: list[int]) -> bool:
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True

def compare_quicksort(N: int):
    print("==============================================================")
    print("Comparing sequential and parallel quicksort")
    print(f"Given that there are N = {N} randomly chosen elements in list")
    lst = [random.randint(0, 100) for _ in range(N)]


    start = time.time()
    res_seq = seq_quicksort(lst)
    end = time.time()
    elapsed_time_seq = end - start
    print(f"Sequential quicksort took {elapsed_time_seq} seconds")

    start = time.time()
    res_par = parallel_quicksort(3, lst)
    end = time.time()
    elapsed_time_par = end - start
    print(f"Parallel quicksort took {elapsed_time_par} seconds")

    assert is_sorted(res_seq)
    assert is_sorted(res_par)
    assert res_seq == res_par

compare_quicksort(100)
compare_quicksort(10500)