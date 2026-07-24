import cv2
from datetime import datetime, timedelta

source = 'Inputs/OCM/1.mp4'

# Hora real del primer frame
start_time = datetime.strptime(
    '2026-07-22 08:33:34',
    '%Y-%m-%d %H:%M:%S'
)

cap = cv2.VideoCapture(source)

if not cap.isOpened():
    print('Error: Could not open video')
    exit()

frame_count = 0

while True:
    success, frame = cap.read()

    if not success:
        break

    frame_count += 1

    # Tiempo transcurrido del video
    ms = cap.get(cv2.CAP_PROP_POS_MSEC)

    # Fecha y hora absolutas
    event_time = start_time + timedelta(milliseconds=ms)
    fecha = event_time.strftime('%Y-%m-%d')
    hora = event_time.strftime('%H:%M:%S')

    print(
        f'Frame: {frame_count:6d} | '
        f'Fecha: {fecha} | '
        f'Hora: {hora}'
    )

    cv2.putText(frame,
                f'{fecha} {hora}',
                (40, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()