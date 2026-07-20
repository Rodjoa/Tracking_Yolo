import cv2


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
cut_image = img[0:80, 0:300]

cv2.imshow("Cut image",cut_image)
cv2.imshow("Original image", img)

cv2.waitKey(0)