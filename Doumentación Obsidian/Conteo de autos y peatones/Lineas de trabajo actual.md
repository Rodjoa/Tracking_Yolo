Tareas rápidas pendientes:
* No llamar a OCR en cada frame, solo cuando DETECTA MOVIMIENTO y ahí actualizar los datos de fecha y hora (posiblemente fecha no lo cambiemos despues, depende)
* Agregar los datos en cada vuelta de bucle al Excel y liberar a variable resigtros = [ ], para que deje de acumular todo y sobreescribirlo en cada vuelta (se vuelve muy pesada la variable)


Enfoques de trabajo:  


Ya tenemos la primera versión V1 del sistema.
Ahora el trabajo se divide en dos líneas.

* Latencia: Lentitud del Tracking (no de Yolo) y dejar de llamar al OCR cada frame

* Confiabilidad del sistema: Testear con diferentes videos, Definir enfoques correctos y resolución útil de cámara, Crear experimentalmente un factor de corrección y ajustar algunas otras cosas experimentalmente, validar sistema con métricas.