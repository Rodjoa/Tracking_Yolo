# Estado actual del proyecto

Fecha:
17-07-2026

---

## Objetivo

Desarrollar un sistema de conteo para tráfico vehicular y peatonal enfocado en cruces mediante YOLO,
tracking y líneas virtuales.

El sistema busca ser adaptable a distintos escenarios de aplicación:

- Cruces vehiculares en intersecciones.
- Conteo de vehículos en carreteras rectas.
- Conteo de peatones en cruces peatonales.

La estrategia de procesamiento dependerá de las características del escenario,
priorizando robustez del tracking y reducción de errores de conteo.

---

## Implementado

- [x] Detección de objetos mediante YOLO.
- [x] Tracking de objetos mediante asignación de ID.
- [x] Obtención de trayectoria mediante centroides.
- [x] Definición manual de líneas virtuales mediante mouse.
- [x] Determinación del lado del objeto respecto a una línea mediante producto cruz.
- [x] Detección de cambios de lado como evento de cruce.
- [x] Validación geométrica del cruce mediante proyección ortogonal sobre el segmento.
- [x] Conteo general mediante líneas virtuales.
- [x] Conteo de vehículos en cruces mediante dos líneas.
- [x] Primera implementación de tabla de movimientos para distinguir trayectorias vehiculares.
- [x] Visualización de bounding boxes, IDs y trayectoria del objeto.

---

## Estrategias definidas actualmente

### Cruces vehiculares en intersecciones

Estrategia:

- Uso de dos o más líneas virtuales.
- Registro del orden de cruce de líneas.
- Clasificación del movimiento mediante tabla de movimientos.

Motivación:

En una intersección no basta conocer que un vehículo cruzó una línea,
sino que es necesario determinar su trayectoria:

- Giro derecha.
- Giro izquierda.
- Continuar recto.

---

### Vehículos en carretera recta

Estrategia propuesta:

- Uso de una línea virtual.

Motivación:

Una única línea reduce la dependencia del tracking entre regiones,
disminuyendo la posibilidad de pérdida de identidad del objeto.

---

### Cruces peatonales

Estrategia propuesta:

- Uso de una línea virtual.

Motivación:

Los peatones presentan mayor variabilidad:

- Cambios de velocidad.
- Oclusiones.
- Movimiento menos predecible.

El uso de múltiples líneas puede aumentar la pérdida de tracking
y generar objetos no contabilizados debido a cambios de ID.

---

## Pendientes de codificación

- [ ] Implementar contador peatonal y carretera recta con una línea.
- [ ] Completar lógica de contador por clase.
- [ ] Exportar datos automáticamente a Excel.
- [ ] Detectar hora y fecha del video.
- [ ] Exportar datos asociados a fecha y hora del video.

---

## Pendientes experimentales

- [ ] Probar distintos videos para determinar en qué condiciones el modelo funciona mejor.
- [ ] Definir ángulo óptimo de cámara.
- [ ] Definir altura/elevación recomendada de cámara.
- [ ] Analizar influencia de perspectiva y distancia.
- [ ] Definir con Luis los videos que serán utilizados.
- [ ] Validar modelo mediante comparación con conteo manual o videos etiquetados.
- [ ] Estimar error del sistema.
- [ ] Definir condiciones donde el modelo es confiable.
- [ ] Iterar si se ven posibles mejoras

Características a evaluar:

- Resolución del video.
- FPS.
- Iluminación.
- Cantidad de objetos simultáneos.
- Oclusiones.
- Ángulo de visión.
- Distancia de la cámara al área de interés.

---

## Problemas encontrados

### Pérdida de tracking

Problema:

El uso de múltiples líneas aumenta la posibilidad de pérdida de identidad del objeto,
debido a cambios de ID durante el recorrido.

Consecuencia:

Un mismo vehículo puede ser considerado como objetos diferentes,
provocando errores de conteo.


---

## Próximos pasos 


1. Subir versión actual a Github
2. Documentar decisiones y funciones importantes en notas de Obsidian
3. Exportar Excel con datos post video
4. Detección de fecha y hora de la cámara y exportar señalando a qué periodo (ej: los primeros 15 min) pertenecen los datos.
5. Implementar contador peatonal de 1 línea
6. Realizar pruebas con distintos escenarios.
7. Definir condiciones de uso del sistema.
