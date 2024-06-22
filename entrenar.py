import os
import librosa
from scipy.spatial.distance import euclidean

#definir diccionario
diccionario = ['Iniciar juego',
               'Abajo cubrete',
               'Avanza adelante',
               'Regresa Atras',
               'Golpe elevado',
               'Golpe directo',
               'Un salto',
               'Sacar espada']
     
#carpetas de datos          
carpetas = [
    'plantillas/1',
    'plantillas/2',
    'plantillas/3',
    'plantillas/4',
    'plantillas/5',
    'plantillas/6',
    'plantillas/7',
    'plantillas/8'
]

#Funcion para cargar y extraer MFCC de un archivo de audio
def extraer_frecuencia(file, sr=16000):
    if isinstance(file, str):
        audio, ratio = librosa.load(file, sr=None)
    else:
        audio = file.astype(float)
        ratio = sr
    mfcc = librosa.feature.mfcc(y=audio, sr= ratio, n_mfcc=13)
    #Normalizacion
    mfcc = (mfcc - mfcc.mean()) / mfcc.std()
    return mfcc

def cargar_audios(carpetas, diccionario):
    plantillas = {}
    for i, comando in enumerate(diccionario):
        folder = carpetas[i]
        archivos = []
        
        for f in os.listdir(folder):
            if f.endswith('.wav'):
                archivos.append(os.path.join(folder,f))
                
        plantillas[comando] = []
        for archivo in archivos:
            plantilla_audio = extraer_frecuencia(archivo)
            plantillas[comando].append(plantilla_audio)

    return plantillas
    
#Calcular la distancia Euclidiana entre dos matrices
def distancia_euclediana(mfcc_1, mfcc_2):
    min_length = min(mfcc_1.shape[1], mfcc_2.shape[1])
    mfcc_1 = mfcc_1[:, :min_length].flatten()
    mfcc_2 = mfcc_2[:, :min_length].flatten()
    return euclidean(mfcc_1, mfcc_2)

def reconocer(audio, sr=16000):
    #Cargar plantillas y extraer caracteristicas
    plantillas = cargar_audios(carpetas, diccionario)

    entrada = extraer_frecuencia(audio, sr)
    distancia_min = float('inf')
    
    respuesta = None
    for comando, mfcc_list in plantillas.items():
        for mfcc_plantilla in mfcc_list:
            distancia = distancia_euclediana(entrada, mfcc_plantilla)
            if distancia < distancia_min:
                #actualizar distancia
                distancia_min = distancia
                respuesta = comando

    return respuesta


if __name__ == '__main__':
    test_file = "test_audio.wav"
    comando = reconocer(test_file)
    print(f'El comando es: {comando}')