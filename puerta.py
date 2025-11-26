import pyxel

class Puerta:
    def __init__(self, x, y):
        self.x = 497
        self.y = 175
        self.sprite = (0,0,104,16,25)  # (img,u,v,w,h)

    def draw(self):
        pyxel.blt(self.x, self.y, *self.sprite)