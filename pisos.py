import pyxel

class Pisos:
    def __init__(self, indice, y, x_inicio, x_fin):
        """
        indice   -> número de piso (0, 1, 2, ...)
        y        -> coordenada vertical donde dibujar el piso
        x_inicio -> desde dónde empieza el suelo en X
        x_fin    -> hasta dónde llega el suelo en X
        sprite   -> tupla (img, u, v, w, h) del trozo de suelo
        """
        self._indice = indice
        self._y = y
        self._x_inicio = x_inicio
        self._x_fin = x_fin
        self.sprite = (0, 0, 16, 90, 5)

    @property
    def indice(self):
        return self._indice

    @property
    def y(self):
        return self._y

    @property
    def x(self):
        return self._x

    def draw(self):
        """
        Dibuja el piso repitiendo el sprite desde x_inicio hasta x_fin.
        """
        x = self._x_inicio
        while x < self._x_fin:
            pyxel.blt(
                x,
                self._y,
                *self.sprite
            )
            x += self.sprite[3]

    @staticmethod
    def crear_columna(pisos_y, x_inicio, x_fin):
        pisos = []
        for i, y in enumerate(pisos_y):
            pisos.append(Pisos(indice=i, x_inicio=x_inicio, y=y, x_fin=x_fin))
        return pisos

    @staticmethod
    def siguiente_piso(indice_actual: int, tipo: str, direccion: str) -> int:
        """
        Devuelve el índice del siguiente piso al que puede ir el personaje,
        según el tipo ('luigi' o 'mario') y la dirección ('subir'/'bajar').

        Si no puede moverse más en esa dirección, devuelve indice_actual.
        """
        # índices de piso permitidos para cada personaje
        if tipo == "luigi":
            validos = [0, 2, 4]  # pisos 1, 3 y 5
        else:  # 'mario'
            validos = [0, 1, 3]  # pisos 1, 2 y 4

        # si por lo que sea el índice actual no está en la lista, no hacemos nada
        if indice_actual not in validos:
            return indice_actual

        pos = validos.index(indice_actual)

        if direccion == "subir":
            if pos < len(validos) - 1:
                return validos[pos + 1]
        elif direccion == "bajar":
            if pos > 0:
                return validos[pos - 1]

        # si no se puede mover, se queda donde está
        return indice_actual
