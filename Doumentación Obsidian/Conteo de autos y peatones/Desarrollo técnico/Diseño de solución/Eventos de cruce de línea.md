
Nuestro modelo nos permite detectar si el objeto realiza el cruce de una línea y también el sentido en el cual lo hace. Para ello realiza los cálculos que se explican a continuación.
# 1. Determinación del lado de una línea

## Fundamento matemático

Supongamos tenemos la recta L en donde sus puntos extremos son A y B. Sabemos que una linea divide el espacio en 2. y queremos determinar a qué lado de la linea se encuentra el punto P0, para detectar cuando cambie de lado (identificando que cruzó) 

Se utiliza PRODUCTO CRUZ:

AB×AP

Código:

```
cross =
(x2-x1)(py-y1)-(y2-y1)(px-x1)
```

Resultado:

| Valor    | Significado    |
| -------- | -------------- |
| positivo | lado 0         |
| negativo | lado 1         |
| cero     | sobre la línea |

Esto permite transformar una posición 2D en un estado discreto:

```
Objeto

lado 0
 |
 |
Linea
 |
 |
lado 1
```

Esto nos permite asignar un estado permanente a cada objeto, según se encuentra al lado 0 o al lado 1 respecto de cada línea dibujada durante la configuración de líneas.

![[Pasted image 20260717222540.png]]

Cuando un objeto cambia de lado respecto a la línea detectamos un cruce, pero esto no es suficiente para detectar un cruce válido, porque calcula cruce para rectas infinitas, pero trabajamos con segmentos de rectas, así que debemos validar el cruce según si está o no en la región de proyección ortogonal de la línea.

# 12. Validación geométrica del cruce

## Problema

Un objeto podría cambiar de lado respecto a la recta (considerada infinita) pero lejos del segmento dibujado.

Ejemplo:
Un auto en la autopista de al lado cruza la línea infinita definida por un segmento de línea para contar cruces en la autopista de al lado, entonces no nos interesa contar ese cruce.

---

## Solución

Se calcula la proyección ortogonal sobre la línea.

Se utiliza el PRODUCTO PUNTO

Función:

```
is_projection_inside_segment()
```

Parámetro:

ttt

Interpretación:

|t|posición|
|---|---|
|0|inicio línea|
|0.5|mitad|
|1|final|
|>1|fuera|
|<0|fuera|

Solo se acepta:

0≤t≤1 



Explicación larga (Dejar clara más adelante):



## Fundamento matemático

La línea de conteo está definida por dos puntos:

\[A=(x_1,y_1)\]

\[
B=(x_2,y_2)
\]

Estos puntos generan el vector dirección de la línea:

\[
\vec{AB}=B-A
\]

El objeto detectado tiene una posición:

\[
P=(x_p,y_p)
\]

y se define el vector desde el inicio de la línea hasta el objeto:

\[
\vec{AP}=P-A
\]


Para conocer dónde cae la proyección ortogonal del punto sobre la línea se calcula:

\[
t=\frac{\vec{AP}\cdot\vec{AB}}
{\vec{AB}\cdot\vec{AB}}
\]

El producto punto permite obtener cuánto del vector \(\vec{AP}\) está alineado con la dirección de la línea \(\vec{AB}\).

El parámetro `t` no representa una distancia, sino una posición relativa dentro de la línea.

---

## Parámetro t

El valor de `t` indica la posición de la proyección sobre la recta:

|t|posición|
|---|---|
|t < 0|Antes del inicio de la línea|
|0|Inicio línea|
|0.5|Mitad de la línea|
|1|Final línea|
|>1|Después del final del segmento|

Ejemplo:
```

t < 0 0 <= t <= 1 t > 1

```
   |----------------------------|

   A                            B
```

```

Solo se acepta:

\[
0 \leq t \leq 1
\]

porque significa que la proyección del objeto está dentro del segmento dibujado.

---

## Aplicación en el sistema

El cruce solamente es considerado válido cuando se cumplen ambas condiciones:

1. El objeto cambia de lado respecto a la línea mediante:
```

calculate_line_side()

```

2. La proyección del objeto se encuentra dentro del segmento mediante:
```

is_projection_inside_segment()

```

De esta forma se evita contabilizar objetos que cruzan la extensión infinita de la 
```

