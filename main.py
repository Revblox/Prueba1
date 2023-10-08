import cv2
import pytesseract
from gtts import gTTS
import pygame

cuadro = 100
anchocam, altocam = 640,480
tamano_deseado = (anchocam, altocam)
cap = cv2.VideoCapture(0)
cap.set(3, anchocam)
cap.set(4, altocam)
exit_flag = False

def text(image):
    def voz(archi_text, lenguaje, nom_archi):
        with open('info.txt', "r") as lec:
            lectura = lec.read()

        if not lectura:
            lectura = "Intenta de nuevo."
            
             
        lect = gTTS(text=lectura, lang= lenguaje, slow=False)
        nombre = nom_archi
        lect.save(nombre)

    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Valde\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    texto = pytesseract.image_to_string(gris)
    print(texto)
    dire = open('info.txt', "w")
    dire.write(texto)
    dire.close()
    audio = "audio.mp3"
    voz("info.txt", "es", audio)
    pygame.mixer.init()
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)

    pygame.mixer.quit()


def exit_callback(event, x, y, flags, param):
    global exit_flag
    if event == cv2.EVENT_LBUTTONDOWN:
        exit_flag = True

# Create an OpenCV window and set the mouse callback
cv2.namedWindow("Lector inteligente")
cv2.setMouseCallback("Lector inteligente", exit_callback)

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, tamano_deseado)
    if ret == False:
        break
    cv2.putText(frame, 'Ubique aqui el texto a leer', (105, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 204, 255), 1)
    cv2.rectangle(frame, (cuadro, cuadro), (anchocam - cuadro, altocam - cuadro), (0, 204, 255), 2)
    x1, y1 = cuadro, cuadro
    ancho, alto = (anchocam - cuadro) - x1, (altocam - cuadro) - y1
    x2, y2 = x1 + ancho, y1 + alto
    doc = frame[y1:y2, x1:x2]

    cv2.imshow("Lector inteligente", frame)
    t = cv2.waitKey(1)

    if t == 27 or exit_flag:
        break

text(doc)
cap.release()
cv2.destroyAllWindows()





