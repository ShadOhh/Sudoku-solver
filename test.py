# Number of queens
print("Enter the number of queens")
N = int(input())
# Chessboard
# NxN matrix with all elements 0
board = [[0]*N for _ in range(N)]

# Function to check if there is an attack on a particular position
def is_attack(i, j):
    # Checking if there is a queen in the same row or column
    for k in range(0, N):
        if board[i][k] == 1 or board[k][j] == 1:
            return True
    # Checking diagonals
    for k in range(0, N):
        for l in range(0, N):
            if (k + l == i + j) or (k - l == i - j):
                if board[k][l] == 1:
                    return True
    return False

# Function to solve the N-Queen problem using backtracking
def N_queen(n):
    # Base case: If n is 0, solution found
    if n == 0:
        return True
    for i in range(0, N):
        for j in range(0, N):
            '''Checking if we can place a queen here or not.
            A queen will not be placed if the position is being attacked
            or already occupied by another queen.'''
            if (not is_attack(i, j)) and (board[i][j] != 1):
                board[i][j] = 1
                # Recursion: Check if we can place the next queen with this arrangement
                if N_queen(n-1) == True:
                    return True
                board[i][j] = 0
    return False

# Call the N_queen function to solve the problem
N_queen(N)
for i in board:
    print(i)
