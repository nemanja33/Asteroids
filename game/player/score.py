class Score():
    def __init__(self):
        self.score = 0
        
    def set_score(self, value):
        self.score += value

    def get_score(self):
        return self.score
