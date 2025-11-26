import pyxel

class ElementosSecundarios:
    class PrimeraCinta:
        def __init__(self):
            self.sprite = (1,0,0,48,32)
            pyxel.blt(256, 100, *self.sprite)