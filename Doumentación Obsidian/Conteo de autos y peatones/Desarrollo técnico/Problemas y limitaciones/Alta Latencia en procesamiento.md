



### Bitácora de Diagnóstico – Sistema de Conteo Vehicular

### Contexto

Sistema de conteo de vehículos basado en:

- YOLO (detección)
    
- Tracking de objetos
    
- Lógica propia de cruce de líneas
    
- OCR (Tesseract) para extraer fecha y hora desde el video
    
- Exportación de eventos a Excel
    

Objetivo de esta etapa: identificar el cuello de botella de rendimiento que provocaba una ejecución de ~2–5 FPS.

### Problemas observados

### 1. Latencia muy alta del sistema

### Síntoma

El pipeline completo procesaba entre 170 y 380 ms por frame, resultando en 2–5 FPS.

### Hipótesis iniciales

- OpenCV (`imshow`) estaba ralentizando la ejecución.
    
- El OCR era el principal problema.
    
- La transferencia GPU → CPU (`.cpu()`) era costosa.
    
- Existía una fuga de memoria.
    
- El problema estaba en la lectura de frames (`cap.read()`).
    

### Experimentos realizados

### Experimento 1 – Eliminar visualización de video

### Cambio

Se desactivó:

```
cv2.imshow(...)
```

### Resultado

La latencia se mantuvo prácticamente igual.

### Diagnóstico

La ventana de video NO era el cuello de botella.

### Experimento 2 – Medir tiempo entre frames

### Instrumentación

Se añadió medición con:

```
time.perf_counter()
```

### Resultado típico

```
FRAME->42: 193.6 ms | FPS REAL: 5.17
```

### Diagnóstico

La medición confirmó que el problema afectaba al pipeline completo, no solo a una función aislada.

### Experimento 3 – Medir OCR por separado

### Instrumentación

```
t2 = time.time()
self.get_date_and_time(im0)
t3 = time.time()
```

### Resultado

OCR ≈ 110–140 ms por frame.

### Diagnóstico

El OCR tenía un costo alto, pero no explicaba por sí solo los 300+ ms observados.

### Experimento 4 – Medir YOLO + Tracking

### Instrumentación

```
t0 = time.time()
results = self.model.track(im0, persist=True, verbose=False)
t1 = time.time()
```

### Resultado

YOLO+TRACK ≈ 150–220 ms, con picos de 250+ ms.

### Diagnóstico

El tracking de Ultralytics aparecía como principal sospechoso.

### Experimento 5 – Verificar fuga de memoria

### Instrumentación

```
process.memory_info().rss
```

### Resultado

- Inicio: ~1450 MB
    
- Después de cientos de frames: ~1485 MB
    

### Diagnóstico

No existe una fuga significativa de memoria.

### Experimento 6 – Medir transferencia GPU → CPU

### Instrumentación

```
t4 = time.time()
boxes = result.boxes.xyxy.cpu()
ids = result.boxes.id.cpu()
t5 = time.time()
```

### Resultado

CPU TRANSFER ≈ 0–1 ms (ocasionalmente 2–3 ms).

### Diagnóstico

La transferencia GPU→CPU NO es el cuello de botella.

### Experimento decisivo – YOLO puro

### Cambio

Se reemplazó:

```
self.model.track(...)
```

por

```
self.model(im0, verbose=False)
```

Además, se desactivó completamente el OCR.

### Resultados

### Inferencia

```
YOLO SOLO: 10–15 ms
```

### Pipeline completo

```
FRAME: 27–35 ms
FPS REAL: 29–40
```

### Casos típicos

```
FRAME->120: 27.0 ms | FPS REAL: 36.98
YOLO SOLO: 10.6 ms
CPU TRANSFER: 0.0 ms
```

### Diagnóstico final

### Componentes descartados

|Componente|Estado|
|---|---|
|Ventana OpenCV (`imshow`)|Descartado|
|Transferencia `.cpu()`|Descartado|
|Fuga de memoria|Descartado|
|`cap.read()`|Descartado|

### Componentes con costo real

|Componente|Costo aproximado|
|---|---|
|YOLO puro|10–15 ms|
|OCR Tesseract|110–140 ms|
|Ultralytics `track(persist=True)`|150–220 ms|

### Conclusión principal

El cuello de botella dominante del sistema es:

Ultralytics track(persist=True)

El tracking agrega aproximadamente:

150–220 ms por frame150\text{–}220\ \text{ms por frame}150–220 ms por frame

mientras que la detección YOLO pura tarda solo:

10–15 ms10\text{–}15\ \text{ms}10–15 ms

La diferencia observada es cercana a:

180 ms adicionales por frame180\ \text{ms adicionales por frame}180 ms adicionales por frame

### Implicancias para la arquitectura

El sistema sí necesita tracking para:

- mantener IDs persistentes,
    
- detectar cruces de líneas,
    
- evitar doble conteo,
    
- reconstruir trayectorias.
    

Sin embargo, los experimentos muestran que:

- YOLO puro es suficientemente rápido (30–40 FPS).
    
- El problema no es la detección, sino el tracker integrado de Ultralytics.
    

Por ello, la línea de trabajo recomendada es:

- Conservar YOLO puro.
    
- Implementar un tracker propio liviano basado en centroides y distancia entre frames.
    
- Ejecutar OCR solo cada N frames (100–300) y reutilizar la última fecha/hora válida.
    

Esta arquitectura permitiría mantener IDs y lógica de conteo con un rendimiento estimado de 25–35 FPS reales, muy superior al obtenido con `track(persist=True)`.





Se creó el archivo TestSpeed_Track.py para aislar el componente de tracking y se vió que la latencia se debe principalmente al Tracker de Ultralitycs, y de forma menor para despues, por estar llamando a OCR en cada frame.

Debemos atender el problema del tracking







![[Pasted image 20260720120358.png]]

Investigar ¿ Y si no ejecutamos el tracking en todos los frames? ¿ Y si lo hacemos cada 3 frames?