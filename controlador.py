import entrenar 
import pyautogui as ag
import noisereduce as nr
import pyaudio
import numpy as np

#Funcion para cargar audio del microfono
def cargar_audio(duracion=3, sr=16000):
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
        return audio_data
    except Exception as e:
       print(f'error al grabar audio{e}')
       return None
   
#Funcion para reducir ruido
def reducir_ruido(audio_data, sr):
    try:
        reducido = nr.reduce_noise(y=audio_data, sr=sr)
        print('Se redujo ruido del entorno...')
        return reducido
    except Exception as e:
        print(f'No hubo ruido que reducir {e}')
        return audio_data
    
#Funcion para ejecutar comandos
def ejecutar_comandos(comando):
    comandos = {
        'iniciar juego': 'enter',
        'avanza adelante': 'right',
        'regresa atras': 'left',
        'abajo cubrete': 'down',
        'golpe elevado': 'a',
        'golpe directo': 's',
        'un salto': 'z',
        'sacar espada': 'x'
    }

    tecla = comandos.get(comando.lower())
    if tecla:
        ag.press(tecla)
        print(f'Se presiono tecla {tecla}')
    else:
        print(f'El comando "{comando}" no fue encontrado')


if __name__ == "__main__":
    print('Comienza a jugar con tu voz :)')
    while True:
        entrada = cargar_audio()
        if entrada is not None:
            audio = reducir_ruido(entrada, 16000)
            comando = entrenar.reconocer(audio,sr=16000)
            print(comando)
            print(f'Ejecutando comando {comando}')
            if comando:
                ejecutar_comandos(comando)
            else:
                print(f'No se encontro el comando {comando}')
        else:
            print('No se capturo nada con el microfono')