
### Tasa de muestreo adaptativa

Frame skipping adaptativo basado en movimiento: el sistema podría ajustar dinámicamente la tasa de procesamiento según la actividad de la escena para optimizar rendimiento sin comprometer precisión.

Ideal para embebidos como raspberry (menor capacidad de procesamiento)



Hilo:

### Y aquí aparece una idea aún mejor para tu proyecto

### Dos frecuencias de operación

### Modo vigilancia (bajo costo)

- 5 FPS.
    
- solo motion detection.
    
- consumo mínimo.
    

### Modo análisis (alto costo)

- 15–30 FPS.
    
- YOLO + tracking.
    
- OCR.
    
- duración corta.
    

Eso es prácticamente un sistema de eventos.

### Ejemplo realista

Supongamos una cámara en una calle tranquila.

### 1 minuto de video

- 45 s sin autos.
    
- 15 s con autos.
    

### Sin adaptación

YOLO corre 60 s completos.

### Con adaptación

YOLO corre solo 15 s.

Ahorro aproximado:

60−1560=75%\frac{60-15}{60}=75\%6060−15​=75%

~75% menos tiempo de inferencia.

En una Raspberry eso es enorme.

### Incluso podrías hacer algo más inteligente

Y esto conecta con tu idea original.

### Control por densidad de movimiento

|Escena|FPS objetivo|
|---|---|
|Vacía|5 FPS|
|1–2 autos|10 FPS|
|Flujo normal|15 FPS|
|Congestión|30 FPS|

Eso ya es un scheduler adaptativo.