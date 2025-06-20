class Shield():
    def __init__(self):
        self.amount = 0
        self.cd = 0
        
    def get_shield(self):
        return self.amount

    def increase_shield(self, x):
        self.amount += x
        
    def decrease_shield(self, x):
        self.amount -= x
        
    def get_cd(self):
        return self.cd
    
    def increse_cd(self, x):
        self.cd = x
    
    def decrease_cd(self, dt, x):
        self.cd -= dt * x
    
    # random na svakih X sekundi da padne shield
    # treba da padne od gore negde izmedju x0 i xMax
    # add shield sprite
    # collision sa igracem .kill()
    