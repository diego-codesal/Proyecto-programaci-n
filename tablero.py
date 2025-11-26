from personaje import Personaje
from camion import Camion
from cinta import Cinta
from pisos import Pisos
from escalera import Escalera
import pyxel
from puerta import Puerta
from plataforma_morada import PlataformaMorada
class Tablero:
    """Esta clase contiene un simple tablero"""

    def __init__(self, ancho: int, alto: int):
        """ Método que crea el tablero
        :param ancho: El ancho del tablero
        :param alto: El alto del tablero
        """
        # Estableciendo los atributos
        self.puntuacion = 0  # puntos del jugador
        self.fallos = 0  # errores cometidos
        self.max_fallos = 3
        self.escalera = []
        self.ancho = ancho
        self.alto = alto

        self.pisos_y = [236, 211, 186, 161, 136]
        self.pisos_luigi = Pisos.crear_columna(self.pisos_y, x_inicio=88, x_fin=128)
        self.pisos_mario = Pisos.crear_columna(self.pisos_y, x_inicio=269, x_fin=350)

        self.escaleras_luigi = Escalera.crear_lado_luigi(self.pisos_y, self.pisos_luigi)
        self.escaleras_mario = Escalera.crear_lado_mario(self.pisos_y, self.pisos_mario)

        x_luigi = self.escaleras_luigi[0].x   # la escalera de la izquierda
        x_mario = self.escaleras_mario[-1].x   # la escalera de la derecha
        # Luigi y Mario empiezan en el piso 0 (el de abajo del todo)
        self.luigi = Personaje(
            x_fijo=x_luigi,
            pisos_y=self.pisos_y,
            piso_inicial=0,
            sprite=(0, 16, 0, 16, 16),  # sprite de Luigi
        )

        self.mario = Personaje(
            x_fijo=x_mario+50,
            pisos_y=self.pisos_y,
            piso_inicial=0,
            sprite=(0, 0, 0, 16, 16),  # sprite de Mario
        )
        self.luigi_piso = 0  # empieza en piso 1
        self.mario_piso = 0  # empieza en piso 1

        ALTURA = 16  # alto del sprite

        # X ya la tienes (de las escaleras)
        self.luigi.y = self.pisos_y[self.luigi_piso] - ALTURA
        self.mario.y = self.pisos_y[self.mario_piso] - ALTURA

        y_plataforma_camion = self.pisos_y[3]  # piso "medio-alto"
        alto_camion = 32  # o Camion.ALTO si lo tienes como constante
        x_camion = 8  # un poco separado del borde izquierdo
        y_camion = y_plataforma_camion - alto_camion
        self.camion = Camion(x_camion, y_camion)

        self.puerta1 = Puerta(245, 208)
        self.puerta2 = Puerta(0, 224)

        self.plataformas_luigi = PlataformaMorada.desde_escaleras(self.escaleras_luigi, lado="luigi")
        self.plataformas_mario = PlataformaMorada.desde_escaleras(self.escaleras_mario, lado="mario")

        # Crear todas las plataformas de Mario
        self.plataformas_mario = PlataformaMorada.desde_escaleras(self.escaleras_mario, lado="mario")
        for p in self.plataformas_mario:
            p.x += 50
            p.y -= 15


        self.cintas_luigi = Cinta.crear_para_pisos(self.pisos_luigi, lado="luigi", sentido=+1)
        self.cintas_mario = Cinta.crear_para_pisos(self.pisos_mario, lado="mario", sentido=-1)

        self.plat_inicio_luigi = PlataformaMorada.bajo_personaje(self.luigi)
        # Ajuste para que NO toque el primer piso naranja
        ancho_plat = self.plat_inicio_luigi.sprite[3]  # 32
        x_inicio_piso_luigi = self.pisos_luigi[0]._x_inicio  # 88
        MARGEN_LUIGI = 4  # hueco que quieres

        self.plat_inicio_luigi.x = x_inicio_piso_luigi - ancho_plat - MARGEN_LUIGI
        self.plat_inicio_mario = PlataformaMorada.bajo_personaje(self.mario)

        self.plat_camion = PlataformaMorada.bajo_objeto(self.camion)






        pyxel.init(self.ancho, self.alto, title="Demo Juego Pyxel")
        # Cargando el fichero pyxres con las imágenes
        pyxel.load("assets/example.pyxres")
        # Ejecutando el juego
        pyxel.run(self.update, self.draw)


    # Properties and setters
    @property
    def ancho(self) -> int:
        return self.__ancho

    @property
    def alto(self) -> int:
        return self.__alto

    @ancho.setter
    def ancho(self, ancho: int):
        if not isinstance(ancho, int):
            raise TypeError("El ancho debe ser un entero " + str(type(ancho)))
        else:
            self.__ancho = ancho

    @alto.setter
    def alto(self, alto: int):
        if not isinstance(alto, int):
            raise TypeError("El alto debe ser un entero " + str(type(alto)))
        elif alto < 1 or alto > 256:
            raise ValueError("El alto debe estar en el rango entre 1 y 256")
        else:
            self.__alto = alto

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        ALTURA = 16

        # ---- LUIGI: W/S ----
        if pyxel.btnp(pyxel.KEY_W):
            self.luigi_piso = Pisos.siguiente_piso(self.luigi_piso, "luigi", "subir")
            self.luigi.y = self.pisos_y[self.luigi_piso] - ALTURA

        if pyxel.btnp(pyxel.KEY_S):
            self.luigi_piso = Pisos.siguiente_piso(self.luigi_piso, "luigi", "bajar")
            self.luigi.y = self.pisos_y[self.luigi_piso] - ALTURA

        # ---- MARIO: ↑/↓ ----
        if pyxel.btnp(pyxel.KEY_UP):
            self.mario_piso = Pisos.siguiente_piso(self.mario_piso, "mario", "subir")
            self.mario.y = self.pisos_y[self.mario_piso] - ALTURA

        if pyxel.btnp(pyxel.KEY_DOWN):
            self.mario_piso = Pisos.siguiente_piso(self.mario_piso, "mario", "bajar")
            self.mario.y = self.pisos_y[self.mario_piso] - ALTURA

    def draw(self):
        """Este es un método pyxel que se ejecuta en cada iteración del juego (cada
        fotograma). Debes poner aquí el código para dibujar los elementos del juego.
        """
        # Borra la pantalla

        pyxel.cls(6)
        # Dibuja el personaje, los parámetros de pyxel.blt son (x, y, sprite tuple)
        pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprite)
        pyxel.blt(self.luigi.x, self.luigi.y, *self.luigi.sprite)
        self.camion.draw()
        for p in self.pisos_luigi:
            p.draw()
        for p in self.pisos_mario:
            p.draw()
        self.puerta1.draw()
        self.puerta2.draw()
        for e in self.escaleras_luigi:
            e.draw()
        for e in self.escaleras_mario:
            e.draw()
        for p in self.plataformas_luigi:
            p.draw()
        for p in self.plataformas_mario:
            p.draw()
        for c in self.cintas_luigi:
            y = self.pisos_y[c.piso]
            c.draw(y)

        for c in self.cintas_mario:
            y = self.pisos_y[c.piso]
            c.draw(y)
        self.plat_inicio_luigi.draw()
        self.plat_inicio_mario.draw()

        self.plat_camion.draw()

        # ---------- MARCADOR ----------
        pyxel.text(5, 5, f"Puntos: {self.puntuacion}", 7)  # color 7 = blanco
        pyxel.text(5, 15, f"Fallos: {self.fallos}/{self.max_fallos}", 8)