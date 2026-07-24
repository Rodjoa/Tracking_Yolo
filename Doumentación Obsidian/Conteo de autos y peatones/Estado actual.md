# Estado actual del proyecto

Fecha:
17-07-2026

---

## Conclusiones principales — Día 21 (21/07/2026)

### Estado general

El sistema presenta una V1 funcional con detección, tracking, OCR y exportación a Excel operativos. El cuello de botella principal de latencia fue mitigado mediante OCR bajo demanda.

---

## Riesgo técnico pendiente

### Robustez del reconocimiento de fecha y hora

Se observó que el OCR funciona correctamente en `videoluis_cortado.mp4` (overlay en blanco y negro), pero falla en otros videos.

Esto sugiere que el problema está asociado a la calidad y representación visual de la ROI más que al funcionamiento básico de Tesseract.

---

## Hipótesis identificadas

### H1 — Calidad insuficiente de la ROI

La compresión del video y la pixelación pueden volver ilegible el timestamp para el OCR.

### H2 — Contraste insuficiente del texto

Los números poseen un color relativamente fijo (amarillo), mientras que el ruido presenta variaciones de color.

Esto sugiere aplicar un preprocesamiento por color para:

- resaltar el amarillo del timestamp,
    
- eliminar píxeles no pertenecientes al texto,
    
- generar una imagen binaria más adecuada para Tesseract MEDIANTE FILTRO HSV u otro

### H3 — Lectura única demasiado frágil

Ejecutar OCR una sola vez cuando se detecta movimiento tiene alta probabilidad de fallo debido a blur, ruido o compresión del frame específico.

### H4 — ROI mal configurada

La posición de la fecha/hora puede variar entre videos, provocando recortes incorrectos.

HIPOTESIS DESCARTADA (DEBUG DE IMAGEN CORTADA ARROJO QUE NO)




    

---

## Método propuesto

### OCR bajo demanda con ráfaga de validación

1. Detectar movimiento o evento relevante.

2. Cortar la imagen, dejando la ROI
    
3. Extraer ROI de fecha/hora.
    
4. Aplicar preprocesamiento por color y contraste.
    
5. Ejecutar OCR.
    
6. Validar el formato obtenido.
    
7. Si el resultado es inválido, repetir el procedimiento durante una pequeña ráfaga de frames hasta obtener un valor válido o alcanzar un número máximo de intentos.
    

Hay que ver si usaremos máscara para el texto para el OCR
---

## Consideración temporal importante

La frecuencia de operaciones debe depender de los FPS del video.

Conociendo los FPS es posible convertir tiempo real a cantidad de frames.

Ejemplo:

- 30 FPS → 1800 frames ≈ 1 minuto.
    

Esto permitirá implementar lógica basada en intervalos temporales, por ejemplo:

- ejecutar OCR al inicio del video,
    
- mantener OCR bajo demanda durante el intervalo actual,
    
- forzar una nueva lectura cuando cambie el intervalo temporal de interés.
    

Esta estrategia desacopla la actualización de la hora del evento de cruce y la vincula a la línea temporal real del video.

Recordar que podemos asignarle la hora 9:15 a todos los movimientos del intervalo                         [9:15:00-9:29:59]



Además, Vemos dos posibles casos de actualización para OCR:

![[Pasted image 20260721170650.png]]