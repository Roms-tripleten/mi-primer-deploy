# 🍬 SnackDash: El Panel de Antojos 🌶️

¡Bienvenido a **SnackDash**! Este es un panel de control (dashboard) interactivo diseñado para el monitoreo y análisis en tiempo real de ventas de snacks, especializándose en dulces enchilados y frutos secos. 

Desarrollado con un enfoque de arquitectura limpia y frontend de datos moderno, este proyecto transforma datos planos de ventas en insights visuales y accionables de forma inmediata.

---

## 🚀 Características Principales

* **⚡ Interactividad Reactiva:** Los gráficos y métricas se actualizan instantáneamente al interactuar con los filtros sin necesidad de recargar la página.
* **🎯 Filtros Avanzados:** Filtrado dinámico por tipo de producto y disponibilidad de envío a domicilio directamente desde la barra lateral.
* **📊 Visualizaciones de Alto Impacto (Plotly Express):**
    * **Gráfico de Barras:** Total de ventas desglosado por variedad de snack.
    * **Gráfico de Dona:** Proporción de ingresos según la fidelidad del cliente (Frecuente vs. Ocasional).
    * **Histograma con Marginal Box:** Distribución de los gramos vendidos por transacción, incluyendo un diagrama de caja superior para detectar valores atípicos.
* **📋 Vista Previa Dinámica:** Opción de desplegar un desglose interactivo de las primeras filas del dataset filtrado mediante un componente `st.dataframe` optimizado.
* **💡 Respaldo de Datos Integrado:** Cuenta con un mecanismo de simulación de datos en caso de que el archivo físico no se encuentre presente en la primera ejecución.

---