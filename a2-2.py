
import csv
import itertools

class Board():

    ##########################################
    ####   Constructor
    ##########################################
    def __init__(self, filename):

        # initialize all of the variables
        self.n2 = 0
        self.n = 0
        self.spaces = 0
        self.board = None
        self.valsInRows = None
        self.valsInCols = None
        self.valsInBoxes = None
        self.unsolvedSpaces = None

        # load the file and initialize the in-memory board with the data
        self.loadSudoku(filename)


    # loads the sudoku board from the given file
    def loadSudoku(self, filename):

        with open(filename) as csvFile:
            self.n = -1
            reader = csv.reader(csvFile)
            for row in reader:

                # Assign the n value and construct the approriately sized dependent data
                if self.n == -1:
                    self.n = int(len(row) ** (1/2))
                    if not self.n ** 2 == len(row):
                        raise Exception('Each row must have n^2 values! (See row 0)')
                    else:
                        self.n2 = len(row)
                        self.spaces = self.n ** 4
                        self.board = {}
                        self.valsInRows = [set() for _ in range(self.n2)]
                        self.valsInCols = [set() for _ in range(self.n2)]
                        self.valsInBoxes = [set() for _ in range(self.n2)]
                        self.unsolvedSpaces = set(itertools.product(range(self.n2), range(self.n2)))

                # check if each row has the correct number of values
                else:
                    if len(row) != self.n2:
                        raise Exception('Each row must have the same number of values. (See row ' + str(reader.line_num - 1) + ')')

                # add each value to the correct place in the board; record that the row, col, and box contains value
                for index, item in enumerate(row):
                    if not item == '':
                        self.board[(reader.line_num-1, index)] = int(item)
                        self.valsInRows[reader.line_num-1].add(int(item))
                        self.valsInCols[index].add(int(item))
                        self.valsInBoxes[self.spaceToBox(reader.line_num-1, index)].add(int(item))
                        self.unsolvedSpaces.remove((reader.line_num-1, index))


    ##########################################
    ####   Utility Functions
    ##########################################

    # converts a given row and column to its inner box number
    def spaceToBox(self, row, col):
        return self.n * (row // self.n) + col // self.n

    # prints out a command line representation of the board
    def print(self):
        for r in range(self.n2):
            # add row divider
            if r % self.n == 0 and not r == 0:
                if self.n2 > 9:
                    print("  " + "----" * self.n2)
                else:
                    print("  " + "---" * self.n2)

            row = ""

            for c in range(self.n2):

                if (r,c) in self.board:
                    val = self.board[(r,c)]
                else:
                    val = None

                # add column divider
                if c % self.n == 0 and not c == 0:
                    row += " | "
                else:
                    row += "  "

                # add value placeholder
                if self.n2 > 9:
                    if val is None: row += "__"
                    else: row += "%2i" % val
                else:
                    if val is None: row += "_"
                    else: row += str(val)
            print(row)


    ##########################################
    ####   Move Functions - YOUR IMPLEMENTATIONS GO HERE
    ##########################################

    # makes a move, records it in its row, col, and box, and removes the space from unsolvedSpaces
    def makeMove(self, space, value):
        r,c = space
        br = r//self.n
        bc = c//self.n
        self.board[(r,c)]=value
        self.valsInRows[r].add(value)
        self.valsInCols[c].add(value)
        self.valsInBoxes[(br*self.n)+bc].add(value)
        self.unsolvedSpaces.remove((r,c))

    # removes the move, its record in its row, col, and box, and adds the space back to unsolvedSpaces
    def undoMove(self, space, value):
        r,c = space
        br = r//self.n
        bc = c//self.n
        del(self.board[(r,c)])
        self.valsInRows[r].remove(value)
        self.valsInCols[c].remove(value)
        self.valsInBoxes[(br*self.n)+bc].remove(value)
        self.unsolvedSpaces.add((r,c))

    # returns True if the space is empty and on the board,
    # and assigning value to it if not blocked by any constraints
    def isValidMove(self, space, value):
        r,c = space
        br = r//self.n
        bc = c//self.n
        if value not in self.valsInRows[r] and value not in self.valsInCols[c] and value not in self.valsInBoxes[(br*self.n)+bc]:
            return True
        return False

    # gets the unsolved space with the most current constraints
    # returns None if unsolvedSpaces is empty
    def getMostConstrainedUnsolvedSpace(self):
        if not self.unsolvedSpaces:
            return None


        def evaluateSpace(space):
            row, col = space
            row_constraints = len(self.valsInRows[row])
            col_constraints = len(self.valsInCols[col])
            box_constraints = len(self.valsInBoxes[self.spaceToBox(row, col)])
            constraints = row_constraints + col_constraints + box_constraints

            return constraints


        sorted_spaces = sorted(self.unsolvedSpaces, key=evaluateSpace, reverse=True)
        return sorted_spaces[0]


class Solver:
    ##########################################
    ####   Constructor
    ##########################################
    def __init__(self):
        pass

    ##########################################
    ####   Solver
    ##########################################

    # recursively selects the most constrained unsolved space and attempts
    # to assign a value to it

    # upon completion, it will leave the board in the solved state (or original
    # state if a solution does not exist)

    # returns True if a solution exists and False if one does not
    def solveBoard(self, board):
        if not board.getMostConstrainedUnsolvedSpace():
            return True
        else:
            space = board.getMostConstrainedUnsolvedSpace()
        # print(space,"SPACE")
        # count = count + 1
        print(len(board.unsolvedSpaces),"UNSOLVED SPACES LEFT")
        for value in range(1,board.n2+1):
            print(space,"CURRENT SPACE")
            print(value, "CURRENT VALUE")
            # print("===============================")
            # print("===============================")
            # print("===============================")
            # board.print()
            if(board.isValidMove(space, value)):
                board.makeMove(space, value)
                # print(count,"CURRENT COUNT")
                if(self.solveBoard(board)):
                    return True
                board.undoMove(space, value)
                # count = count - 1
                # print(count, "Current Count")
                # print("BACKTRACKED",space , value, "SPACE, BACKTRACKED VALUE")
        # print("NO VALID NUMBERS" , space , value, "SPACE, VALUE")
        return False
        # print(board.valsInRows) # List of Sets
        # print(board.valsInCols) # List of Sets
        # print(board.valsInBoxes) #List of Sets
        # print(board.unsolvedSpaces) #Set of lists
        # print(board.board)

if __name__ == "__main__":
    # change this to the input file that you'd like to test
    board = Board("tests-1\\tests\\test-1-easy\\07.csv")
    s = Solver()
    s.solveBoard(board)
    board.print()
