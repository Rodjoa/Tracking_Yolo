
## Definición

El movimiento de un objeto se determina analizando la secuencia de líneas virtuales que atraviesa durante su trayectoria.

Cada vez que un objeto cambia de lado respecto a una línea se genera un evento de cruce, el cual almacena:

- Número de línea atravesada.
- Estado anterior (lado desde donde viene).
- Estado nuevo (lado hacia donde cruza).

Un movimiento queda definido por la combinación de dos eventos consecutivos pertenecientes al mismo objeto.

## Registro de eventos

Cuando un objeto cruza una línea se genera una estructura:

```python
current_event = {
    "line": numero_linea,
    "from": prev_side_value,
    "to": new_side_value
}
```





## Vehículos

### Definición de movimiento

En vehículos, el movimiento se define como la trayectoria realizada por un objeto entre diferentes zonas de una escena.

No basta con detectar que un vehículo cruzó una línea, ya que un mismo cruce puede corresponder a diferentes trayectorias:

- Continuar recto.
- Girar a la derecha.
- Girar a la izquierda.

Por esta razón, en intersecciones vehiculares el movimiento se determina mediante la secuencia de cruces de líneas virtuales.

---

### Método utilizado

Cada cruce de línea genera un evento:

```python
{
    "line": número_de_línea,
    "from": lado_inicial,
    "to": lado_final
}
````

La trayectoria del vehículo se obtiene combinando eventos consecutivos del mismo ID.

Ejemplo:

```
Vehículo A

Cruza línea 0:
lado 0 → lado 1

Luego cruza línea 2:
lado 0 → lado 1
```

La combinación de ambos eventos identifica un movimiento específico.

---

### Tabla de movimientos

Debido a que la geometría cambia según el video, cada escenario requiere una tabla de movimientos propia.

Ejemplo:

```
(línea inicial, lado inicial, lado final,
 línea final, lado inicial, lado final)

              ↓

          movimiento
```

Ejemplo:

```
(0,0,1,2,0,1)

              ↓

        Giro derecha
```

---

## Peatones

### Definición de movimiento

En peatones, generalmente no es necesario identificar una trayectoria completa, sino determinar si una persona atravesó una zona de interés.

El movimiento se reduce a:

- Entró a una zona.
- Salió de una zona.
- Cruzó una línea peatonal.

---

### Método utilizado

Debido a que los peatones presentan mayor falla en el trackeo, se opta por usar una linea, porque basta con que el id se mantenga durante el cruce, en cambio si es más de una linea, aumenta la probabilidad de falla del id, porque debe mantenerse durante toda esa distancia.

Los problemas de trackeo se deben, entre otros a

- Oclusiones frecuentes.
- Posiciones extrañas
- Mala detección de personas lejanas

Entonces se utiliza principalmente una sola línea virtual.
En este escenario basta el cruce de una sola línea para configurar el movimiento determinado.

Ejemplo:

```
Antes:

Persona
lado 0


---------------- Línea de conteo


Después:

Persona
lado 1
```

El evento registrado es:

```
Cruce peatonal válido
```


## Decisión de diseño

Se decidió utilizar estrategias diferentes según el objeto:

- Vehículos en intersecciones:
    - Múltiples líneas.
    - Secuencia de eventos.
    - Tabla de movimientos.
- Peatones:
    - Una línea.
    - Conteo por cambio de lado.

Esta separación busca reducir errores debido a las diferencias de comportamiento y dificultad de tracking entre vehículos y peatones.

Se pondera la poca cantidad de personas que a medio cruzar se devuelven (falso positivo), con la enorme cantidad de personas que no son detectadas al cruzar (falso negativo) y se considera apropiado este enfoque.