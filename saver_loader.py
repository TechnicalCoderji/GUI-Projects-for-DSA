# This File For Save and Load Sudoku From/To ".sudoku" File.
import pickle

# For Save Sudoku from Board to as a File
def save_sudoku(file_name, board):
    # Making Board With Saving File
    final_board = [[None for _ in range(9)] for _ in range(9)]
    for i,j in board:
        value = board[(i,j)].text
        if value:
            final_board[i][j] = int(value)
        else:
            final_board[i][j] = None

    final_file_name = "game boards/"+file_name+".sudoku"
    with open(final_file_name,"wb") as file:
        pickle.dump(final_board,file)

# For Load Sudoku from File to as a Board
def load_sudoku(file_name, board):
    final_file_name = "game boards/"+file_name+".sudoku"
    with open(final_file_name,"rb") as file:
        loaded_board = pickle.load(file)

    for i,j in board:
        value = loaded_board[i][j]
        if value:
            board[(i,j)].text = str(value)
            board[(i,j)].permanent = True
        else:
            board[(i,j)].text = None
            board[(i,j)].permanent = False

if __name__=="__main__":
    pass