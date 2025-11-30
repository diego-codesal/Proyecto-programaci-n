from personaje import Personaje
from camion import Camion
from pisos import Pisos
import pyxel
from paquete import Paquete


class Tablero:
    """Esta clase contiene un simple tablero"""

    def __init__(self, ancho: int, alto: int):
        """ Método que crea el tablero
        :param ancho: El ancho del tablero
        :param alto: El alto del tablero
        """

        self.pantalla = "juego"


        # Estableciendo los atributos
        self.puntuacion = 0  # puntos del jugador
        self.fallos = 0  # errores cometidos
        self.max_fallos = 3
        self.escalera = []
        self.ancho = ancho
        self.alto = alto

        self.pisos_y = [225, 200, 175, 150, 125]

        self.pisos_luigi = Pisos(2,0,153,243,(0, 0, 251, 90, 5))
        self.pisos_luigi = self.pisos_luigi.crear_columna(self.pisos_y,153,243,(0, 0, 251, 90, 5))


        self.pisos_mario = Pisos(1, 0, 269, 359, (0, 0, 128, 90, 5))
        self.pisos_mario = self.pisos_mario.crear_columna(self.pisos_y, 269, 359, (0, 0, 128, 90, 5))

        self.piso_inicial = Pisos(0, 225, 425, 495, (0, 0, 251, 70, 5))
        self.camion = Camion(10,132,(2, 16, 8, 80, 53,13),(2,96,245,15,11,6))


        # Luigi y Mario empiezan en el piso 0 (el de abajo deltodo)
        self.luigi = Personaje(
            x_fijo=117,
            pisos_y=self.pisos_y,
            piso_inicial=0,
            tipo="luigi",
            sprite_idle_p0=(2, 0, 176, 27, 29, 6),  # idle manos derecha
            sprite_coger_otro=(2, 56, 176, 32, 29, 6),  # subir caja (manos arriba)
            sprite_tirar_camion=(0, 74, 64, 18, 21, 0),  # sprite tirando al camión
        )

        self.mario = Personaje(
            x_fijo=375,
            pisos_y=self.pisos_y,
            piso_inicial=0,
            tipo="mario",
            sprite_idle_p0=(1,144,200,40,29,6), # piso 0, manos derecha
            sprite_idle_otro=(1, 0, 200, 30, 29, 6),  # pisos 2/4, manos izquierda
            sprite_coger_p0=(1, 48, 200, 28, 29, 6),  # piso 0, cogiendo lateral
            sprite_coger_otro=(1, 48, 200, 28, 29, 6),  # pisos 2/4, subiendo caja
        )
        self.mario.y = 222

        self.luigi_piso = 0  # empieza en piso 1
        self.mario_piso = 0  # empieza en piso 1

        self.separacion_medio = [232,85,[2,200,78,47,173]]
        self.ventana = [350, 75, [0, 200, 70, 42, 28]]
        self.maquina=[450, 200, [1, 192, 152, 64, 64]]
        self.sujeta_cinta=[425, 230, [2, 144, 165, 19, 27]]
        self.caja_fusibles = [485, 120, [0, 24, 208, 32, 32]]

        # Lista de paquetes (cajas)
        # Lista de paquetes
        self.paquetes: list[Paquete] = []

        # temporizador para generar paquetes nuevos
        self._contador_spawn = 0
        self._spawn_interval = 360
        self.paquetes.append(self._crear_paquete())



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

    def _crear_paquete(self) -> Paquete:
        """
        Crea un paquete nuevo en la cinta inicial (cinta 0),
        con los sprites que ya estabas usando.
        """
        return Paquete(
            piso=self.piso_inicial,
            sprite_normal=(2, 0, 251, 15, 5,6),
            direccion=-1, # -1 = hacia la izquierda
            sprite_anim=(2,24,232,16,16,6),
            sprite_anim2=(2, 0, 251, 15, 5,6)
        )

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # --- 1) MANEJO DE GAME OVER ANTES DE NADA ---
        if self.pantalla == "game_over":
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.reiniciar_partida()
            return

        # --- 2) SI YA HAS ALCANZADO 3 FALLOS, ACTIVAR GAME OVER ---
        if self.fallos >= self.max_fallos:
            self.pantalla = "game_over"
            return

        # --- 3) LÓGICA NORMAL DEL JUEGO ---
        ALTURA = 29

        # ---- LUIGI: W/S ----
        if pyxel.btnp(pyxel.KEY_W):
            self.luigi_piso = self.pisos_luigi[0].siguiente_piso(self.luigi_piso, "luigi", "subir")
            self.luigi.y = self.pisos_y[self.luigi_piso] - ALTURA

        if pyxel.btnp(pyxel.KEY_S):
            self.luigi_piso = self.pisos_luigi[0].siguiente_piso(self.luigi_piso, "luigi", "bajar")
            self.luigi.y = self.pisos_y[self.luigi_piso] - ALTURA

        # ---- MARIO: ↑/↓ ----
        if pyxel.btnp(pyxel.KEY_UP):
            self.mario_piso = self.pisos_mario[0].siguiente_piso(self.mario_piso, "mario", "subir")
            self.mario.y = self.pisos_y[self.mario_piso] - ALTURA
            self.mario.x = 367
            self.mario.piso = self.mario_piso
            if self.mario.estado == "idle":
                self.mario._actualizar_sprite_idle()

        if pyxel.btnp(pyxel.KEY_DOWN):
            self.mario_piso = self.pisos_mario[0].siguiente_piso(self.mario_piso, "mario", "bajar")
            if self.mario_piso == 0:
                self.mario.y = 222
                self.mario.x = 375
            else:
                self.mario.y = self.pisos_y[self.mario_piso] - ALTURA
            self.mario.piso = self.mario_piso
            if self.mario.estado == "idle":
                self.mario._actualizar_sprite_idle()

        # --- SPAWN DE PAQUETES ---
        self._contador_spawn += 1
        if self._contador_spawn >= self._spawn_interval:
            self._contador_spawn = 0
            self.paquetes.append(self._crear_paquete())

        # --- ACTUALIZAR PAQUETES ---
        for p in self.paquetes:
            p.update(self)

        self.mario.update_anim()
        self.luigi.update_anim()

    def paquete_llega_al_final(self, paquete: Paquete):
        """
        De momento, cuando la caja llega al final de su cinta:
        - solo la frenamos (no la borramos ni la movemos).
        Más adelante aquí meteremos la lógica:
        - si mario/luigi están en el sitio -> subir de piso y cambiar de cinta
        - si no -> fallo
        """
        piso_actual = paquete.piso
        if piso_actual == self.piso_inicial:
            if self.mario_piso == 0:
                nuevo_piso = self.pisos_mario[0]

                paquete.empezar_animacion_recogida(
                    tipo="mario",
                    destino_piso=nuevo_piso,
                    destino_direccion=-1,
                    invertir_lado=False,
                    anim_x=409,
                    anim_y=225,
                    anim_x2=360,
                    anim_y2=220,
                    duracion_frames=50,
                    frames_personaje=20,
                )
                return
            else:
                self.fallos += 1
                paquete.empezar_fallo(x_fallo=409,y_fallo=225,blink_total=30,blink_interval=6,sprite_caida=(2,24,232,16,16,6))
                return
        # CINTA 1 (self.pisos_mario[0]) -> CINTA 2 (self.pisos_luigi[0])
        if piso_actual in self.pisos_mario:
            idx_m = self.pisos_mario.index(piso_actual)

            # Solo tratamos el caso de la cinta 1 por ahora
            if idx_m == 0:  # cinta 1
                destino = self.pisos_luigi[0]  # cinta 2
                paquete.aplicar_modificacion(sprite_normal=[2,81,232,15,8,6])
                # pequeña pausa de, por ejemplo, 8 frames
                paquete.empezar_transicion(
                    destino_piso=destino,
                    destino_direccion=paquete.direccion,  # misma dirección
                    invertir_lado=False,  # entra por el lado “normal”
                    duracion_frames=16,
                    )
                return
            elif idx_m == 1:  # cinta 3
                # aquí decides en qué pisos Luigi puede coger de la cinta 2
                # por lo que comentaste: en el piso inferior (luigi_piso == 0)
                if self.mario_piso == 1:
                    destino = self.pisos_mario[2]  # cinta 8

                    # animación igual que con Mario pero usando tipo="luigi"
                    paquete.empezar_animacion_recogida(
                        tipo="mario",
                        destino_piso=destino,
                        destino_direccion=-1,  # normalmente misma dirección
                        invertir_lado=False,  # ajusta si necesitas cambiar lado
                        anim_x=359,
                        anim_y=185,
                        anim_x2=355,
                        anim_y2=167,
                        duracion_frames=50,
                        frames_personaje=20,
                        spriteanim=[2,128,224,16,16,6],
                        spriteanim2=[2,64,248,15,8,6]
                    )
                else:
                    # Luigi no está en su sitio -> fallo, por ahora simplemente desactivamos
                    paquete.empezar_fallo(x_fallo=355,y_fallo=185,blink_total=30,blink_interval=6,sprite_caida=[2,128,224,16,16,6])
                    self.fallos += 1  # si quieres contabilizar fallos

                return
            elif idx_m == 2:  # cinta 1
                destino = self.pisos_luigi[2]  # cinta 2
                paquete.aplicar_modificacion(sprite_normal=[2, 64, 231, 15, 9, 6])
                # pequeña pausa de, por ejemplo, 8 frames
                paquete.empezar_transicion(
                    destino_piso=destino,
                    destino_direccion=paquete.direccion,  # misma dirección
                    invertir_lado=False,  # entra por el lado “normal”
                    duracion_frames=16,
                    )
                return

            elif idx_m == 3:  # cinta 3
                # aquí decides en qué pisos Luigi puede coger de la cinta 2
                # por lo que comentaste: en el piso inferior (luigi_piso == 0)
                if self.mario_piso == 3:
                    destino = self.pisos_mario[4]  # cinta 8

                    # animación igual que con Mario pero usando tipo="luigi"
                    paquete.empezar_animacion_recogida(
                        tipo="mario",
                        destino_piso=destino,
                        destino_direccion=-1,  # normalmente misma dirección
                        invertir_lado=False,  # ajusta si necesitas cambiar lado
                        anim_x=359,
                        anim_y=135,
                        anim_x2=355,
                        anim_y2=114,
                        duracion_frames=50,
                        frames_personaje=20,
                        spriteanim=[2, 144, 219, 21, 21, 6],
                        spriteanim2=[2,80,245,15,11,6]
                    )
                else:
                    # Luigi no está en su sitio -> fallo, por ahora simplemente desactivamos
                    paquete.empezar_fallo(x_fallo=355,y_fallo=135,blink_total=30,blink_interval=6,sprite_caida=[2, 144, 219, 21, 21, 6])
                    self.fallos += 1  # si quieres contabilizar fallos

                return

            elif idx_m == 4:  # cinta 1
                destino = self.pisos_luigi[4]  # cinta 2
                paquete.aplicar_modificacion(sprite_normal=[2, 96, 245, 15, 11, 6])
                # pequeña pausa de, por ejemplo, 8 frames
                paquete.empezar_transicion(
                    destino_piso=destino,
                    destino_direccion=paquete.direccion,  # misma dirección
                    invertir_lado=False,  # entra por el lado “normal”
                    duracion_frames=16,
                    )
                return

            # aquí más adelante podrás meter la lógica para cintas 3,5,7,9...
            # if idx_m == 2:  # cinta 5
            #     ...
        # CINTAS DE LUIGI (2,4,6,8,10)
        if piso_actual in self.pisos_luigi:
            idx_l = self.pisos_luigi.index(piso_actual)

            # ----- CINTA 2 -> LUIGI -> CINTA 4 -----
            if idx_l == 0:  # cinta 2
                # aquí decides en qué pisos Luigi puede coger de la cinta 2
                # por lo que comentaste: en el piso inferior (luigi_piso == 0)
                if self.luigi_piso == 0:
                    destino = self.pisos_luigi[1]  # cinta 4

                    # animación igual que con Mario pero usando tipo="luigi"
                    paquete.empezar_animacion_recogida(
                        tipo="luigi",
                        destino_piso=destino,
                        destino_direccion=+1,  # normalmente misma dirección
                        invertir_lado=False,  # ajusta si necesitas cambiar lado
                        anim_x=140,
                        anim_y=210,
                        anim_x2=150,
                        anim_y2=192,
                        duracion_frames=50,
                        frames_personaje=20,
                        spriteanim=[2,112,224,16,16,6],
                        spriteanim2=[2,81,232,15,8,6]
                    )
                else:
                    # Luigi no está en su sitio -> fallo, por ahora simplemente desactivamos
                    paquete.empezar_fallo(x_fallo=137,y_fallo=210,blink_total=30,blink_interval=6,sprite_caida=(2,112,224,16,16,6))
                    self.fallos += 1  # si quieres contabilizar fallos
                return
            elif idx_l == 1:
                destino = self.pisos_mario[1]  # cinta 3
                paquete.aplicar_modificacion(sprite_normal=[2, 64, 248, 15, 8, 6])
                # pequeña pausa de, por ejemplo, 8 frames
                paquete.empezar_transicion(
                    destino_piso=destino,
                    destino_direccion=paquete.direccion,  # misma dirección
                    invertir_lado=False,  # entra por el lado “normal”
                    duracion_frames=16,
                )
                return
            elif idx_l == 2:  # cinta 6
                # aquí decides en qué pisos Luigi puede coger de la cinta 2
                # por lo que comentaste: en el piso inferior (luigi_piso == 0)
                if self.luigi_piso == 2:
                    destino = self.pisos_luigi[3]  # cinta 8

                    # animación igual que con Mario pero usando tipo="luigi"
                    paquete.empezar_animacion_recogida(
                        tipo="luigi",
                        destino_piso=destino,
                        destino_direccion=+1,  # normalmente misma dirección
                        invertir_lado=False,  # ajusta si necesitas cambiar lado
                        anim_x=140,
                        anim_y=160,
                        anim_x2=150,
                        anim_y2=141,
                        duracion_frames=50,
                        frames_personaje=20,
                        spriteanim=[2, 128, 208, 16, 16, 6],
                        spriteanim2=[2,64,231,15,9,6]
                    )
                else:
                    # Luigi no está en su sitio -> fallo
                    paquete.empezar_fallo(x_fallo=135,y_fallo=160,blink_total=30,blink_interval=6,sprite_caida=(2, 128, 208, 16, 16, 6))
                    self.fallos += 1  # si quieres contabilizar fallos

                return
            elif idx_l == 3:
                destino = self.pisos_mario[3]  # cinta 2
                paquete.aplicar_modificacion(sprite_normal=[2, 80, 245, 15, 11, 6])
                # pequeña pausa de, por ejemplo, 8 frames
                paquete.empezar_transicion(
                    destino_piso=destino,
                    destino_direccion=paquete.direccion,  # misma dirección
                    invertir_lado=False,  # entra por el lado “normal”
                    duracion_frames=16,
                )
                return

            # última cinta de Luigi: tira al camión
            if idx_l == 4:  # suponiendo que self.pisos_luigi[4] es la cinta 10
                if self.luigi_piso == 4:  # piso superior de Luigi (ajusta si es otro índice)
                    DUR_TOTAL = 40
                    DUR_LUIGI = 15

                    # fase 1: paquete en las manos de Luigi
                    anim_x1 = self.luigi.x + 4
                    anim_y1 = self.luigi.y - 2

                    # fase 2: paquete “en vuelo” cerca del camión
                    anim_x2 = self.camion.x + 24  # ajusta donde quieras ver el vuelo
                    anim_y2 = self.camion.y - 8

                    paquete.empezar_animacion_recogida(
                        tipo="luigi",
                        destino_piso=None,  # no hay cinta destino
                        destino_direccion=0,
                        invertir_lado=False,
                        anim_x=anim_x1,
                        anim_y=anim_y1,
                        anim_x2=anim_x2,
                        anim_y2=anim_y2,
                        duracion_frames=DUR_TOTAL,
                        frames_personaje=DUR_LUIGI,
                        accion_personaje="tirar",  # para Luigi.empezar_anim("tirar", ...)
                    )
                else:
                    # Luigi no está -> fallo (parpadeo + explosión abajo)
                    self.fallos += 1
                    x_fallo = self.luigi.x + 4
                    y_fallo = self.luigi.y - 2
                    paquete.empezar_fallo(x_fallo, y_fallo)
                return



    def recolocar_paquete_en_piso(self, paquete, nuevo_piso, invertir_lado: bool = False):
        """
        Coloca el paquete en la nueva cinta.

        - Si invertir_lado=False: lado "normal" según la dirección.
        - Si invertir_lado=True: se pone en el lado contrario.
        """
        paquete.piso = nuevo_piso
        w = paquete.w
        h = paquete.h

        if paquete.direccion > 0:
            # va hacia la derecha
            if not invertir_lado:
                # lado normal: izquierda
                paquete.x = nuevo_piso._x_inicio
            else:
                # lado invertido: derecha
                paquete.x = nuevo_piso._x_fin - w
        else:
            # va hacia la izquierda
            if not invertir_lado:
                # lado normal: derecha
                paquete.x = nuevo_piso._x_fin - w
            else:
                # lado invertido: izquierda
                paquete.x = nuevo_piso._x_inicio

        paquete.y = nuevo_piso.y - h

    def paquete_entregado_en_camion(self, paquete: Paquete):
        """
        Llamada por Paquete.update cuando termina la animación de Luigi tirando el paquete.
        """
        # 1) colocamos una caja en el camión
        colocado = self.camion.recibir_paquete()

        if colocado:
            # 2) sumar puntos
            self.puntuacion += 100
        else:
            # si estuviera lleno y aún así llega un paquete, podría ser fallo,
            # pero eso ya lo decides tú
            pass

        # 3) este paquete ya no circula por cintas
        paquete.activo = False

    def reiniciar_partida(self):
        """Reinicia completamente la partida después del Game Over."""
        self.pantalla = "juego"
        self.puntuacion = 0
        self.fallos = 0

        # Reiniciar posiciones
        self.luigi_piso = 0
        self.mario_piso = 0

        self.luigi.y = self.pisos_y[0] - 29
        self.mario.y = self.pisos_y[0] - 29
        self.mario.x = 375

        # Reiniciar paquetes
        self.paquetes.clear()
        self._contador_spawn = 0

        # Crear paquete inicial
        paquete0 = Paquete(
            piso=self.piso_inicial,
            sprite_normal=(2, 0, 251, 15, 5, 6),
            direccion=-1,
            sprite_anim=(2, 24, 232, 16, 16, 6),
            sprite_anim2=(2, 0, 251, 15, 5, 6)
        )
        self.paquetes.append(paquete0)

    def draw(self):
        """Este es un método pyxel que se ejecuta en cada iteración del juego (cada
        fotograma). Debes poner aquí el código para dibujar los elementos del juego.
        """
        # Borra la pantalla
        if self.pantalla == "game_over":
            pyxel.cls(0)
            pyxel.text(120, 100, "GAME OVER", 8)
            pyxel.text(80, 120, "Has cometido demasiados fallos.", 7)
            pyxel.text(60, 140, "Pulsa ENTER para volver a jugar", 10)
            return

            # ---- DIBUJO NORMAL DEL JUEGO ----

        pyxel.cls(7)
        x = 15

        pyxel.blt(self.separacion_medio[0], self.separacion_medio[1], *self.separacion_medio[2])
        pyxel.blt(self.ventana[0], self.ventana[1], *self.ventana[2])
        pyxel.blt(self.maquina[0], self.maquina[1], *self.maquina[2])
        pyxel.blt(self.sujeta_cinta[0], self.sujeta_cinta[1], *self.sujeta_cinta[2])
        pyxel.blt(self.caja_fusibles[0], self.caja_fusibles[1], *self.caja_fusibles[2])

        #plataforma donde empieza Luigi
        pyxel.blt(85,225,*[0,0,24,50,5])

        #plataforma del piso 3 de luigi
        pyxel.blt(110, 175, *[0, 0, 24, 25, 5])

        #plataforma del piso 5 de luigi
        pyxel.blt(100, 125, *[0, 0, 24, 35, 5])

        #plataforma que se encuentra debajo del camion
        pyxel.blt(0, 185, *[0, 0, 24, 110, 5])

        #pared que separa a luigi de las escaleras
        pyxel.blt(105, 130, *[0, 248, 0, 5, 55])

        #escaleras entre piso 1 y 3 luigi
        pyxel.blt(115,180,*[0,232,32,10,18])

        # escaleras entre piso 3 y 5 luigi
        pyxel.blt(115, 130, *[0, 232, 32, 10, 23])

        #detalle izquierda camion
        pyxel.blt(0, 110, *[0, 250, 175, 5, 75])
        pyxel.blt(0, 105, *[0, 240, 163, 15, 5])

        #dibujo del camion
        self.camion.draw()


        #puerta de luigi
        pyxel.blt(0,225,*[0,16,104,16,24])

        #detalle lado luigi
        pyxel.blt(0,249,*[0,48,184,85,5])
        pyxel.blt(80,230,*[0,0,155,26,21])
        pyxel.blt(105,230,*[0,32,151,26,26])
        pyxel.blt(180, 230, *[0, 32, 151, 26, 26])


        # Dibuja el personaje, los parámetros de pyxel.blt son (x, y, sprite tuple)
        pyxel.blt(self.luigi.x, self.luigi.y, *self.luigi.sprite)

        for p in self.pisos_luigi:
            p.draw()
        for m in self.pisos_mario:
            m.draw()

        #detalles mario
        pyxel.blt(300, 230, *[0, 32, 151, 26, 26])

        #plataforma inicial mario
        pyxel.blt(375, 251, *[0, 0, 24, 35, 5])
        #plataforma 1 de mario
        pyxel.blt(375, 200, *[0, 0, 24, 75, 5])
        #plataforma 2 de mario
        pyxel.blt(375, 150, *[0, 0, 24, 35, 5])
        #escalera 1 mario
        pyxel.blt(382, 205, *[0, 232, 32, 10, 18])
        #escalera 2 mario
        pyxel.blt(382, 155, *[0, 232, 32, 10, 23])
        pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprite)

        pyxel.blt(500, 175, *[0, 16, 104, 16, 24])

        #piso_inicial
        pyxel.blt(425,225,*self.piso_inicial.sprite)

        # dibujar pisos...
        for p in self.pisos_luigi:
            p.draw()
        for m in self.pisos_mario:
            m.draw()

        # ---- DIBUJAR PAQUETES SOBRE LAS CINTAS ----
        for paquete in self.paquetes:
            paquete.draw()

        # personajes...
        pyxel.blt(self.luigi.x, self.luigi.y, *self.luigi.sprite)
        pyxel.blt(self.mario.x, self.mario.y, *self.mario.sprite)


        # ---------- MARCADOR ----------
        pyxel.text(5, 5, f"Puntos: {self.puntuacion}", 7)  # color 7 = blanco
        pyxel.text(5, 15, f"Fallos: {self.fallos}/{self.max_fallos}", 8)

      
