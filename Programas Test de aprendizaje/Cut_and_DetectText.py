import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
source = "Inputs/FotoVideo.jpeg"

# Cargar imagen
img = cv2.imread(source)
#img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
#resize:(0,0) -> Tamaño absoluto del destino (dzise). Al ponerle 0 en ancho y alto le indicamos a opencv
#que no use dimensiones fijas, sino que calcule el nuevo tamaño basándose en los 
#factores de escala fx y fy
#fx: Factor de escala horizontal, al ser 0.5 reduce el ancho a la mitad
#fy: Lo mismo anterior pero con la dimensión vertical (alto)
#Todo lo anterior es escalar la imagen

rows, cols, _ = img.shape
print("Rows: ", rows)
print("Cols: ", cols)

#cut image
cut_image = img[0:50, 0:300]


#========== bloque de deteccion ============
#ChatGPT me recomienda esta linea texto = pytesseract.image_to_string(roi, config='--psm 7'). Despues le echaremos un ojo a ese parámetro de config



# OCR completo
texto = pytesseract.image_to_string(cut_image)
print(texto)
for letter in texto:
    print("word: ",letter,"\n")

# Obtener datos de cada palabra
hImg, wImg, _ = cut_image.shape
boxes = pytesseract.image_to_data(cut_image)

for x, b in enumerate(boxes.splitlines()):
    if x != 0:
        b = b.split()

        # Algunas líneas vienen vacías
        if len(b) == 12:
            x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])

            # Dibujar rectángulo
            cv2.rectangle(cut_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Dibujar texto detectado
            cv2.putText(
                cut_image,
                b[11],
                (x, y - 10),
                cv2.FONT_HERSHEY_COMPLEX,
                0.7,
                (255, 0, 255),
                2
            )

#========== Fin Bloque de detección ===========

cv2.imshow("Cut image",cut_image)
cv2.imshow("Original image", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
