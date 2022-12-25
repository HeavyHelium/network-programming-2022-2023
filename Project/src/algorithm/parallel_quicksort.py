from multiprocessing import Process, Pipe, connection
from algorithm.sequential_quicksort import seq_quicksort
import random

def parallel_quicksort_helper(arr: list[int], conn: connection.Connection, proc_num: int) -> None:
    """
        The idea is to partition the list into two halves, 
        and sort each half in parallel.
    """
    if proc_num <= 0 or len(arr) <= 1:
        conn.send(seq_quicksort(arr))
        conn.close()
        return
    
    # partitioning
    pivot: int = arr.pop(random.randint(0, len(arr) - 1))

    left: list[int] = [x for x in arr if x < pivot]
    right: list[int] = [x for x in arr if x >= pivot]

    # Create a pipe to communate with the child process for the left half
    send_pipe_left, recv_pipe_left = Pipe()
    # Create a pipe to communate with the child process for the right half
    send_pipe_right, recv_pipe_right = Pipe()
    
    left_process = Process(target=parallel_quicksort_helper, 
                           args=(left, recv_pipe_left, proc_num - 1))
    right_process = Process(target=parallel_quicksort_helper, 
                            args=(right, recv_pipe_right, proc_num - 1))

    left_process.start()
    right_process.start()
    left_process.join()
    right_process.join()

    conn.send(send_pipe_left.recv() + [pivot] + send_pipe_right.recv())
    conn.close()

def parallel_quicksort(procs: int, arr: list[int]): 
    send_pipe, recv_pipe = Pipe()
    
    process = Process(target=parallel_quicksort_helper, args=(arr, recv_pipe, procs))
    process.start()
    process.join()
    sorted_arr: list[int] = send_pipe.recv() 

    return sorted_arr   

if __name__ == "__main__":
    # Simple test for the parallel quicksort
    arr: list[int] = [random.randint(0, 100) for _ in range(10)]
    assert parallel_quicksort(4, arr) == sorted(arr)
