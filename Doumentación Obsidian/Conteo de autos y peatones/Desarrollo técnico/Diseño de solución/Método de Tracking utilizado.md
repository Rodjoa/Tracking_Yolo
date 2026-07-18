
El modelo de YOLO se encarga de detectar los objetos, asignarles box rectangulares con un id, y también de mantener esa id a lo largo del trayecto del objeto detectado. A continuación explicamos cómo guardamos cada posición que va tomando el objeto en nuestra imagen.
## Historial de trayectoria

Variable:

```
self.track_history
```


self.track_history[n] corresponde al historial de trayectorias del objeto con id n.

Estructura:

```
ID -> lista de coordenadas del centroide de la caja del objeto
```

Ejemplo:

```
{
23:[
(450,200),
(455,205),
(460,210)
]
}
```

Cada punto la coordenada del centroide capturada su respectivo frame:

![[Pasted image 20260717220648.png]]

El historial de de trayectoria nos indica dónde se encuentra el objeto en cada frame, expresado en coordenadas (x,y). Y nos permite en cada frame saber de qué lado está respecto a la linea de cruce, y saber si ocurrió un cambio de lado (cruce) respecto a alguna línea.