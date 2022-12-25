from multiprocessing import Pipe, Process
import algorithm.parallel_quicksort as pq


class DataHandler:
    def __init__(self, data: str):
        self._proc_num, self._data = self.parse_data(data)

    @staticmethod
    def parse_data(data) -> tuple[int, list[int]]:
        """
        data format is: number of processes, list of numbers
        format of the list of numbers is: [element1, element2, ..., elementN]
        :param data: data to be read
        :return: tuple of number of processes and list of numbers
        """
        proc_num, *lst = data.split(",", 1)
        proc_num = int(proc_num)

        lst = lst[0].strip()
        
        if lst[0] != "[" or lst[-1] != "]":
            raise ValueError("Invalid data format!")
        
        lst = lst[1:-1]
        lst = lst.split(",")
        data = [int(x) for x in lst]

        return proc_num, data


    def __call__(self) -> str:
        return str(pq.parallel_quicksort(self._proc_num, self._data))

if __name__ == "__main__":
    dh = DataHandler("4, [5, 7, 2, 3, 1, 4, 6, 8, 9, 10]")
    print(dh())