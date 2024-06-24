import threading
import time
from pynput.keyboard import Controller, Key
import noisereduce as nr
import soundfile as sf

import entrenar
import grabador
# Importa la clase de la aplicación Simon dice
from simondice.app import Aplicacion  


keyboard = Controller()
app = None  # Variable global para la aplicación

# Funcion para reducir ruido
def reducir_ruido(file, sr):
    try:
        audio_data, _ = sf.read(file)
        reducido = nr.reduce_noise(y=audio_data, sr=sr)
        print('Se redujo ruido del entorno...')
        sf.write(file, reducido, sr)
    except Exception as e:
        print(f'No hubo ruido que reducir {e}')

# Funcion para ejecutar comandos
def ejecutar_comandos(comando):
    global app  # Accede a la variable global 'app'

    comandos = {
        'presionar verde': 0,
        'presionar rojo': 1,
        'presionar amarillo': 2,
        'presionar azul': 3,
        'iniciar juego': 'enter'
    }

    if comando.lower() == 'iniciar juego':
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        print(f'Se presionó el botón "Start"')
    else:
        index = comandos.get(comando.lower())
        if index is not None:
            app.presionar_boton(index)
            print(f'Se presionó el botón de color {comando}')
        else:
            print(f'El comando "{comando}" no fue encontrado')

# Función para ejecutar la aplicación Tkinter en un hilo separado
def run_tk_app():
    global app  # Accede a la variable global 'app'
    app = Aplicacion()
    app.__ventana.mainloop()

if __name__ == "__main__":
    print('Abriendo juego Simon Dice')

    # Iniciar el hilo de la aplicación Tkinter
    tk_thread = threading.Thread(target=run_tk_app)
    tk_thread.start()

    # Esperar un breve momento para asegurarse de que la ventana Tkinter está inicializada
    time.sleep(2)  # Ajusta el tiempo según sea necesario

    print('Comienza a jugar con tu voz :)')
    n = 1
    while n < 3:
        # Funcion para cargar audio del microfono
        grabador.cargar_audio()
        reducir_ruido('audio.wav', 16000)
        comando = entrenar.reconocer('audio.wav', sr=16000)
        print(f'El comando es: {comando}')
        if comando:
            ejecutar_comandos(comando)
        else:
            print(f'No se encontró el comando {comando}')
        n += 1
