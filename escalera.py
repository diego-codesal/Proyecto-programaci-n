import pyxel

class Escalera:
    """
    Representa una escalera entre dos pisos.
    Dibuja el sprite repetido en vertical entre y_top y y_bottom.
    """
    SPRITE = (0, 4, 32, 8, 12)  # (img, u, v, w, h)
    ALTURA_PISO = 5  # alto del sprite del piso
    MARGEN_Y = 2  # hueco vertical
    MARGEN_X = 12  # hueco horizontal

    def __init__(self, x, y_top, y_bottom):
        """
        x        -> coordenada X de la escalera (columna fija)
        y_top    -> y del piso superior
        y_bottom -> y del piso inferior
        sprite   -> (img, u, v, w, h)
        """
        self.x = x
        self.y_top = y_top
        self.y_bottom = y_bottom
        self.sprite = (0, 4, 32, 8, 12)  # (img, u, v, w, h)

    def draw(self):
        y = self.y_top
        # vamos bajando hasta el piso de abajo
        while y < self.y_bottom:
            pyxel.blt(self.x, y,*self.sprite,colkey=0)
            y += self.sprite[-1]

    @staticmethod
    def crear_lado_luigi(pisos_y, pisos_izq, indices_tramos=(1, 3), margen_y=2, margen_x=12):
        escaleras = []
        w = Escalera.SPRITE[3]
        x_izq = pisos_izq[0]._x_inicio - w - margen_x

        for i in indices_tramos:
            y_abajo = pisos_y[i]
            y_arriba = pisos_y[i + 1]
            y_top = y_arriba + Escalera.ALTURA_PISO + margen_y
            y_bottom = y_abajo - Escalera.ALTURA_PISO - margen_y
            escaleras.append(Escalera(x_izq, y_top, y_bottom))
        return escaleras

    @staticmethod
    def crear_lado_mario(pisos_y, pisos_der, indices_tramos=(0, 2), margen_y=2, margen_x=12):
        escaleras = []
        x_der_base = pisos_der[0]._x_fin + margen_x

        for i in indices_tramos:
            y_abajo = pisos_y[i]
            y_arriba = pisos_y[i + 1]
            y_top = y_arriba + Escalera.ALTURA_PISO + margen_y
            y_bottom = y_abajo - Escalera.ALTURA_PISO - margen_y
            escaleras.append(Escalera(x_der_base, y_top, y_bottom))
        return escaleras