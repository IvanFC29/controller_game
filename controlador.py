from pynput.keyboard import Controller, Key
import noisereduce as nr
import soundfile as sf
import entrenar
import grabador

keyboard = Controller()

# Funcion para reducir ruido
def reducir_ruido(file, sr):
    try:
        audio_data, _ = sf.read(file)
        reducido = nr.reduce_noise(y=audio_data, sr=sr)
        print('Se redujo ruido del entorno...')
        sf.write(file, reducido, sr)
    except Exception as e:
        print(f'No hubo ruido que reducir {e}')

# Función para ejecutar comandos
def ejecutar_comandos(comando):
    comandos = {
        'presionar verde': 'v',
        'presionar rojo': 'r',
        'presionar amarillo': 'm',
        'presionar azul': 'a',
        'iniciar juego': Key.enter,
        'guardar jugador': Key.ctrl_l
    }

    tecla = comandos.get(comando.lower())
    if tecla:
        keyboard.press(tecla)
        keyboard.release(tecla)
        print(f'Se presionó la tecla para {comando}')
    else:
        print(f'El comando "{comando}" no fue encontrado')



if __name__ == "__main__":
    print('Comienza a jugar con tu voz :)')
    while True:
        # Funcion para cargar audio del microfono
        grabador.cargar_audio()
        reducir_ruido('audio.wav', 16000)
        comando = entrenar.reconocer('audio.wav', sr=16000)
        print(f'El comando es: {comando}')
        if comando:
            ejecutar_comandos(comando)
        else:
            print(f'No se encontró el comando {comando}')

