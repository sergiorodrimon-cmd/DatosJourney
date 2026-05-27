import pandas as pd

# 1. Cargar datos
ventas = pd.read_csv("data/raw/ventas_2024.csv")
clientes = pd.read_csv("data/raw/clientes.csv")
productos = pd.read_csv("data/raw/productos.csv")

# 2. Convertir tipos de datos
ventas["fecha"] = pd.to_datetime(ventas["fecha"])
ventas["cantidad"] = ventas["cantidad"].astype(int)
ventas["precio_unitario"] = ventas["precio_unitario"].astype(float)

# 3. Limpieza de texto
ventas["region"] = ventas["region"].str.strip().str.title()
ventas["categoria"] = ventas["categoria"].str.strip().str.title()
ventas["producto"] = ventas["producto"].str.strip()

# 4. Validación básica
ventas = ventas[ventas["cantidad"] > 0]
ventas = ventas[ventas["precio_unitario"] > 0]

# 5. Cálculo de métricas
ventas["ventas_totales"] = ventas["cantidad"] * ventas["precio_unitario"]

# 6. Integración de datos
ventas = ventas.merge(clientes, on="cliente_id", how="left")
ventas = ventas.merge(productos, on="producto", how="left")

# 7. Cálculo de margen
ventas["margen"] = ventas["ventas_totales"] - (
    ventas["cantidad"] * ventas["costo_unitario"]
)

# 8. Verificación final
print("Registros finales:", ventas.shape[0])
print("Valores nulos por columna:\n", ventas.isnull().sum())

# 9. Guardar dataset limpio
ventas.to_csv("data/processed/ventas_limpias.csv", index=False)

print("Datos limpios guardados en data/processed/ventas_limpias.csv")
