# student name: Sant Sumetpong
# student number: 24821563

# A command-line 2048 game

# For part 2, my implementation to make the game harder is to avoid placing a 2 or 4 right next to an equal number
# vertically or horizontally to avoid immediate merges. My overall evaluation is as such: this implementation is
# more effective with more cells being full, which makes sense as there are fewer available options to place a number.


import random

board: list[list] = []  # a 2-D list to keep the current status of the game board


def init() -> None:  # Use as is
    """
        initializes the board variable
        and prints a welcome message
    """
    # initialize the board cells with ''
    for _ in range(4):
        rowList = []
        for _ in range(4):
            rowList.append('')
        board.append(rowList)
    # add two starting 2's at random cells
    twoRandomNumbers = random.sample(range(16), 2)  # randomly choose two numbers between 0 and 15
    # correspond each of the two random numbers to the corresponding cell
    twoRandomCells = ((twoRandomNumbers[0] // 4, twoRandomNumbers[0] % 4),
                      (twoRandomNumbers[1] // 4, twoRandomNumbers[1] % 4))
    for cell in twoRandomCells:  # put a 2 on each of the two chosen random cells
        board[cell[0]][cell[1]] = 2

    print();
    print("Welcome! Let's play the 2048 game.");
    print()


def displayGame() -> None:  # Use as is
    """ displays the current board on the console """
    print("+-----+-----+-----+-----+")
    for row in range(4):
        for column in range(4):
            cell = board[row][column]
            print(f"|{str(cell).center(5)}", end="")
        print("|")
        print("+-----+-----+-----+-----+")


def promptGamerForTheNextMove() -> str:  # Use as is
    """
        prompts the gamer until a valid next move or Q (to quit) is selected
        (valid move direction: one of 'W', 'A', 'S' or 'D')
        returns the user input
    """
    print("Enter one of WASD (move direction) or Q (to quit)")
    while True:  # prompt until a valid input is entered
        move = input('> ').upper()
        if move in ('W', 'A', 'S', 'D', 'Q'):  # a valid move direction or 'Q'
            break
        print('Enter one of "W", "A", "S", "D", or "Q"')  # otherwise inform the user about valid input
    return move


def addANewTwoToBoard() -> None:
    """
        adds a new 2 or 4 at an available randomly-selected cell of the board, based on probabilities; also
        makes placing the new number harder, as it tries to avoid placing the same number next to any equal vertical
        or horizontal number.
    """
    emptyCells = findEmptyCoordinates(board)

    if not emptyCells:  # we break if there are no empty cells left on the board
        return

    newNum = getRandomNumber()
    newCells = findNewCells(board, emptyCells, newNum)

    if newCells:  # if newCells is not empty, choose from it; else, choose any other empty cell
        (row, col) = random.choice(newCells)  # .choice() is a python method in the "random" class
    else:
        (row, col) = random.choice(emptyCells)

    board[row][col] = newNum


def isFullAndNoValidMove() -> bool:
    """
        returns True if no empty cell is left, False otherwise; also finds if
        there exists any valid move horizontally or vertically.
    """
    for col in range(len(board[0])):  # because all rows have equal number of columns and vice versa (4x4 matrix)
        for row in range(len(board)):
            if board[row][col] == '':
                return False
            if col < len(board[0]) - 1 and board[row][col] == board[row][col + 1]:
                return False
            if row < len(board) - 1 and board[row][col] == board[row + 1][col]:
                return False

    return True


def getCurrentScore() -> int:
    """
        calculates and returns the current score
        the score is the sum of all the numbers currently on the board
    """
    score = 0
    for col in range(len(board[0])):
        for row in range(len(board)):
            if isinstance(board[row][col], int):  # if there is an int in the cell, add the int; else, add 0
                score += board[row][col]
            else:
                score += 0

    return score


def updateTheBoardBasedOnTheUserMove(move: str) -> None:
    """
        updates the board variable based on the move argument by sliding and merging
        the move argument is either 'W', 'A', 'S', or 'D'
        directions: W for up; A for left; S for down, and D for right
    """
    print(f"Updating the board based on the move: {move}")

    if move == 'W':
        for col in range(4):  # start at first column with each row varying
            tempList = []
            for row in range(4):  # work from top to bottom
                if board[row][col] != '':
                    tempList.append(board[row][col])
                    board[row][col] = ''

            tempList = mergeElements(tempList)

            for i in range(len(tempList)):
                board[i][col] = tempList[i]  # starting from the top effectively shifts the numbers up

    elif move == 'A':
        for row in range(4):  # start at first row with each column varying
            tempList = []
            for col in range(4):  # work from left to right
                if board[row][col] != '':
                    tempList.append(board[row][col])
                    board[row][col] = ''

            tempList = mergeElements(tempList)

            for i in range(len(tempList)):
                board[row][i] = tempList[i]  # starting from the left effectively shifts the numbers left

    elif move == 'S':
        for col in range(4):  # start at first column with each row varying
            tempList = []
            for row in range(3, -1, -1):  # start = 3, stop = -1 (col = 0), step = -1, i.e. work from bottom to top
                if board[row][col] != '':
                    tempList.append(board[row][col])
                    board[row][col] = ''

            tempList = mergeElements(tempList)

            for i in range(len(tempList)):
                board[3 - i][col] = tempList[i]  # starting from the bottom effectively shifts the numbers down

    elif move == 'D':
        for row in range(4):  # start at first row with each column varying
            tempList = []
            for col in range(3, -1, -1):  # start = 3, stop = -1 (col = 0), step = -1, i.e. work from right to left
                if board[row][col] != '':
                    tempList.append(board[row][col])
                    board[row][col] = ''

            tempList = mergeElements(tempList)

            for i in range(len(tempList)):
                board[row][3 - i] = tempList[i]  # starting from the right effectively shifts the numbers right


#  new functions allowed to be added (if needed)
#  as usual, they must be documented well
#  they have to be placed below this line


def mergeElements(tempList):
    """
        Finds any potential merges in the given list. If possible, add the current number by itself.
        Else, simply iterate through and merge as is. Return type is a list.
    """
    mergedList = []  # initialize an empty list to be merged later

    i = 0
    while i < len(tempList):
        if i + 1 < len(tempList) and tempList[i] == tempList[i + 1]:  # if in range AND is adjacent/equal
            mergedList.append(tempList[i] + tempList[i])
            i += 2  # add 2 to ignore the next cell, which already has been merged by the line above
        else:
            mergedList.append(tempList[i])  # else, iterate through and merge the non-equal number to list
            i += 1

    return mergedList


def findEmptyCoordinates(board):
    """
        Finds and returns the coordinates of all empty cells to later be used for "difficulty" evaluation.
    """
    emptyCells = []

    for col in range(len(board[0])):  # try to find coordinates of all empty cells to then append a 2 or 4 (see below)
        for row in range(len(board)):
            if board[row][col] == '':
                emptyCells.append((row, col))

    return emptyCells


def getRandomNumber():
    """
        This method returns 2 with 2/3 chance and 3 with 1/3 chance
    """
    return random.choices([2, 4], weights=[2/3, 1/3], k=1)[0]  # .choices() is a python method in the "random" class


def findNewCells(board, emptyCells, newNum):
    """
        Finds more difficult cells. This means it searches through to find if any vertically or
        horizontally adjacent number is equal to the current number. If so, the flag turns true
        and indicates that it is an "easy" cell and won't be appended to newCells. Returns a list.
    """

    newCells = []
    for row, col in emptyCells:
        equalAdjacent = False
        if row > 0 and board[row - 1][col] == newNum:
            equalAdjacent = True
        if row < 3 and board[row + 1][col] == newNum:
            equalAdjacent = True
        if col > 0 and board[row][col - 1] == newNum:
            equalAdjacent = True
        if col < 3 and board[row][col + 1] == newNum:
            equalAdjacent = True
        if not equalAdjacent:
            newCells.append((row, col))  # give (row, col) of emptyCell to newCell if current cell != adjacent cell

    return newCells


if __name__ == "__main__":  # Use as is
    init()
    displayGame()
    while True:  # Super-loop for the game
        print(f"Score: {getCurrentScore()}")
        userInput = promptGamerForTheNextMove()
        if(userInput == 'Q'):
            print("Exiting the game. Thanks for playing!")
            break
        updateTheBoardBasedOnTheUserMove(userInput)
        addANewTwoToBoard()
        displayGame()

        if isFullAndNoValidMove():  # game is over once all cells are taken
            print("Game is Over. Check out your score.")
            print("Thanks for playing!")
            break
