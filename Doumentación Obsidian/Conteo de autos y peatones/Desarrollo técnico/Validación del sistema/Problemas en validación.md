
Comienzo de Etapa de Validación:
-Se seleccionaron 13 videos del video largo para probar.

Pendientes:
* Presenta problemas al reconocer fecha y hora (funciona bien en videoluis_cortado.mp4 que es en blanco y negro)

Posibles problemas OCR:
* Calidad de cámara o frame ilegible para el OCR (no lee la hora por pixelación)
* ROI mal configurada en el video respectivo
* Alta posibilidad de fallo al leer OCR una sola vez, mejor lanzar una ráfaga cuando detecte movimiento (ajustar el umbral o criterio después)
* Hacer filtro para la ROI para que el texto destaque más y sea más legible para el OCR (bajo demanda, cuando detecte movimiento)

TENER EN CUENTA LOS FPS DEL VIDEO, PORQUE PODEMOS SABER CADA CUANTOS FRAMES HACER UNA OPERACIÓN SI QUEREMOS POR EJEMPLO: HACER ALGO CUANDO PASEN X MINUTOS EN EL VIDEO -> Recordar que despues habrán intervalo de tiempo que nos interesa medir. La idea será activar el OCR al principio del primer intervalo (inicio del video) y despues cuando cambie el intervalo, dejaremos de hacer el OCR bajo demanda de cruce y la haremos cada tantos FPS sabiendo los fps del video que estamos procesando 




Ideas encontradas sin validar (aún no se si son necesarias pero las guardo)

Mejora para el algoritmo:
* En vez de líneas hacer un polígono
* Detectar la dirección (diferencial o aproximado) de giro en varios puntos (quita la necesidad de trackeo constante) (Evita falsos negativos pero introduce falsos positivos por cambio de id-> contaría los dos ids)
* 
OBSERVACIONES:
* Ya tengo el id de cada objeto en cada frame ¿ realmente necesito un polígono o ya puedo hacer esos cálculos? -> Puedo realizar los cálculos de giro despues de cruzar la primera linea (sabemos por diseño que todos los autos cruzarán 2 líneas)

