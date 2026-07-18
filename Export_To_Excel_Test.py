import pandas as pd
from datetime import datetime
import random
import time


archivo = "conteo_flujo.xlsx"

registros = []
periodo_exportacion = 3

for i in range(11):

    #En nuestro programa sin OCR (aún)

    hora = 7 + (i // 4) #Operador de división entera: Divide y redondea hacia abajo al entero más cercano. 7//4 = redond(1.75) = 1
    minutos = (i % 4) * 15  #Se repiten cíclicamente los valores 0, 15,30 y 45 para los minutos

    hhmm = hora * 100 + minutos

    m1 = random.randint(1, 4)
    m2 = random.randint(1, 4)
    m3 = random.randint(1, 4)
    m4 = random.randint(1, 4)

    registro = {
        "PC": 1,
        "UBICACION": "Interseccion Av. Principal",
        "COMUNA": "Viña del Mar",
        "DIA": "Lunes",
        "FECHA": "18-07-2026",
        "HORA": f"{hora:02d}:{minutos:02d}",
        "HH": hora,
        "HHMM": hhmm,
        "MOV 1": m1,
        "MOV 2": m2,
        "MOV 3": m3,
        "MOV 4": m4,
        "FLUJO": (m1+m2+m3+m4)
    }

    registros.append(registro)

    
    df = pd.DataFrame(registros)

    df.to_excel(
        archivo,
        index=False
    )
    print("registros")
    print(registros)
    registros.clear() #En nuestro programa real se limpiará cada 15 minutos de video (Quizas no lo usemos aún en la version reporte post video)
    

   


print("Excel generado")