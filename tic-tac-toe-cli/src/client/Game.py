class Game:
    def __init__(self):
        self.board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
        self.player = '1'


    def isWinner(self):
        return ((self.board[0][0] == self.board[0][1] == self.board[0][2] != ' ') or # across the top
        (self.board[1][0] ==  self.board[1][1] ==  self.board[1][2] != ' ') or # across the middle
        (self.board[2][0] ==  self.board[2][1] ==  self.board[2][2] != ' ') or # across the bottom
        (self.board[0][0] ==  self.board[1][0] ==  self.board[2][0] != ' ') or # down the left side
        (self.board[0][1] ==  self.board[1][1] ==  self.board[2][1] != ' ') or # down the middle
        (self.board[0][2] ==  self.board[1][2] ==  self.board[2][2] != ' ') or # down the right side
        (self.board[0][0] ==  self.board[1][1] ==  self.board[2][2] != ' ') or # diagonal
        (self.board[2][0] ==  self.board[1][1] ==  self.board[0][2] != ' ')) # diagonal

    def isFinished(self):
        if self.isWinner():
            return True
        for value in self.board:
            for p in value:
                if p == ' ': return False
        return True


    def play(self, column, row):
        if self.board[row-1][column-1] == ' ':
            self.board[row-1][column-1] = self.player
            self.player = '2' if self.player == '1' else '1'
            return True
        return False

    def drawBoard(self):
        # This function prints out the board that it was passed.

        # "board" is a list of 10 strings representing the board (ignore index 0)
        print('   |   |')
        print(' ' + self.board[0][0] + ' | ' + self.board[0][1] + ' | ' + self.board[0][2])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + self.board[1][0] + ' | ' + self.board[1][1] + ' | ' + self.board[1][2])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + self.board[2][0] + ' | ' + self.board[2][1] + ' | ' + self.board[2][2])
        print('   |   |')
