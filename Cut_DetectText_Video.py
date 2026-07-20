import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
source = "Inputs/videoluis_cortado.mp4" 
cap = cv2.VideoCapture(source)

# Check if the video file opened successfully
if not cap.isOpened():
    print("Error: Could not open the video file.")
    exit()

# 2. Loop through each frame sequentially
prev_texto = ''     #Variable util para comparar si el texto cambia respecto al frame anterior (detectar si cambia fecha u hora)
while cap.isOpened():
    # Read the next frame
    success, frame = cap.read()
    if not success:
        print("End of video file or failed to read frame.")
        break

    #La imagen es la variable 'frame'
    rows, cols, _ = frame.shape       #Capturamos la dimensión para testear donde cortar la fecha y hora
    #print("Rows: ", rows)
    #print("Cols: ", cols)
        
    # 3. Mostramos la imagen original
    #cv2.imshow('Video Playback', frame)

    #Cortamos la imagen y la mostramos
    ROI_DateTime = frame[0:100, 0:600]          #Región de pixeles de interés donde se encuentra la fecha y hora del video
    #cv2.imshow('Video Playback', ROI_DateTime)


    # OCR completo
    texto = pytesseract.image_to_string(ROI_DateTime)
    #Cambiaremos la foto solo cuando el texto cambie

    if(texto and texto!= prev_texto ):

        cv2.imshow('Video Playback', ROI_DateTime)
        frame_num = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        print('Frame:', frame_num)
        print(texto)
        

    prev_texto = texto


    #cv2.imshow('Video Playback', ROI_DateTime)

    #for letter in texto:
        #print("word: ",letter,"\n")

    # Obtener datos de cada palabra
    hImg, wImg, _ = ROI_DateTime.shape
    boxes = pytesseract.image_to_data(ROI_DateTime)

    for x, b in enumerate(boxes.splitlines()):
        if x != 0:
            b = b.split()

            # Algunas líneas vienen vacías
            if len(b) == 12:
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])

                # Dibujar rectángulo
                cv2.rectangle(ROI_DateTime, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Dibujar texto detectado
                cv2.putText(
                    ROI_DateTime,
                    b[11],
                    (x, y - 10),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.7,
                    (255, 0, 255),
                    2
                )
    
    # 4. Control playback speed and handle user exit (Press 'q' to quit)
    # The number 25 introduces a 25ms delay between frames


    #TERMINAMOS CON LA TECLA 'q'
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
cap.release()
#cv2.waitKey(0)
cv2.destroyAllWindows()
