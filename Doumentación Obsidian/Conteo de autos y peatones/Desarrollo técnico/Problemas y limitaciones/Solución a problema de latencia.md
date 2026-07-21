
## Optimización de latencia del sistema

Durante la etapa de validación se identificó que la principal fuente de latencia del sistema era la ejecución simultánea de OCR y tracking en cada frame del video.

### Pipeline original

En la versión inicial, cada frame ejecutaba las siguientes etapas:

- OCR de fecha y hora.
    
- Detección y tracking con YOLO.
    
- Lógica de cruces.
    
- Exportación de datos.
    

Esto generaba tiempos de procesamiento del orden de:

- OCR: ~130-150 ms.
    
- YOLO + Tracking: ~250 ms.
    
- Total por frame: ~380-400 ms.
    

La tasa de procesamiento efectiva era aproximadamente 2.5 FPS.

### Optimización implementada

Se modificó la arquitectura para ejecutar el OCR únicamente cuando se detecta un movimiento relevante.

El nuevo pipeline quedó definido como:

- YOLO + Tracking.
    
- Lógica de cruces.
    
- OCR solo ante evento de movimiento.
    

Con esta estrategia, el costo del OCR dejó de ser fijo por frame y pasó a ser un costo asociado únicamente a eventos.

### Submuestreo temporal

Adicionalmente se evaluó el descarte de un frame de cada dos, procesando aproximadamente la mitad de los frames del video.

La viabilidad de esta técnica depende de la velocidad de los vehículos:

- Vehículos lentos: alta viabilidad.
    
- Vehículos rápidos: menor viabilidad debido al riesgo de perder el instante de cruce.
    

Por lo tanto, el submuestreo temporal se considera un parámetro configurable según el tipo de escena analizada.

### Conclusión

La reducción de latencia se logró principalmente mediante decisiones de arquitectura del pipeline y no mediante modificaciones al modelo YOLO. La activación condicional del OCR y el procesamiento selectivo de frames permitieron aumentar significativamente la velocidad de operación del sistema manteniendo la funcionalidad de detección de cruces.