"""
    Sort lists with Algorsort
    supports number lists and word lists
    batteries not included

    created by:
    Jased#0001
    and Github Copilot
"""

if __name__ == "__main__":
    exit()

#bubble sort, insertion sort, selection sort, merge sort, quick sort, and heap sort
class NumberListSort():
    """
        sort numbers in a list by size
    """
    def bubble(sort: list) -> list:
        """
        bubble sort algorithm
        """
        try:
            for i in range(len(sort)):
                for j in range(len(sort)-1):
                    if sort[j] > sort[j+1]:
                        sort[j], sort[j+1] = sort[j+1], sort[j]
            return sort
        except Exception as e:
            return e

    def insertion(sort: list) -> list:
        """
        insertion sort algorithm
        """
        try:
            for i in range(1, len(sort)):
                j = i
                while j > 0 and sort[j-1] > sort[j]:
                    sort[j-1], sort[j] = sort[j], sort[j-1]
                    j -= 1
            return sort
        except Exception as e:
            return e

    def selection(sort: list) -> list:
        """
        selection sort algorithm
        """
        try:
            for i in range(len(sort)):
                min = i
                for j in range(i+1, len(sort)):
                    if sort[min] > sort[j]:
                        min = j
                sort[i], sort[min] = sort[min], sort[i]
            return sort
        except Exception as e:
            return e

    def merge(sort: list) -> list:
        """
        merge sort algorithm
        """
        try:
            if len(sort) > 1:
                mid = len(sort)//2
                left = sort[:mid]
                right = sort[mid:]
                NumberListSort.merge(left)
                NumberListSort.merge(right)
                i = j = k = 0
                while i < len(left) and j < len(right):
                    if left[i] < right[j]:
                        sort[k] = left[i]
                        i += 1
                    else:
                        sort[k] = right[j]
                        j += 1
                    k += 1
                while i < len(left):
                    sort[k] = left[i]
                    i += 1
                    k += 1
                while j < len(right):
                    sort[k] = right[j]
                    j += 1
                    k += 1
            return sort
        except Exception as e:
            return e

    def quick(sort: list) -> list:
        """
        quick sort algorithm
        """
        try:
            if len(sort) > 1:
                pivot = sort[0]
                left = []
                right = []
                for i in range(1, len(sort)):
                    if sort[i] < pivot:
                        left.append(sort[i])
                    else:
                        right.append(sort[i])
                NumberListSort.quick(left)
                NumberListSort.quick(right)
                sort[:] = left + [pivot] + right
            return sort
        except Exception as e:
            return e

    def heap(sort: list) -> list:
        """
        heap sort algorithm
        """

        def heapify(arr: list, n: int, i: int):
            largest = i
            l = 2*i + 1
            r = 2*i + 2
            if l < n and arr[i] < arr[l]:
                largest = l
            if r < n and arr[largest] < arr[r]:
                largest = r
            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                heapify(arr, n, largest)

        try:
            n = len(sort)
            for i in range(n, -1, -1):
                heapify(sort, n, i)
            for i in range(n-1, 0, -1):
                sort[i], sort[0] = sort[0], sort[i]
                heapify(sort, i, 0)
            return sort
        except Exception as e:
            return e

    #radix sort, counting sort, bucket sort, shell sort, and comb sort
    def radix(sort: list) -> list:
        """
        radix sort algorithm
        """
        try:
            max = 0
            for i in range(len(sort)):
                if max < sort[i]:
                    max = sort[i]
            for i in range(1, max+1):
                bucket = [[] for i in range(10)]
                for j in range(len(sort)):
                    bucket[sort[j]%10].append(sort[j])
                sort = []
                for j in range(10):
                    sort += bucket[j]
            return sort
        except Exception as e:
            return e

    def counting(sort: list) -> list:
        """
        counting sort algorithm
        """
        try:
            max = 0
            for i in range(len(sort)):
                if max < sort[i]:
                    max = sort[i]
            count = [0]*(max+1)
            for i in range(len(sort)):
                count[sort[i]] += 1
            for i in range(1, max+1):
                count[i] += count[i-1]
            for i in range(len(sort)-1, -1, -1):
                sort[count[sort[i]]-1] = sort[i]
                count[sort[i]] -= 1
            return sort
        except Exception as e:
            return e

    def bucket(sort: list) -> list:
        """
        bucket sort algorithm
        """
        try:
            max = 0
            for i in range(len(sort)):
                if max < sort[i]:
                    max = sort[i]
            bucket = [[] for i in range(max+1)]
            for i in range(len(sort)):
                bucket[sort[i]].append(sort[i])
            sort = []
            for i in range(max+1):
                sort += bucket[i]
            return sort
        except Exception as e:
            return e

    def shell(sort: list) -> list:
        """
        shell sort algorithm
        """
        try:
            gap = len(sort)//2
            while gap > 0:
                for i in range(gap, len(sort)):
                    temp = sort[i]
                    j = i
                    while j >= gap and sort[j-gap] > temp:
                        sort[j] = sort[j-gap]
                        j -= gap
                    sort[j] = temp
                gap //= 2
            return sort
        except Exception as e:
            return e

    def comb(sort: list) -> list:
        """
        comb sort algorithm
        """
        try:
            gap = len(sort)
            while gap > 1:
                gap = int(gap/1.3)
                for i in range(gap, len(sort)):
                    temp = sort[i]
                    j = i
                    while j >= gap and sort[j-gap] > temp:
                        sort[j] = sort[j-gap]
                        j -= gap
                    sort[j] = temp
            return sort
        except Exception as e:
            return e
            
    #cycle sort, cocktail sort, gnome sort, and pancake sort
    def cycle(sort: list) -> list:
        """
        cycle sort algorithm
        """
        try:
            for i in range(len(sort)):
                while i > 0 and sort[i] < sort[i-1]:
                    sort[i], sort[i-1] = sort[i-1], sort[i]
                    i -= 1
            return sort
        except Exception as e:
            return e

    def cocktail(sort: list) -> list:
        """
        cocktail sort algorithm
        """
        try:
            left = 0
            right = len(sort)-1
            while left < right:
                for i in range(left, right):
                    if sort[i] > sort[i+1]:
                        sort[i], sort[i+1] = sort[i+1], sort[i]
                right -= 1
                for i in range(right, left, -1):
                    if sort[i] < sort[i-1]:
                        sort[i], sort[i-1] = sort[i-1], sort[i]
                left += 1
            return sort
        except Exception as e:
            return e

    def gnome(sort: list) -> list:
        """
        gnome sort algorithm
        """
        try:
            i = 0
            while i < len(sort):
                if i == 0 or sort[i] >= sort[i-1]:
                    i += 1
                else:
                    sort[i], sort[i-1] = sort[i-1], sort[i]
                    i -= 1
            return sort
        except Exception as e:
            return e

    def pancake(sort: list) -> list:
        """
        pancake sort algorithm
        """
        try:
            for i in range(len(sort)):
                for j in range(i, len(sort)):
                    if sort[j] < sort[i]:
                        sort[j], sort[i] = sort[i], sort[j]
                        if i != 0:
                            sort[:i+1] = sort[:i+1][::-1]
                        if j != len(sort)-1:
                            sort[j+1:] = sort[j+1:][::-1]
            return sort
        except Exception as e:
            return e

