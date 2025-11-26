class Personaje:
    """Esta clase es un ejemplo sencillo de cómo representar un personaje para el proyecto final.
    Este personaje sólo se mueve horizontalmente."""

    def __init__(self, x_fijo: int, pisos_y: list[int], piso_inicial: int, sprite: tuple):
        """
        :param x_fijo: columna X donde estará siempre (debajo de su escalera)
        :param pisos_y: lista con las coordenadas Y de cada piso [piso0, piso1, ...]
        :param piso_inicial: índice del piso donde empieza (0 = abajo)
        :param sprite: tupla (img, u, v, w, h)
        """
        self._pisos_y = pisos_y
        self.sprite = sprite
        self.x = x_fijo
        self.piso = piso_inicial   # 0..len(pisos_y)-1

        self._actualizar_y()

    # Creando properties y setters para los atributos del personaje
    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @x.setter
    def x(self, x: int):
        if not isinstance(x, int):
            raise TypeError ("La x debe ser un entero " + str(type(x)))
        elif x < 0:
            raise ValueError("LA x no debe ser un número negativo")
        else:
            self.__x = x

    @y.setter
    def y(self, y: int):
        if not isinstance(y, int):
            raise TypeError ("La y debe ser un entero " + str(type(y)))
        elif y < 0:
            raise ValueError("La y debe ser un número negativo")
        else:
            self.__y = y

    def _actualizar_y(self):
        """Coloca al personaje en la Y correcta según el piso actual."""
        altura = self.sprite[4]
        # el personaje se apoya sobre el piso: y del piso - altura del sprite
        self.__y = self._pisos_y[self.piso] - altura

    def subir(self):
        """Sube un piso si no está en el de arriba del todo."""
        if self.piso < len(self._pisos_y) - 1:
            self.piso += 1
            self._actualizar_y()

    def bajar(self):
        """Baja un piso si no está en el de abajo del todo."""
        if self.piso > 0:
            self.piso -= 1
            self._actualizar_y()