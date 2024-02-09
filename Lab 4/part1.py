# student name: Sant Sumetpong
# student number: 24821563

import threading as t


def sortingWorker(firstHalf: bool) -> None:
    """
    If param firstHalf is True, the method
    takes the first half of the shared list testcase,
    and stores the sorted version of it in the shared
    variable sortedFirstHalf.
    Otherwise, it takes the second half of the shared list
    testcase, and stores the sorted version of it in
    the shared variable sortedSecondHalf.
    The sorting is ascending, and you can choose any
    sorting algorithm of your choice and code it.
    """
    def bsort(nums: list) -> None:  # my version of a bubble sort algorithm
        for i in range(len(nums)):
            for j in range(0, len(nums) - i - 1):
                if nums[j] > nums[j + 1]:  # if current bigger than adjacent, swap
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]

    n = int(len(testcase) / 2)

    if firstHalf:
        sortedFirstHalf[:] = testcase[:n]  # first half of list
        bsort(sortedFirstHalf)
    else:
        sortedSecondHalf[:] = testcase[n:]  # second half of list
        bsort(sortedSecondHalf)


def mergingWorker() -> None:
    """ This function uses the two shared variables
        sortedFirstHalf and sortedSecondHalf, and merges/sorts
        them into a single sorted list that is stored in
        the shared variable sortedFullList.
    """
    global SortedFullList
    i, j = 0, 0
    while i < len(sortedFirstHalf) and j < len(sortedSecondHalf):  # compare both lists and append to main list
        if sortedFirstHalf[i] < sortedSecondHalf[j]:
            SortedFullList.append(sortedFirstHalf[i])
            i += 1
        else:
            SortedFullList.append(sortedSecondHalf[j])
            j += 1
    SortedFullList += sortedFirstHalf[i:] + sortedSecondHalf[j:]  # account for any remaining values after sorted merge

if __name__ == "__main__":
    # shared variables
    testcase = [8, 5, 7, 7, 4, 1, 3, 2]
    sortedFirstHalf: list = []
    sortedSecondHalf: list = []
    SortedFullList: list = []

    t1 = t.Thread(target=sortingWorker, args=(True,))
    t2 = t.Thread(target=sortingWorker, args=(False,))
    t12 = t.Thread(target=mergingWorker)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    t12.start()
    t12.join()

    # as a simple test, printing the final sorted list
    print("The final sorted list is ", SortedFullList)
