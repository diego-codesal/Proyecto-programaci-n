# plataforma_morada.py
import pyxel

class PlataformaMorada:
    SPRITE = (0, 0, 76, 32, 4)

    def __init__(self, x, y,sprite=None):
        self.x = x
        self.y = y
        # sprite del suelo morado
        self.sprite = sprite if sprite else PlataformaMorada.SPRITE

    def draw(self):
        img, u, v, w, h = self.sprite
        pyxel.blt(self.x, self.y, img, u, v, w, h, 0)

    @staticmethod
    def desde_escaleras(escaleras, lado, ajuste_izq=8):
        plataformas = []
        plat_w = PlataformaMorada.SPRITE[3]
        plat_h = PlataformaMorada.SPRITE[4]

        for esc in escaleras:
            wEsc = esc.sprite[3]
            if lado == "luigi":
                # plataforma más hacia el centro
                x_plat = esc.x - (plat_w - wEsc) + ajuste_izq
            else:  # "mario"
                x_plat = esc.x
            y_plat = esc.y_top - plat_h
            plataformas.append(PlataformaMorada(x_plat, y_plat, PlataformaMorada.SPRITE))
        return plataformas

    @classmethod
    def bajo_personaje(cls, personaje):
        """
        Crea una plataforma morada centrada bajo el personaje,
        de modo que el personaje quede apoyado sobre ella.
        """
        plat_w = cls.SPRITE[3]
        plat_h = cls.SPRITE[4]

        char_w = personaje.sprite[3]
        char_h = personaje.sprite[4]

        # centramos la plataforma respecto al personaje
        x = personaje.x + char_w // 2 - plat_w // 2
        # la parte de arriba de la plataforma justo en los pies del personaje
        y = personaje.y + char_h

        return cls(x, y)

    @classmethod
    def bajo_objeto(cls, objeto):
        """
        Crea una plataforma morada debajo de un objeto cualquiera
        (camión, máquina, etc.) usando su sprite para posicionarse.
        """
        plat_w = cls.SPRITE[3]
        plat_h = cls.SPRITE[4]

        obj_w = objeto.sprite[3]
        obj_h = objeto.sprite[4]

        x = objeto.x + obj_w // 2 - plat_w // 2
        y = objeto.y + obj_h

        return cls(x, y)