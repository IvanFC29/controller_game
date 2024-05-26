#importamos librerias 
import speech_recognition as sr
import pyautogui

def reconocer():
    reconocedor = sr.Recognizer()
    with sr.Microphone() as source:
        print("Di algo....")
        audio = reconocedor.listen(source)
        try:
            texto = reconocedor.recognize_google(audio)
            print(f"Tu dijiste: {texto}")
            return texto
        except sr.UnknownValueError:
            print("Google no pudo entender")
            return None
        except sr.RequestError as e:
            print(f"Fallo al conectar{e}")
            return None
        
def ejecutar_comandos(comando):
    if comando == "uno":
        pyautogui.press('space')
    elif comando == "bebe":
        pyautogui.press("right")
    elif comando == "a":
        pyautogui.press("left")
    else:
        print(f"El comando {comando} no fue reconocido")
        
if __name__ == "__main__":
    while True:
        comando = reconocer()
        if comando:
            ejecutar_comandos(comando.lower())