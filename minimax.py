import copy


ROWS, COLS = 6,6
EMPTY = 0
COM_PIECE = 1
PLAYER_PIECE = 2
COM_KING = 3
PLAYER_KING = 4


class Minimax:
    def __init__(self, depth=10):
        self.depth = depth
        self.winning =  []
        self.best_move = None
    

    def minimax(self, board, com_turn, height=0):
        if height == self.depth:
            return self.calculatePoints(board)

        if com_turn:
            maxEval = -1000
            allComMoves = self.possibleComMoves(board)
            best_move = None
            for move in allComMoves:
                board_copy = copy.deepcopy(board)
                new_board = self.makeMove(board_copy, move)
                
                eval = self.minimax(new_board, not com_turn, height+1)
                
                if eval > maxEval:
                    maxEval = eval
                    best_move = move

                if height==0 and eval >= 0:
                    self.winning.append(move)
                
                if height == 0:
                    self.best_move = best_move
            return maxEval
        
        else:
            minEval = +1000
            allPlayerMoves = self.possiblePlayerMoves(board)
            for move in allPlayerMoves:
                board_copy = copy.deepcopy(board)
                new_board = self.makeMove(board_copy, move)
                
                eval = self.minimax(new_board, not com_turn, height+1)
                
                if eval < minEval:
                    minEval = eval

            return minEval


    def possibleComMoves(self, board):
        allValidMoves = []
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] == COM_PIECE:
                    if row < ROWS-1:
                        if col > 0 and board[row + 1][col - 1] == EMPTY:
                            allValidMoves.append((row, col, row+1, col-1))
                        if col < COLS - 1 and board[row + 1][col + 1] == EMPTY:
                            allValidMoves.append((row, col, row+1, col+1))
        return allValidMoves
    

    def possiblePlayerMoves(self, board):
        allValidMoves = []
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] == PLAYER_PIECE:
                    if row > 0:
                        if col > 0 and board[row - 1][col - 1] == EMPTY:
                            allValidMoves.append((row, col, row-1, col-1))
                        if col < COLS - 1 and board[row - 1][col + 1] == EMPTY:
                            allValidMoves.append((row, col, row-1, col+1))
        return allValidMoves


    def calculatePoints(self, board):
        comPieceCount, playerPieceCount = 0, 0
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] == COM_PIECE or board[row][col] == COM_KING:
                    comPieceCount+=1
                elif board[row][col] == PLAYER_PIECE or board[row][col] == PLAYER_KING:
                    playerPieceCount+=1
        return comPieceCount - playerPieceCount


    def makeMove(self, board, move):
        board[move[2]][move[3]] = board[move[0]][move[1]]
        board[move[0]][move[1]] = EMPTY
        return board
