# 1. Definición de líneas virtuales

Las líneas son ingresadas manualmente utilizando mouse.

Cada línea está definida como:

```
(
 punto_inicio,
 punto_final
)
```

Ejemplo:

```
((200,300),(500,300))
```

# 2. Configuración interactiva mediante mouse

Al iniciar el programa se toma el primer frame para realizar la configuración de las lineas, mediante la siguiente función:

Función:

```
Mouse_Callback()
```

Permite:

1. Seleccionar primer punto.
2. Seleccionar segundo punto.
3. Crear una línea.
4. Guardarla en:

```
self.lines
```

Estructura:

```
[
((x1,y1),(x2,y2)),
((x3,y3),(x4,y4))
]
```