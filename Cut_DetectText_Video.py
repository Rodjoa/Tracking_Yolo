import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

source = "Inputs/OCM/1.mp4"

cap = cv2.VideoCapture(source)

if not cap.isOpened():
    print("Error: Could not open video")
    exit()

# Leer primer frame
success, frame = cap.read()

if success:

    print("Frame capturado")

    # Mostrar frame original
    cv2.imshow("Frame original", frame)

    # Recortar zona fecha/hora
    ROI_DateTime = frame[0:10, 0:85]

    #ROI_DateTime = cv2.resize(
        #ROI_DateTime,
       #None,
       # fx=4,
      #  fy=4,
       # interpolation=cv2.INTER_CUBIC
    #)


    cv2.imshow("ROI fecha hora", ROI_DateTime)

    # OCR
    texto = pytesseract.image_to_string(
        ROI_DateTime,
        config='--psm 7'
    )

    print("Texto detectado:")
    print(texto)


else:
    print("No se pudo leer frame")


cap.release()

cv2.waitKey(0)
cv2.destroyAllWindows()