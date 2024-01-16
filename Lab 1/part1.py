# student name: Sant Sumetpong
# student number: 24821563

# A command-line 2048 game


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
        adds a new 2 at an available randomly-selected cell of the board
    """
    if not isFull():
        while True:
            row = random.randint(0, 3)
            col = random.randint(0, 3)

            if board[row][col] == '':
                board[row][col] = 2
                break


def isFull() -> bool:
    """ 
        returns True if no empty cell is left, False otherwise 
    """
    for col in range(len(board[0])):  # because all rows have equal number of columns
        for row in range(len(board)):
            if board[row][col] == '':
                return False
            else:
                continue
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

    print(f"Updating the board based on the move: {move}")


#  up to two new functions allowed to be added (if needed)
#  as usual, they must be documented well
#  they have to be placed below this line


def mergeElements(tempList):
    mergedList = []  # initialize an empty list to be merged later
    i = 0
    while i < len(tempList):
        if i + 1 < len(tempList) and tempList[i] == tempList[i + 1]:  # if iterator is in range AND is adjacent/equal
            mergedList.append(tempList[i] + tempList[i])
            i += 2  # add 2 to ignore the next cell, which already has been merged by the line above
        else:
            mergedList.append(tempList[i])  # else, iterate through and merge the non-equal number to list
            i += 1
    return mergedList


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

        if isFull():  # game is over once all cells are taken
            print("Game is Over. Check out your score.")
            print("Thanks for playing!")
            break
