class Robot():
    def __init__(self):
        self.position = [0,0]
        self.speed=10

    def move_right(self):
        self.position[0] += self.speed

    def move_left(self):
        self.position[0] -= self.speed