class WordListSort:
    """
    sort words in a list alphabetically using the above sorting algorithms
    """

    def __init__(self, words: list):
        self.words = words

    def bubble(self) -> list:
        """
        bubble sort algorithm
        """
        try:
            for i in range(len(self.words)):
                for j in range(len(self.words)-1, i, -1):
                    if self.words[j] < self.words[j-1]:
                        self.words[j], self.words[j-1] = self.words[j-1], self.words[j]
            return self.words
        except Exception as e:
            return e

    def selection(self) -> list:
        """
        selection sort algorithm
        """
        try:
            for i in range(len(self.words)):
                min = i
                for j in range(i+1, len(self.words)):
                    if self.words[j] < self.words[min]:
                        min = j
                self.words[i], self.words[min] = self.words[min], self.words[i]
            return self.words
        except Exception as e:
            return e

    def insertion(self) -> list:
        """
        insertion sort algorithm
        """
        try:
            for i in range(1, len(self.words)):
                temp = self.words[i]
                j = i
                while j > 0 and self.words[j-1] > temp:
                    self.words[j] = self.words[j-1]
                    j -= 1
                self.words[j] = temp
            return self.words
        except Exception as e:
            return e

    def merge(self) -> list:
        """
        merge sort algorithm
        """
        def merge_sort(sort: list) -> list:
            """
            merge sort algorithm
            """
            if len(sort) > 1:
                mid = len(sort)//2
                left = sort[:mid]
                right = sort[mid:]
                merge_sort(left)
                merge_sort(right)
                i = j = k = 0
                while i < len(left) and j < len(right):
                    if left[i] < right[j]:
                        sort[k] = left[i]
                        i += 1
                    else:
                        sort[k] = right[j]
                        j += 1
                    k += 1
                while i < len(left):
                    sort[k] = left[i]
                    i += 1
                    k += 1
                while j < len(right):
                    sort[k] = right[j]
                    j += 1
                    k += 1
            return sort
        try:
            return merge_sort(self.words)
        except Exception as e:
            return e

    def quick(self) -> list:
        """
        quick sort algorithm
        """
        def quick_sort(sort: list) -> list:
            """
            quick sort algorithm
            """
            if len(sort) > 1:
                pivot = sort[0]
                left = [i for i in sort[1:] if i < pivot]
                right = [i for i in sort[1:] if i >= pivot]
                return quick_sort(left) + [pivot] + quick_sort(right)
            else:
                return sort
        try:
            return quick_sort(self.words)
        except Exception as e:
            return e

    def heap(self) -> list:
        """
        heap sort algorithm
        """
        def heapify(sort: list, n: int, i: int) -> list:
            """
            heap sort algorithm
            """
            largest = i
            l = 2*i+1
            r = 2*i+2
            if l < n and sort[i] < sort[l]:
                largest = l
            if r < n and sort[largest] < sort[r]:
                largest = r
            if largest != i:
                sort[i], sort[largest] = sort[largest], sort[i]
                heapify(sort, n, largest)
            return sort
        try:
            n = len(self.words)
            for i in range(n//2-1, -1, -1):
                heapify(self.words, n, i)
            for i in range(n-1, 0, -1):
                self.words[i], self.words[0] = self.words[0], self.words[i]
                heapify(self.words, i, 0)
            return self.words
        except Exception as e:
            return e

    def cocktail(self) -> list:
        """
        cocktail sort algorithm
        """
        try:
            left = 0
            right = len(self.words)-1
            while left < right:
                for i in range(left, right):
                    if self.words[i] > self.words[i+1]:
                        self.words[i], self.words[i+1] = self.words[i+1], self.words[i]
                right -= 1
                for i in range(right, left, -1):
                    if self.words[i] < self.words[i-1]:
                        self.words[i], self.words[i-1] = self.words[i-1], self.words[i]
                left += 1
            return self.words
        except Exception as e:
            return e

    def comb(self) -> list:
        """
        comb sort algorithm
        """
        try:
            gap = len(self.words)
            shrink = 1.3
            sorted = False
            while not sorted:
                gap = int(gap/shrink)
                if gap > 1:
                    sorted = False
                else:
                    gap = 1
                    sorted = True
                i = 0
                while i+gap < len(self.words):
                    if self.words[i] > self.words[i+gap]:
                        self.words[i], self.words[i+gap] = self.words[i+gap], self.words[i]
                        sorted = False
                    i += 1
            return self.words
        except Exception as e:
            return e

    def gnome(self) -> list:
        """
        gnome sort algorithm
        """
        try:
            i = 0
            while i < len(self.words):
                if i == 0 or self.words[i] >= self.words[i-1]:
                    i += 1
                else:
                    self.words[i], self.words[i-1] = self.words[i-1], self.words[i]
                    i -= 1
            return self.words
        except Exception as e:
            return e

    def odd_even(self) -> list:
        """
        odd-even sort algorithm
        """
        try:
            sorted = False
            while not sorted:
                sorted = True
                for i in range(1, len(self.words)-1, 2):
                    if self.words[i] > self.words[i+1]:
                        self.words[i], self.words[i+1] = self.words[i+1], self.words[i]
                        sorted = False
                for i in range(0, len(self.words)-1, 2):
                    if self.words[i] > self.words[i+1]:
                        self.words[i], self.words[i+1] = self.words[i+1], self.words[i]
                        sorted = False
            return self.words
        except Exception as e:
            return e

    def stooge(self) -> list:
        """
        stooge sort algorithm
        """
        def stooge_sort(sort: list, i: int, j: int) -> list:
            """
            stooge sort algorithm
            """
            if sort[i] > sort[j]:
                sort[i], sort[j] = sort[j], sort[i]
            if i+1 >= j:
                return sort
            t = (j-i+1)//3
            stooge_sort(sort, i, j-t)
            stooge_sort(sort, i+t, j)
            stooge_sort(sort, i, j-t)
            return sort
        try:
            return stooge_sort(self.words, 0, len(self.words)-1)
        except Exception as e:
            return e
