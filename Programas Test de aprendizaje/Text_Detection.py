import cv2
import pytesseract

# Ruta de Tesseract en Windows (cámbiala si es distinta)
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
source = "Inputs/Texto_Reducido.jpeg"

# Cargar imagen
img = cv2.imread(source)
#img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
#resize:(0,0) -> Tamaño absoluto del destino (dzise). Al ponerle 0 en ancho y alto le indicamos a opencv
#que no use dimensiones fijas, sino que calcule el nuevo tamaño basándose en los 
#factores de escala fx y fy
#fx: Factor de escala horizontal, al ser 0.5 reduce el ancho a la mitad
#fy: Lo mismo anterior pero con la dimensión vertical (alto)
#Todo lo anterior es escalar la imagen


# OCR completo
texto = pytesseract.image_to_string(img)
print(texto)

# Obtener datos de cada palabra
hImg, wImg, _ = img.shape
boxes = pytesseract.image_to_data(img)

for x, b in enumerate(boxes.splitlines()):
    if x != 0:
        b = b.split()

        # Algunas líneas vienen vacías
        if len(b) == 12:
            x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])

            # Dibujar rectángulo
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Dibujar texto detectado
            cv2.putText(
                img,
                b[11],
                (x, y - 10),
                cv2.FONT_HERSHEY_COMPLEX,
                0.7,
                (255, 0, 255),
                2
            )

cv2.imshow('Result', img)
cv2.waitKey(0)