import pandas as pd

# 1. Cargar datos limpios
df = pd.read_csv("data/processed/ventas_limpias.csv")

# 2. Preparar columnas
df["fecha"] = pd.to_datetime(df["fecha"])
df["mes"] = df["fecha"].dt.to_period("M").astype(str)

# 3. KPIs generales
kpis = {
    "Ventas Totales": df["ventas_totales"].sum(),
    "Total Órdenes": df["orden_id"].nunique(),
    "Ticket Promedio": df["ventas_totales"].mean(),
    "Margen Total": df["margen"].sum()
}

df_kpis = pd.DataFrame(
    list(kpis.items()),
    columns=["Indicador", "Valor"]
)

# 4. Resumen mensual
resumen_mensual = (
    df.groupby("mes")
      .agg(
          ventas_totales=("ventas_totales", "sum"),
          margen_total=("margen", "sum"),
          ordenes=("orden_id", "nunique")
      )
      .reset_index()
)

# 5. Top productos
top_productos = (
    df.groupby("producto")
      .agg(ventas_totales=("ventas_totales", "sum"))
      .sort_values(by="ventas_totales", ascending=False)
      .reset_index()
)

# 6. Exportar a Excel
output_path = "output/reporte_ventas.xlsx"

with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
    df_kpis.to_excel(writer, sheet_name="KPIs", index=False)
    resumen_mensual.to_excel(writer, sheet_name="Resumen Mensual", index=False)
    top_productos.to_excel(writer, sheet_name="Top Productos", index=False)

print("✅ Reporte generado correctamente en:", output_path)
