import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import time
from ultralytics import YOLO
from ultralytics.utils.plotting import colors
import random
from collections import defaultdict
import pytesseract
#=== Debug de memoria ===
import psutil
import os
process = psutil.Process(os.getpid())


pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class ObjectTracking:
    """Object Tracking using Ultralytics YOLO26: https://docs.ultralytics.com/models/yolo26/"""

    def __init__(self, model="yolo11s.pt", source= "Inputs/videoluis_cortado.mp4"
    ".mp4"): #yolo11s.pt, yolo11n.pt...Hay diferentes modelos. Hay que ir testeando

        self.model = YOLO(model)  # Model initialization
        self.names = self.model.names  # Store model classes names

        self.counter_frames = 0   # Creamos atributo porque  nos sirve para contar
        self.counter_crossing = 0 # Contamos cuantos cruzan la linea (TOTAL)
        self.line_side = {} # Llave (id): valor (0 o 1) -> Lado actual ->Despues migramos al siguiente nivel con la linea comentada de arriba
        self.counter_crossing_class = {} # Clase: Cantidad de cruces por clase
        self.counter_crossing_line = {} #Contador de cruce para cada linea {0: 5, 1: 4} -> El valor de self.counter_crossing_line[1] es 4
        self.lines = [] #La llenaremos con los datos capturados por el Mouse_Callback(..) 
        self.last_event_by_id = {} # {id_n: {"cruzó linea": n, "fromstate": 0, "to_state": 1}}

        #====== Tabla de movimientos ======= Haremos una tabla diseñada para cada video (debemos hacerlo dibujando el frame)

        #Esta tabla de movimientos debe diseñarse para cada video
        self.movement_table = { #OBS: La llave del diccionario es (1,0,1,2,1,0) y el valor es "Girar derecha" ->{(1,0,2,1): Girar derecha}
            #En nuestro esquema las lineas se definen de derecha a izquierda
            (
                0,0,1,
                1,0,1
            ): "MOV 1",    #Automovil de la pista 1 (Pista 1 solo es en sentido hacia afuera a la pantalla) 1 gira a la derecha
            (
                0,0,1,
                2,0,1
            ): "MOV 2",    #Automovil de la pista 1 sigue recto
            (
                0,0,1,
                3,0,1
            ): "MOV 3",    #Automovil de la pista 1 gira a la izquierda
            (
                4,1,0,
                5,1,0
            ): "MOV 4",    #Automovil de la pista 2 (Pista 2 solo es en sentido hacia dentro a la pantalla) Avanzan recto (no hay curvas)
            
        }

        #Contador para cada movimiento
        self.counter_movement = {}      # Ej: {"movimiento_1": 3, "movimiento_2": 1, "movimiento_3": 1}

        #Detección de Fecha y Hora (OCR)
        #self.ROI_DateTime = im0[0:100, 0:600]   #Región de pixeles que recortaremos para obtener la hora con Tesseract
        self.prev_texto = ''     #Variable util para comparar si el texto cambia respecto al frame anterior (detectar si cambia fecha u hora)
        self.prev_texto = ""
        self.current_date = None
        self.current_time = None
        self.prev_date = None
        self.prev_time = None

        
        #==== Variables del Callback Mouse ==== 
        self.prevX = -1
        self.prevY = -1
        self.P_start = (0,0)
        self.P_end =   (0,0)
        self.number_line = 0 #Variable para numero de linea en el callback
        self.countCalls_to_Mouse_Callback = 0 #verificaremos paridad para ver si cambia la linea o si es el segundo punto de la misma linea

        # ===== Variables para exportación a Excel =====

        #Variables vijas x video después pueden hacerse por input consola al ejecutar
        self.pc = 1
        self.ubicacion = "Interseccion Av. Principal"
        self.comuna = "Viña del Mar"

        #===== Estas variables se sacaran de la detección OCR de texto =====
        self.dia = "Lunes"
        self.fecha = "02/25/2026"
        self.hora = "9:00"
        self.hh = "9"
        self.hhmm = "900"
        self.flujo = 0

        # Lista donde se irán almacenando los registros
        self.registros = []
        self.archivo = "conteo_flujo.xlsx"

        #los registros tienen la forma 
        # registro = {
        #"PC": 1,
        #"UBICACION": "Interseccion Av. Principal",
        #"COMUNA": "Viña del Mar",
        #"DIA": "Lunes",
        #"FECHA": "18-07-2026",
        #"HORA": f"{hora:02d}:{minutos:02d}",
        #"HH": hora,
        #"HHMM": hhmm,
        #"MOV 1": m1,
        #"MOV 2": m2,
        #"MOV 3": m3,
        #"MOV 4": m4,
        #"FLUJO": (m1+m2+m3+m4)
    #}

        # Video capturing module
        self.cap = cv2.VideoCapture(source)
        assert self.cap.isOpened(), "Error reading video file"

        # Video writing module
        w, h, fps = (
            int(self.cap.get(x)) 
            for x in (
                cv2.CAP_PROP_FRAME_WIDTH, 
                cv2.CAP_PROP_FRAME_HEIGHT, 
                cv2.CAP_PROP_FPS))
        self.writer = cv2.VideoWriter(
            "object-tracking.avi",
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps, 
            (w, h)
            )

        self.track_history = defaultdict(lambda: [])  # Store the track history

        # Display settings
        self.rect_width=2
        self.font = 1.0
        self.text_width=2
        self.padding = 12
        self.margin = 10
        self.circle_thickness=5
        self.polyline_thickness=2

        #=== Para tener adaptado dinamico ===
        self.h = h
        self.w = w

        # Window setup
        self.window_name = "YOLO Tracking"
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

    def run(self):
        """Function to run object tracking on video file or webcam."""
        #Podemos crear atributos a la clase ObjectTracking que nos sirvan:
        #self.count_frame = 0

        #Antes del while principal donde se pasan los frames
        #Pondremos el primer frame en pantalla para configurar las lineas
        #Luego setearemos el primer frame (para volver al primer frame sin perderlo)

        success, first_frame = self.cap.read() #success: Estado si se procesó correctamente
        #print("Frame OpenCV:", int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)))
        if not success:
            return

        self.configure_lines(first_frame)

        #print("Antes del set:", int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)))
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        #print("Después del set:", int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)))
    
        # --- Medición de tiempo entre frames ---
        last_loop_time = time.perf_counter()

        while self.cap.isOpened():

            current_time = time.perf_counter()
            delta_ms = (current_time - last_loop_time) * 1000
            last_loop_time = current_time

            success, im0 = self.cap.read()

            if not success:
                break

            fps_real = 1000 / delta_ms if delta_ms > 0 else 0
            print(f"FRAME->{self.counter_frames + 1}: {delta_ms:.1f} ms | FPS REAL: {fps_real:.2f}")

            self.counter_frames += 1

            # ===== OCR DESACTIVADO =====
            # self.current_time, self.current_date = self.get_date_and_time(im0)

            # ===== YOLO PURO =====
            t0 = time.time()

            # ===== YOLO PURO =====
            results = self.model(im0, verbose=False)

            t1 = time.time()
            print(f"YOLO SOLO: {(t1-t0)*1000:.1f} ms")

            if results and len(results) > 0:

                result = results[0]

                if result.boxes is not None:

                    t4 = time.time()

                    boxes = result.boxes.xyxy.cpu()
                    clss = result.boxes.cls.cpu()

                    t5 = time.time()
                    print(f"CPU TRANSFER: {(t5-t4)*1000:.1f} ms")

                    for box, cls in zip(boxes, clss.tolist()):

                        # Solo para visualizar si quieres
                        x1, y1, x2, y2 = box

                        cv2.rectangle(
                            im0,
                            (int(x1), int(y1)),
                            (int(x2), int(y2)),
                            (0, 255, 0),
                            2
                        )

            self.writer.write(im0)
            cv2.imshow(self.window_name, im0)
            

            key = cv2.waitKey(1) & 0xFF
            if key == 13:
                break
            elif key == ord('c'):
                self.selected_id = None
                #print("Selection cleared")

        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        #print("Conteo final:", self.counter_crossing)
        print("Conteo de movimientos:\n")
        print(self.counter_movement)

    

    def draw_lines(self, im0):
        #Creamos todas las lineas en un ciclo for que recorre la linesta self.lines
        #Debemos escribir 0/1 a cada lado de la linea (utilizar la función calculate_line_side(..))

        for numero_linea, (line_start, line_end) in enumerate (self.lines):
            
            x_mid = int((line_start[0]+line_end[0])//2)
            y_mid = int((line_start[1]+line_end[1])//2)

            cv2.line(
                im0,
                line_start,
                line_end,
                (0, 0, 255),   # rojo
                2
            )

            cv2.putText(
                im0,
                f"Línea {numero_linea}",
                (x_mid + 20, y_mid-50),
                cv2.FONT_HERSHEY_PLAIN,
                1,
                (255,255,255),
                1
            )
            P0, P1 = self.get_line_side_points(line_start, line_end, distance=25)
            side_P0 = self.calculate_line_side(P0, line_start, line_end)
            side_P1 = self.calculate_line_side(P1, line_start, line_end)

            cv2.putText(
                im0,
                f"({side_P0})",
                (P0),
                cv2.FONT_HERSHEY_PLAIN,
                1,
                (255,255,255),
                1
            )

            cv2.putText(
                im0,
                f"({side_P1})",
                (P1),
                cv2.FONT_HERSHEY_PLAIN,
                1,
                (255,255,255),
                1
            )






    def configure_lines(self, frame):

        self.img = frame.copy()
        cv2.imshow("Configurar lineas", self.img)
        cv2.setMouseCallback("Configurar lineas", self.Mouse_Callback)
    
        while True:

            key = cv2.waitKey(1) & 0xFF

            #Usamos tecla enter para terminar de ingresar lineas
            if key == 13:
                break

        cv2.destroyAllWindows()
        
      
                           #   a una auxiliar al llamar a la función?
        #======= Fin Bloque INPUTS de lineas ==========

    #============== INICIO BLOQUE CALLBACK DE MOUSE ===============
    def Mouse_Callback(self, event, x, y, flags, params):

        #FIN TESTING
        

        if event==cv2.EVENT_LBUTTONDOWN:
            self.countCalls_to_Mouse_Callback+=1
            if(self.countCalls_to_Mouse_Callback%2 != 0): #Mantenemos el numero de linea para los dos puntos mientras la dibujamos
                self.number_line+=1

            #print("Evento:", event) #Para debug
            cv2.circle(self.img,(x,y),3,(255,255,255),-1)
            #INICIO TESTING
            

            print("coordenadas: ", x," , ", y)
            
        
            if self.prevX ==-1 and self.prevY==-1: #Garantiza que haya nuevo valor
                print("debug 1")
                self.prevX,self.prevY=x,y
                self.P_start = (x,y)
            else:
                self.P_end = (x,y)

                x_mid = (self.P_end[0] + self.P_start[0])//2
                y_mid = (self.P_end[1] + self.P_start[1])//2

                cv2.line(self.img,(self.prevX,self.prevY),(x,y),(0,0,255),5)
                cv2.circle(self.img,(x_mid,y_mid),3,(105,100,0),-1)   #Dibujamos un circulo en medio de la linea para identificar punto medio

                #Acá debemos llamar la función que devuelve 2 puntos con la linea R= (self.prevX,self.prevY),(x,y)
                P0,P1 = self.get_line_side_points((self.prevX,self.prevY), (x,y), distance=30)
                #Ahora vemos de que lado están ambos puntos evaluandolos en la función calculate
                side_P0 = self.calculate_line_side(P0, (self.prevX,self.prevY), (x,y))
                side_P1 = self.calculate_line_side(P1, (self.prevX,self.prevY), (x,y))


                #Dibujar esos dos puntos con su respectivo nombre
                cv2.circle(self.img,(P0[0], P0[1]),3,(105,100,0),-1)   
                cv2.circle(self.img,(P1[0], P1[1]),3,(105,100,0),-1)   

                #Luego dentro de put text ocupar la funcion que entrega el lado en ese punto (escribira un 0 o 1 en cada lado)

                cv2.putText(
                    self.img,
                    f"Linea {self.number_line-1}",
                    (x_mid+40, y_mid-50),
                    #(mid_x + 10, mid_y - 10),
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    (255,255,255),
                    1
                )

                cv2.putText(
                    self.img,
                    f"({x},{y})",
                    (x + 20, y + 20),
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    (255,255,255),
                    1
                )

                cv2.putText(
                    self.img,
                    f"({side_P0})",
                    (P0),
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    (255,255,255),
                    1
                )
                cv2.putText(
                    self.img,
                    f"({side_P1})",
                    (P1),
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    (255,255,255),
                    1
                )



                self.prevX,self.prevY=-1,-1 #Garantiza de que se haya guardado un nuevo valor

                self.lines.append((self.P_start, self.P_end))    #Llenamos la lista de lineas que despues dibujaremos
            cv2.imshow("Configurar lineas", self.img)
 
    #============== FIN BLOQUE CALLBACK DE MOUSE ===============

    #================ Obtener Fecha y hora (OCR) =================
    def get_date_and_time(self, frame):

        ROI_DateTime = frame[0:100, 0:600]

        texto = pytesseract.image_to_string(ROI_DateTime).strip()

        if texto and texto != self.prev_texto:

            try:
                dt = datetime.strptime(texto, '%Y-%m-%d %H:%M:%S')

                self.current_date = dt.date()
                self.current_time = dt.time()

                self.prev_texto = texto

            except ValueError:
                pass

        return  self.current_time, self.current_date

#Uso de bloque try en get_date_and_time(self, frame) 
#Intenta convertirlo. Si no puede porque el formato está malo, no mata el programa; simplemente sigue." -> Fuente de datos puede fallar


  #==== Función que devolverá dos puntos a cada lado de una recta,
    #==== ubicados a una distancia "distance" en el vector ortogonal
    def get_line_side_points(self, line_start, line_end, distance=30):

        # Guardamos las componentes del vector AB de la línea
        dx = line_end[0] - line_start[0]
        dy = line_end[1] - line_start[1]

        # Obtenemos un vector normal a la línea.
        # Esta expresión sale de imponer que el producto punto sea cero:
        # AB · N = 0
        Vector_normal = (-dy, dx)

        # Calculamos el módulo del vector normal para normalizarlo
        modulo = (Vector_normal[0]**2 + Vector_normal[1]**2)**0.5

        # Evitamos división por cero si la línea tiene longitud cero
        if modulo == 0:
            return None, None

        # Normalizamos el vector normal
        nx = Vector_normal[0] / modulo
        ny = Vector_normal[1] / modulo

        # Sacamos el punto medio de la línea
        x_mid = (line_start[0] + line_end[0]) / 2
        y_mid = (line_start[1] + line_end[1]) / 2

        # Obtenemos los puntos a ambos lados de la línea,
        # separados una distancia "distance"
        P0 = (int(x_mid + distance * nx),int(y_mid + distance * ny))
        P1 = (int(x_mid - distance * nx),int(y_mid - distance * ny))

        return P0, P1


    def calculate_line_side(self, point, line_start, line_end):

        x1, y1 = line_start
        x2, y2 = line_end
        px, py = point

        # Se utiliza el producto cruz entre el vector de la recta (AB) y el vector---------
        # desde el inicio de la recta hasta el punto (AP). El signo del resultado \  |
        # indica en qué lado de la recta se encuentra el punto.                    \ |
        cross = (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)                      

        if cross > 0:
            return 0
        elif cross < 0:
            return 1
        else:
            return None   # Está sobre la línea
        

    #HACER FUNCION PARA DECIDIR SI CONT++ AL CRUZAR LA LINEA -> VERIFICA SI SE ENCUENTRA EN LA PROYECCIÓN ORTOGONAL DE LA LINEA (PRODUCTO PUNTO)
    def is_projection_inside_segment(self, point, line_start, line_end):
        x1, y1 = line_start
        x2, y2 = line_end
        px, py = point

        # Vector AB (segmento)
        ab_x = x2 - x1
        ab_y = y2 - y1

        # Vector AP (desde el inicio de la línea al punto)
        ap_x = px - x1
        ap_y = py - y1

        # Parámetro de la proyección ortogonal
        t = (ap_x * ab_x + ap_y * ab_y) / (ab_x**2 + ab_y**2)
        #t: Parametro adimencional que señala en qué parte de la recta está la proyeccion
        # EJ: t = 0 -> A, t = 1->B, t=0.5 -> en la mitad, 
        # t=1.3 -> pasado 30% más alla de B, t=0.2-> 20% antes del A 

        #Si además quisieras obtener el punto proyectado Q, sería:
        #qx = x1 + t * ab_x
        #qy = y1 + t * ab_y

        if(t>=0 and t<=1):
            validation = 1
        else:
            validation = 0

        return validation

    def draw_bbox(self, im0, box, track_id, cls):

    # draw_bbox no se ejecuta 1 vez por frame, sino la cantidad n de objetos detectados
    # en cada frame
    # Para contar los frames debemos hacerlo en run(), justo leer el frame    
        """Draw bounding box with label at TOP-LEFT, but TEXT CENTERED in
          its box."""
        
        
    #La funcion recibe una caja para dibujar con sus atributos:

        #im0: Frame o imagen que se quiere cargar
        #box: Cajas definidas como [x1, y1, x2, y2]
        #track_id: Identificador del objeto cuando hay tracking
        #cls: Clase detectada por YOLO (0->person), (1->bycicle)...

        x1, y1, x2, y2 = map(int, box) # Opencv necesita int para dibujar (convierte los decimales)
        # map(int, location_object.xyxy[0]) le pasa los numeros del rectangulo a las varibles 

        color = colors(int(cls), True) #Asigna color distinto x clase. True->devuelve en formato BGR

        # Draw main bounding box
        cv2.rectangle(im0, (x1, y1), (x2, y2), color, self.rect_width)

        # Prepare label
        label = f"{self.names[int(cls)]}:{int(track_id)}"

        # Get text size (Alto y Ancho del texto de la caja)
        (tw, th), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, self.font, self.text_width
        )

        bg_x1 = x1  # left edge of bbox
        bg_x2 = bg_x1 + (tw + 2 * self.padding)

        bg_y2 = y1  # top of bbox
        bg_y1 = bg_y2 - (th + 2 * self.margin)

        # Draw filled background rectangle (top-left)
        #Este rectangulo contiene el texto por ej: "person: 16"
        # El último argumento es el grosor, -1 significa rellenar completamente el rectángulo
        cv2.rectangle(
            im0,
            (bg_x1, bg_y1),
            (bg_x2, bg_y2),
            color,
            -1,
        )

        text_x = bg_x1 + ((bg_x2 - bg_x1) - tw) // 2
        text_y = bg_y1 + ((bg_y2 - bg_y1) + th) // 2 - 2  # small vertical tweak

        cv2.putText(
            im0,
            label,
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            self.font,
            (104, 31, 17) if cls==2 else (255, 255, 255) ,  # white text
            self.text_width,
            cv2.LINE_AA,
        )
    #Funcion para calcular lado respecto de la linea definida por punto inicio y punto final (self, punto centro caja, inicio linea, fin linea) 
    #Se debe usar en bucle con todas las lineas (todos los id_objetos con todas las lineas)

    

if __name__ == "__main__":
    # Initialize and run tracker
    tracker = ObjectTracking(
        model="yolo11s.pt",
        source="Inputs/videoluis_cortado.mp4"
    )
    tracker.run()
