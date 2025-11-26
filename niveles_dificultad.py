class NivelDificultad:
    def __init__(self, nombre, vel_cintas, tiempo_spawn, puntos_paquete):
        self.nombre = nombre
        self.vel_cintas = vel_cintas          # píxeles/frame
        self.tiempo_spawn = tiempo_spawn      # frames entre paquetes nuevos
        self.puntos_paquete = puntos_paquete  # puntuación por paquete correcto

    """Para configurar la dificultad:
    self.niveles = {
    "FACIL": NivelDificultad(
        nombre="Fácil",
        vel_cintas=1,
        tiempo_spawn=90,        # cada 90 frames (~1.5 segundos)
        puntos_paquete=10,
    ),
    "MEDIO": NivelDificultad(
        nombre="Medio",
        vel_cintas=2,
        tiempo_spawn=60,
        puntos_paquete=15,
    ),
    "DIFICIL": NivelDificultad(
        nombre="Difícil",
        vel_cintas=3,
        tiempo_spawn=40,
        puntos_paquete=20,
    ),
}
self.nivel_actual = self.niveles["FACIL"]"""