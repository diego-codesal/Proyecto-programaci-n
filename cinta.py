import pyxel

class Cinta:
    def __init__(self, piso, x_inicio, x_fin, sentido, lado):
        self.piso = piso          # índice de piso 0..4
        self.x_inicio = x_inicio
        self.x_fin = x_fin
        self.sentido = sentido    # +1 derecha, -1 izquierda
        self.lado = lado          # "luigi" o "mario"
        self.velocidad = 0
        self.activa = True
        self.sprite = (0, 16, 40, 40, 5)  # ejemplo

    def draw(self, y):
        pyxel.blt(256, 200, *self.sprite)

    @staticmethod
    def crear_para_pisos(pisos, lado, sentido):
        cintas = []
        for piso in pisos[1:]:   # por ejemplo, de piso 1 a 4
            cintas.append(
                Cinta(
                    piso=piso.indice,
                    x_inicio=piso._x_inicio,
                    x_fin=piso._x_fin,
                    sentido=sentido,
                    lado=lado,
                )
            )
        return cintas
