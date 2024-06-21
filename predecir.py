import pyautogui as ag
import numpy as np
import pyaudio
import noisereduce as nr
import entrenar 
from entrenar import voz_recibido

#Funcion para cargar audio del microfono
def recibir_audio(duracion=3, sr=16000):
    try: 
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=sr, input=True, frames_per_buffer=1024)
        print('Grabando...')
    
        frames = []
        for _ in range(0, int(sr/1024 * duracion)):
            data = stream.read(1024)
            frames.append(data)
        print('Grabacion terminada')    
    
        stream.stop_stream()
        stream.close()
        p.terminate()
    
        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
        return audio_data, sr
    except Exception as e:
       print(f'error al grabar audio{e}')
       return None, sr
        
#Funcion para reducir ruido
def reducir_ruido(audio_data, sr):
    try:
        reducido = nr.reduce_noise(y=audio_data, sr=sr)
        return reducido
    except Exception as e:
        print(f'error al reducir el ruido {e}')
        return audio_data

#Funcion para ejecutar comandos
def ejecutar_comandos(comando):
    comandos = {
        'iniciar juego': 'enter',
        'avanza adelante': 'right',
        'atras regresa': 'left',
        'abajo cubrete': 'down',
        'golpe elevado': 'a',
        'golpe directo': 's',
        'un salto': 'z',
        'sacar espada': 'x'
    }

    tecla = comandos.get(comando.lower())
    if tecla:
        ag.press(tecla)
    else:
        print(f'El comando "{comando}" no fue encontrado')

        
if __name__ == "__main__":
    print('Comienza a jugar con tu voz :)')
    while True:
        audio, sr = recibir_audio()
        if audio is not None:
            audio = reducir_ruido(audio, sr)
            comando = entrenar.reconocer(audio)
            if comando:
                ejecutar_comandos(comando)
                print(f'Ejecutando comando {voz_recibido}')
            else:
                print(f'No se encontro el comando {comando}')
        else:
            print('Error en la grabacion del audio')
            print('No se pudo jugar :(')