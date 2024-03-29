import time

class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.pNames = [None, None]
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.countdown = None
        self.wins = [0, 0]
        self.ties = 0
        self.start_time = None
        self.move_times = [None, None]

    def get_player_move(self, p):
        return self.moves[p]

    def set_player_name(self, player, name):
        self.pNames[player] = name

    def get_player_name(self, p):
        return self.pNames[p]

    def set_countdown(self, count):
        self.countdown = count

    def get_countdown(self):
        return self.countdown
    
    def get_player_response_times(self, p):
        return self.move_times[p]

    def start_timer(self):
        self.start_time = time.time()

    def get_elapsed_time(self):
        if self.start_time:
            return time.time() - self.start_time
        else:
            return 0

    def play(self, player, move):
        self.moves[player] = move
        self.move_times[player] = int(time.time() - self.start_time)
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
