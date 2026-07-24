import pandas as pd

# ================= Leer eventos =================
df = pd.read_excel("conteo_flujo.xlsx")

# Convertir FECHA y HORA a texto seguro
fecha_str = pd.to_datetime(df["FECHA"]).dt.strftime("%Y-%m-%d")
hora_str = pd.to_datetime(df["HORA"].astype(str)).dt.strftime("%H:%M:%S")

# Timestamp completo
df["DT"] = pd.to_datetime(fecha_str + " " + hora_str)

# ================= Definir intervalo =================
intervalo = "1min"

# Redondear cada evento al inicio del intervalo
df["INTERVALO"] = df["DT"].dt.floor(intervalo)

# ================= Resumen por intervalo =================
resumen = (
    df.groupby(["INTERVALO", "MOVIMIENTO"])
      .size()
      .unstack(fill_value=0)
)

# ================= Crear TODOS los intervalos =================
inicio = df["INTERVALO"].min()
fin = df["INTERVALO"].max()

todos_los_intervalos = pd.date_range(
    start=inicio,
    end=fin,
    freq=intervalo
)

# ================= Reindexar y rellenar con 0 =================
resumen = resumen.reindex(todos_los_intervalos, fill_value=0)

# Nombre del índice
resumen.index.name = "INTERVALO"

# ================= Mostrar y guardar =================
print(resumen)

resumen.to_excel("resumen_intervalos.xlsx")

print("Resumen generado correctamente")