import sounddevice as sd
import wavio

def cargar_audio(duracion=3, sample_rate = 44100):
    #grabación
    print('Grabando....')
    audio = sd.rec(int(duracion*sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    print('Grabacion terminada')
    
    wavio.write('audio.wav', audio, sample_rate, sampwidth=2)
    print('Archivo guardado')
    
"""
if __name__ == "__main__":
    cargar_audio()
"""