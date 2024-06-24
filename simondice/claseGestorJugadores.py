import os
import json
from .claseJugador import Jugador

class GestorJugadores:
    def __init__(self):
        self.__jugadores = []

    def agregarJugador(self, jugador):
        self.__jugadores.append(jugador)

    def cargarJugadores(self):
        ruta_archivo = os.path.join(os.path.dirname(__file__), 'pysimonpuntajes.json')
        if os.path.exists(ruta_archivo):
            with open(ruta_archivo, 'r') as archi:
                data = json.load(archi)
            for jug in data['jugadores']:
                self.agregarJugador(Jugador(jug['jugador'], jug['fecha'], jug['hora'], jug['puntaje']))
            archi.close()

    def __str__(self):
        s = ''
        for jug in self.__jugadores:
            s += str(jug) + '\n'
        return s

    def get_jugadores(self):
        return self.__jugadores

    def toJson(self):
        d = dict(
            jugadores = [jug.toJson() for jug in self.__jugadores]
        )
        return d

    def guardarJSONArchivo(self, dic):
        ruta_archivo = os.path.join(os.path.dirname(__file__), 'pysimonpuntajes.json')
        with open(ruta_archivo, 'w') as archi:
            json.dump(dic, archi, indent=4)
