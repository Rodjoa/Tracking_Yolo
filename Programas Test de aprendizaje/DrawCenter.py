from ultralytics import YOLO
import cv2

model = YOLO("yolo11n.pt")

source = "inputs/ball.jpg"

results = model(source) #Aplica el modelo a la fuente (foto o video) y nos devuelve los resultados

for result in results:  #Puede ser muchas fotos asi que busca para cada resultado entre todos los resultados

    # Imagen original
    img = result.orig_img.copy()   # Hace una copia de la imagen original del respectivo resultado

for box in result.boxes:    #Recorre todas las cajas "segmentadoras" (tbn estan en los resultados)

    cx, cy, w, h = box.xywh[0].tolist()

    cv2.circle(img, (int(cx), int(cy)), 5, (0,0,255), -1)

cv2.imshow("Centros", img)
cv2.waitKey(0)
cv2.destroyAllWindows()