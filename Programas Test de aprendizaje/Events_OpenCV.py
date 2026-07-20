import cv2
import numpy as np

#======== Obtenemos el directorio con todos los eventos de Open CV =========
#events=[i for i in dir(cv2) if "EVENT" in i]
#for i in events:
#    print(i)

    #EVENT_MBUTTONDBLCLK Pareciera ser el evento click de mouse


import cv2
import numpy as np

prevX,prevY=-1,-1
def Mouse_Callback(event, x, y, flags, params):
    global prevX,prevY
    if event==cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img,(x,y),3,(255,255,255),-1)
        strXY='('+str(x)+','+str(y)+')'
        font=cv2.FONT_HERSHEY_PLAIN
        cv2.putText(img,strXY,(x+10,y-10),font,1,(255,255,255))

        print("coordenadas: ", x," , ", y)

        if prevX==-1 and prevY==-1:
            prevX,prevY=x,y
        else:
            cv2.line(img,(prevX,prevY),(x,y),(0,0,255),5)
            prevX,prevY=-1,-1
        cv2.imshow("image",img)
img = np.zeros((300,300,3),dtype=np.uint8)
cv2.imshow("image",img)
cv2.setMouseCallback("image", Mouse_Callback)
cv2.waitKey()
cv2.destroyAllWindows()   

#Al llenar las lineas le exigiremos tener dos componentes, sino no se guarda
#Le pediremos que presione la tecla enter (para prototipar cualquier tecla) para hacer set frame 0 y entrar al bucle de video