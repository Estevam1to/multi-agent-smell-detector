#Q: Write a method to print even numbers in a list.
#A: 
def   printEvenNumbers(nums):
    """
    :param nums: (list) The list of numbers.
    """
    for num in nums:
        if num % 2 == 0:
            print(num)

print(printEvenNumbers([1,2,3,4,5,6,7,8,9]))

def returnEvenNUmber(nums):
    """
    :param nums: (list) The list of numbers.
    """
    result = []
    for num in nums:
        if num % 2 == 0:
            result.append(num)
    return result

assert(returnEvenNUmber([1,2,3,4,5,6,7,8,9]), [2,4,6,8])

## Auto Genetrated code by github copilot

def createAGameBoard(n):
    """
    :param n: (int) The size of the board.
    """
    board = []
    for i in range(n):
        board.append([])
        for j in range(n):
            board[i].append(0)
    return board

# Create a game board class with a method to print the board.
class GameBoard:
    def __init__(self, n):
        self.n = n
        self.board = createAGameBoard(n)
    def printBoard(self):
        for i in range(self.n):
            for j in range(self.n):
                print(self.board[i][j], end=" ")
            print()

# test GameBoard class
board = GameBoard(3)
board.printBoard()
