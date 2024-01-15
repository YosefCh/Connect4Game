from abc import (ABC, abstractmethod)


class Connect4GameStrategy(ABC):
    def __init__(self):
        ...

    @abstractmethod
    def strategy(self, game_safety_copy):
        ...


class Connect4Game:
    def __init__(self):
        self.board = [[0] * 7 for _ in range(6)]
        self.current_player = 1
        self.winner = None

    def is_valid_move(self, column):
        if not (0 <= column < 7):
            return False
        return self.board[0][column] == 0

    def make_move(self, column):
        if not self.is_valid_move(column) or self.winner is not None:
            return

        for row in range(5, -1, -1):
            if self.board[row][column] == 0:
                self.board[row][column] = self.current_player
        
                if self.check_winner(row, column):
                    self.winner = self.current_player
                else:
                    self.current_player = 3 - self.current_player
                return

    def check_winner(self, row, col):
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        results = [self.check_line(row, col, dr, dc) for dr, dc in directions]
        return any(results)

    def check_line(self, row, col, dr, dc):
        count = 0
        row = row - dr * 3
        col = col - dc * 3
        for _ in range(7):
            if 0 <= row < 6 and 0 <= col < 7 and self.board[row][col] == self.current_player:
                count += 1
                if count == 4:
                    return True
            else:
                count = 0
            row += dr
            col += dc

        return False