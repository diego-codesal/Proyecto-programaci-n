import pyxel

class Camion:
    """Representa el camion que recoge los paquetes.
    Vamos a poner la posicion en la que se encuentra y la cantidad de paquetes
    que va a ir almacenando"""
    def __init__(self,x,y):
        self._x = x
        self._y = y
        self.sprite = (2, 48, 120, 40, 32)

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
            colkey=13
        )

    # ---------- Métodos para sprints posteriores ----------
    def agregar_paquete(self):
        """
        Luigi entregó un paquete al camión.
        """
        self._paquetes += 1

    def paquetes_cargados(self):
        return self._paquetes

    def lleno(self):
        """
        Devuelve True si tiene 8 paquetes (Sprint 4).
        """
        return self._paquetes >= 8

    def mandar_a_reparto(self):
        """Se usará en Sprint 4."""
        self._en_reparto = True

    def volver_del_reparto(self):
        """Se usará en Sprint 4."""
        self._en_reparto = False
        self._paquetes = 0