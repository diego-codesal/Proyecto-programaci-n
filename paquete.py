import pyxel

class Paquete:
    """Representa el camion que recoge los paquetes.
    Vamos a poner la posicion en la que se encuentra y la cantidad de paquetes
    que va a ir almacenando"""
    def __init__(self,x,y):
        self._x = x
        self._y = y
        self.sprite = (3, 57, 120, 40, 32)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def draw(self):
        """
        Dibuja el camión usando su sprite.
        """
        pyxel.blt(
            self._x,
            self._y,
            *self.sprite,
            colkey=14
        )
