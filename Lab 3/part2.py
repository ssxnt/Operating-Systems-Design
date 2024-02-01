# student name: Sant Sumetpong
# student number: 24821563

import multiprocessing as mp


def checkColumn(puzzle: list, column: int):
    """
        param puzzle: a list of lists containing the puzzle
        param column: the column to check (a value between 0 to 8)

        This function checks the indicated column of the puzzle, and
        prints whether it is valid or not.

        As usual, this function must not mutate puzzle
    """
    repeat = set()  # to track how many unique numbers there are and thus if there are any repeats

    for row in range(len(puzzle)):
        num = puzzle[row][column]
        if num in repeat or num not in range(1, 10):
            print(f"Column {column} not valid")
            return
        repeat.add(num)
    print(f"Column {column} valid")


def checkRow(puzzle: list, row: int):
    """
        param puzzle: a list of lists containing the puzzle
        param row: the row to check (a value between 0 to 8)

        This function checks the indicated row of the puzzle, and
        prints whether it is valid or not.

        As usual, this function must not mutate puzzle
    """
    repeat = set(puzzle[row])  # no need to add nums to this because this creates a set of the entire row already
    valid = True

    for num in repeat:
        if num not in range(1, 10):
            valid = False

    if valid and len(repeat) == 9:  # if len < 9, this means there was a duplicate and the row is thus invalid
        print(f"Row {row} valid")
    else:
        print(f"Row {row} not valid")


def checkSubgrid(puzzle: list, subgrid: int):
    """
        param puzzle: a list of lists containing the puzzle
        param subgrid: the subgrid to check (a value between 0 to 8)
        Subgrid numbering order:    0 1 2
                                    3 4 5
                                    6 7 8
        where each subgrid itself is a 3x3 portion of the original list

        This function checks the indicated subgrid of the puzzle, and
        prints whether it is valid or not.

        As usual, this function must not mutate puzzle
    """
    repeat = set()
    initRow, initCol = 3 * int(subgrid / 3), 3 * (subgrid % 3)  # mathematical way to determine starting rows/cols

    for row in range(initRow, initRow + 3):
        for col in range(initCol, initCol + 3):
            num = puzzle[row][col]
            if num in repeat or num not in range(1, 10):
                print(f"Subgrid {subgrid} not valid")
                return
            repeat.add(num)
    print(f"Subgrid {subgrid} valid")


if __name__ == "__main__":
    test1 = [[6, 2, 4, 5, 3, 9, 1, 8, 7],
             [5, 1, 9, 7, 2, 8, 6, 3, 4],
             [8, 3, 7, 6, 1, 4, 2, 9, 5],
             [1, 4, 3, 8, 6, 5, 7, 2, 9],
             [9, 5, 8, 2, 4, 7, 3, 6, 1],
             [7, 6, 2, 3, 9, 1, 4, 5, 8],
             [3, 7, 1, 9, 5, 6, 8, 4, 2],
             [4, 9, 6, 1, 8, 2, 5, 7, 3],
             [2, 8, 5, 4, 7, 3, 9, 1, 6]
             ]
    test2 = [[6, 2, 4, 5, 3, 9, 1, 8, 7],
             [5, 1, 9, 7, 2, 8, 6, 3, 4],
             [8, 3, 7, 6, 1, 4, 2, 9, 5],
             [6, 2, 4, 5, 3, 9, 1, 8, 7],
             [5, 1, 9, 7, 2, 8, 6, 3, 4],
             [8, 3, 7, 6, 1, 4, 2, 9, 5],
             [6, 2, 4, 5, 3, 9, 1, 8, 7],
             [5, 1, 9, 7, 2, 8, 6, 3, 4],
             [8, 3, 7, 6, 1, 4, 2, 9, 5]
             ]

    testcase = test1  # modify here for other testcases
    SIZE = 9

    processes = []  # to keep track of all started processes

    for col in range(SIZE):
        process = mp.Process(target=checkColumn, args=(testcase, col))
        processes.append(process)
        process.start()

    for row in range(SIZE):
        process = mp.Process(target=checkRow, args=(testcase, row))
        processes.append(process)
        process.start()

    for subgrid in range(SIZE):
        process = mp.Process(target=checkSubgrid, args=(testcase, subgrid))
        processes.append(process)
        process.start()

    for process in processes:  # when all processes have finished, join them
        process.join()
