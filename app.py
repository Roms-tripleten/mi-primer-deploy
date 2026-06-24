import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página (Debe ser la primera instrucción de Streamlit)
st.set_page_config(
    page_title="SnackDash - Frutos Secos & Dulces Enchilados",
    page_icon="🌶️",
    layout="wide"
)

# 2. Carga de datos con caché para optimizar el rendimiento
@st.cache_data
def load_data():
    # Carga el dataset desde la ruta especificada
    df = pd.read_csv("data/data.csv")
    # Asegurar que la fecha sea tipo datetime
    df['Fecha_Venta'] = pd.to_datetime(df['Fecha_Venta'])
    return df

try:
    df_raw = load_data()
except FileNotFoundError:
    st.error("⚠️ No se encontró el archivo en 'data/dataset.csv'. Por favor, asegúrate de que la ruta sea correcta.")
    st.stop()

# 3. Título y Subtítulo muy llamativos con Emojis 🌶️🥜
st.title("🌶️ SnackDash: Panel de Control de Ventas 🥜")
st.markdown("""
### ¡Bienvenido al análisis picante y saludable! 📊
Explora el comportamiento de las ventas, las variedades más populares y los patrones de consumo de nuestros **Frutos Secos** y **Dulces Enchilados**. 
Use la barra lateral para filtrar la información en tiempo real.
---
""")

# 4. Barra Lateral (Sidebar) para Filtros Interactivos
st.sidebar.header("🎯 Filtros de Búsqueda")

# Filtro por Tipo de Producto
productos_disponibles = df_raw['Producto'].unique()
productos_seleccionados = st.sidebar.multiselect(
    "Selecciona el tipo de producto:",
    options=productos_disponibles,
    default=productos_disponibles
)

# Filtro por Variedad (Dinámico según el Producto seleccionado)
df_filtrado_temp = df_raw[df_raw['Producto'].isin(productos_seleccionados)]
variedades_disponibles = df_filtrado_temp['Variedad'].unique()
variedades_seleccionadas = st.sidebar.multiselect(
    "Selecciona la variedad específica:",
    options=variedades_disponibles,
    default=variedades_disponibles
)

# Filtro por Cliente Frecuente
cliente_frecuente_opt = st.sidebar.radio(
    "¿Filtrar por Cliente Frecuente?",
    options=["Todos", "Sí (TRUE)", "No (FALSE)"]
)

# Aplicación final de filtros al DataFrame
df_filtrado = df_raw[
    (df_raw['Producto'].isin(productos_seleccionados)) & 
    (df_raw['Variedad'].isin(variedades_seleccionadas))
]

if cliente_frecuente_opt == "Sí (TRUE)":
    df_filtrado = df_filtrado[df_filtrado['Cliente_Frecuente'] == True]
elif cliente_frecuente_opt == "No (FALSE)":
    df_filtrado = df_filtrado[df_filtrado['Cliente_Frecuente'] == False]

# 5. Métricas Clave de Alto Nivel (KPIs)
if not df_filtrado.empty:
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric("Total de Ventas ($)", f"${df_filtrado['Total_Venta'].sum():,.2f}")
    with kpi2:
        st.metric("Total Kilos Vendidos", f"{(df_filtrado['Gramos_Vendidos'].sum() / 1000):,.2f} kg")
    with kpi3:
        st.metric("Ticket Promedio", f"${df_filtrado['Total_Venta'].mean():,.2f}")
else:
    st.warning("No hay datos que coincidan con los filtros seleccionados.")

# 6. Checkbox para mostrar/ocultar vista previa del DataFrame
st.markdown("### 📋 Vista Previa de los Datos")
if st.checkbox("Mostrar vista previa de los datos filtrados", value=False):
    st.write(f"Mostrando las primeras {min(10, len(df_filtrado))} filas de un total de {len(df_filtrado)} registros encontrados:")
    st.dataframe(df_filtrado.head(10), use_container_width=True)

st.markdown("---")

# 7. Sección de Gráficos de Plotly Express
st.markdown("### 📈 Visualización Avanzada e Interactiva")

if not df_filtrado.empty:
    # Definimos una paleta de colores personalizada acordes a la temática (Chiles, Tamarindos, Nueces)
    color_palette = px.colors.qualitative.T10

    # Fila 1: Gráfico de Barras y Gráfico Circular
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📊 Top Variedades por Total de Venta")
        # Agrupamos para el gráfico de barras
        df_barras = df_filtrado.groupby('Variedad', as_index=False)['Total_Venta'].sum().sort_values(by='Total_Venta', ascending=True)
        
        fig_bar = px.bar(
            df_barras,
            x='Total_Venta',
            y='Variedad',
            orientation='h',
            labels={'Total_Venta': 'Total Ventas ($)', 'Variedad': 'Producto / Variedad'},
            color='Total_Venta',
            color_continuous_scale='YlOrRd' # Gradiente que evoca al chile y calor picante
        )
        fig_bar.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.markdown("#### 🍩 Distribución de Ventas por Categoría (Producto)")
        fig_pie = px.pie(
            df_filtrado,
            names='Producto',
            values='Total_Venta',
            hole=0.4,
            color_discrete_sequence=['#D32F2F', '#8D6E63'] # Rojo Picante y Marrón Fruto Seco
        )
        fig_pie.update_traces(textinfo='percent+label', pull=[0.05, 0])
        fig_pie.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Fila 2: Histograma utilizando el ancho completo
    st.markdown("#### 🧮 Histograma: Distribución de los Gramos Vendidos por Transacción")
    fig_hist = px.histogram(
        df_filtrado,
        x='Gramos_Vendidos',
        color='Producto',
        marginal='box', # Agrega un diagrama de caja superior para detectar outliers
        barmode='overlay',
        labels={'Gramos_Vendidos': 'Gramos en la Transacción', 'count': 'Frecuencia'},
        color_discrete_sequence=['#D32F2F', '#8D6E63']
    )
    fig_hist.update_layout(
        xaxis_title="Gramos Vendidos por Pedido",
        yaxis_title="Cantidad de Transacciones",
        margin=dict(l=20, r=20, t=30, b=20),
        height=450
    )
    st.plotly_chart(fig_hist, use_container_width=True)

else:
    st.info("💡 Consejo: Prueba seleccionando más opciones en los filtros de la barra lateral para renderizar los gráficos.")