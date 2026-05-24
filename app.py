import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# ======================================
# CONFIGURACIÓN DE PÁGINA
# ======================================
st.set_page_config(
    page_title="Pronóstico de Ventas · Adidas USA",
    page_icon="👟",
    layout="centered"
)

# ======================================
# CSS PERSONALIZADO
# ======================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=Barlow+Condensed:wght@700;800&display=swap');

html, body, [class*="css"] { font-family: 'Barlow', sans-serif; }
.stApp { background-color: #0a0a0a; color: #f0f0f0; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 700px; }

.header-band {
    background: #111111; border-left: 5px solid #00c74d;
    border-radius: 4px; padding: 1.5rem 1.75rem; margin-bottom: 2rem;
}
.header-band h1 {
    font-family: 'Barlow Condensed', sans-serif; font-size: 2.4rem;
    font-weight: 800; color: #ffffff; letter-spacing: 0.04em;
    text-transform: uppercase; margin: 0 0 0.25rem 0; line-height: 1;
}
.header-band .tag {
    display: inline-block; background: #00c74d; color: #003318;
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.15em;
    text-transform: uppercase; padding: 3px 10px; border-radius: 2px; margin-bottom: 0.75rem;
}
.header-band p { color: #888888; font-size: 0.9rem; margin: 0; }

.section-label {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.18em;
    text-transform: uppercase; color: #555555;
    margin: 1.5rem 0 0.75rem 0; border-bottom: 1px solid #1e1e1e; padding-bottom: 0.4rem;
}
label, .stNumberInput label, .stSelectbox label, .stSlider label {
    color: #aaaaaa !important; font-size: 0.82rem !important;
    font-weight: 500 !important; letter-spacing: 0.04em !important; text-transform: uppercase !important;
}
.stNumberInput input {
    background-color: #161616 !important; border: 1px solid #2a2a2a !important;
    border-radius: 4px !important; color: #f0f0f0 !important;
    font-family: 'Barlow', sans-serif !important; font-size: 1rem !important; font-weight: 600 !important;
}
.stNumberInput input:focus {
    border-color: #00c74d !important; box-shadow: 0 0 0 2px rgba(0,199,77,0.15) !important;
}
.stSelectbox > div > div {
    background-color: #161616 !important; border: 1px solid #2a2a2a !important;
    border-radius: 4px !important; color: #f0f0f0 !important;
}
.stSlider [data-testid="stSliderThumb"] { background: #00c74d !important; border: none !important; }
.stSlider [data-testid="stSliderTrackFill"] { background: #00c74d !important; }

.stButton > button {
    background: #00c74d !important; color: #002a10 !important; border: none !important;
    border-radius: 4px !important; font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 1.05rem !important; font-weight: 800 !important; letter-spacing: 0.12em !important;
    text-transform: uppercase !important; padding: 0.65rem 2rem !important;
    width: 100% !important; margin-top: 1.5rem !important; transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: #00e858 !important; transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(0,199,77,0.3) !important;
}

.result-box {
    background: #0d1f13; border: 1px solid #00c74d;
    border-radius: 6px; padding: 1.5rem 2rem; margin-top: 1.5rem; text-align: center;
}
.result-box .result-label {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.2em;
    text-transform: uppercase; color: #00c74d; margin-bottom: 0.5rem;
}
.result-box .result-value {
    font-family: 'Barlow Condensed', sans-serif; font-size: 3rem;
    font-weight: 800; color: #ffffff; letter-spacing: 0.02em; line-height: 1;
}
.result-box .result-context { font-size: 0.75rem; color: #558866; margin-top: 0.6rem; letter-spacing: 0.05em; }

/* Insight cards */
.insight-card {
    border-radius: 6px; padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem; display: flex; align-items: flex-start; gap: 0.75rem;
}
.insight-green  { background: #0d1f13; border: 1px solid #1a4a2a; }
.insight-yellow { background: #1f1a00; border: 1px solid #4a3a00; }
.insight-icon { font-size: 1.1rem; margin-top: 1px; }
.insight-title {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; margin-bottom: 0.2rem;
}
.insight-green  .insight-title { color: #00c74d; }
.insight-yellow .insight-title { color: #f0c030; }
.insight-body { font-size: 0.85rem; color: #cccccc; line-height: 1.5; }

thead tr th {
    background-color: #1a1a1a !important; color: #00c74d !important;
    font-size: 0.72rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important;
}
tbody tr td { color: #e0e0e0 !important; font-size: 0.85rem !important; }
tbody tr:hover td { background-color: #1a2a1e !important; }

.btn-limpiar button {
    background: transparent !important; color: #ff4444 !important;
    border: 1px solid #ff4444 !important; font-size: 0.75rem !important;
    padding: 0.3rem 1rem !important; margin-top: 0.5rem !important; width: auto !important;
}
</style>
""", unsafe_allow_html=True)

# ======================================
# CARGAR MODELO
# ======================================
modelo = joblib.load("modelo_xgboost.pkl")

# ======================================
# INICIALIZAR SESSION STATE
# ======================================
if "historial" not in st.session_state:
    st.session_state.historial = []

# ======================================
# FUNCIÓN AUXILIAR
# ======================================
def construir_datos(price, units, margin, yr, mo, dy, dow, reg, ret, method):
    return pd.DataFrame({
        'Unnamed: 0': [0], 'Retailer ID': [1185732],
        'Price per Unit': [price], 'Units Sold': [units],
        'Operating Profit': [0], 'Operating Margin': [margin],
        'año': [yr], 'mes': [mo], 'dia': [dy], 'dia_semana': [dow],
        'Region_Northeast':       [1 if reg == "Northeast"  else 0],
        'Region_South':           [1 if reg == "South"      else 0],
        'Region_Southeast':       [1 if reg == "Southeast"  else 0],
        'Region_West':            [1 if reg == "West"       else 0],
        'Sales Method_Online':    [1 if method == "Online"  else 0],
        'Sales Method_Outlet':    [1 if method == "Outlet"  else 0],
        'Retailer_Foot Locker':   [1 if ret == "Foot Locker"   else 0],
        "Retailer_Kohl's":        [1 if ret == "Kohl's"        else 0],
        'Retailer_Sports Direct': [1 if ret == "Sports Direct" else 0],
        'Retailer_Walmart':       [1 if ret == "Walmart"       else 0],
        'Retailer_West Gear':     [1 if ret == "West Gear"     else 0],
    })

# ======================================
# HEADER
# ======================================
st.markdown("""
<div class="header-band">
    <div class="tag">Modelo Predictivo · XGBoost</div>
    <h1>Pronóstico de Ventas</h1>
    <p>Predicción de demanda de ropa y calzado deportivo Adidas USA</p>
</div>
""", unsafe_allow_html=True)

# ======================================
# ENTRADAS
# ======================================
st.markdown('<div class="section-label">Parámetros del producto</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    price_per_unit = st.number_input("Precio por unidad ($)", min_value=0.0, step=1.0, format="%.2f")
with col2:
    units_sold = st.number_input("Cantidad vendida", min_value=0, step=1)
operating_margin = st.number_input("Margen operativo (%)", min_value=0.0, max_value=100.0, step=0.5, format="%.2f")

st.markdown('<div class="section-label">Segmento de mercado</div>', unsafe_allow_html=True)
col_a, col_b, col_c = st.columns(3)
with col_a:
    region = st.selectbox("Región", ["Northeast", "South", "Southeast", "West", "Midwest"])
with col_b:
    retailer = st.selectbox("Retailer", ["Foot Locker", "Walmart", "Sports Direct", "West Gear", "Kohl's", "Amazon"])
with col_c:
    sales_method = st.selectbox("Canal de venta", ["Online", "In-store", "Outlet"])

st.markdown('<div class="section-label">Fecha de proyección</div>', unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    year = st.selectbox("Año", [2025, 2026, 2027])
with col4:
    dias_semana = {0:"Lunes",1:"Martes",2:"Miércoles",3:"Jueves",4:"Viernes",5:"Sábado",6:"Domingo"}
    day_of_week_label = st.selectbox("Día de la semana", list(dias_semana.values()))
    day_of_week = {v: k for k, v in dias_semana.items()}[day_of_week_label]
col5, col6 = st.columns(2)
with col5:
    month = st.slider("Mes", 1, 12, 1)
with col6:
    day = st.slider("Día", 1, 31, 1)

# ======================================
# BOTÓN Y PREDICCIÓN
# ======================================
if st.button("⚡  Generar pronóstico"):
    datos = construir_datos(price_per_unit, units_sold, operating_margin,
                            year, month, day, day_of_week, region, retailer, sales_method)
    valor = modelo.predict(datos)[0]

    st.session_state.historial.append({
        "Fecha":          f"{day:02d}/{month:02d}/{year}",
        "Retailer":       retailer,
        "Región":         region,
        "Canal":          sales_method,
        "Precio ($)":     f"{price_per_unit:,.2f}",
        "Cant.":          units_sold,
        "Margen (%)":     f"{operating_margin:.1f}",
        "Pronóstico ($)": f"{valor:,.2f}",
    })

    st.markdown(f"""
    <div class="result-box">
        <div class="result-label">Pronóstico estimado de ventas</div>
        <div class="result-value">${valor:,.2f}</div>
        <div class="result-context">{retailer} · {region} · {sales_method}</div>
    </div>
    """, unsafe_allow_html=True)

    # ======================================
    # CÁLCULOS PARA GRÁFICAS E INSIGHTS
    # ======================================
    retailers_todos = ["Foot Locker", "Walmart", "Sports Direct", "West Gear", "Kohl's", "Amazon"]
    valores_ret = [modelo.predict(construir_datos(price_per_unit, units_sold, operating_margin,
                   year, month, day, day_of_week, region, r, sales_method))[0] for r in retailers_todos]

    regiones_todas = ["Northeast", "South", "Southeast", "West", "Midwest"]
    valores_reg = [modelo.predict(construir_datos(price_per_unit, units_sold, operating_margin,
                   year, month, day, day_of_week, r, retailer, sales_method))[0] for r in regiones_todas]

    canales_todos = ["Online", "In-store", "Outlet"]
    valores_can = [modelo.predict(construir_datos(price_per_unit, units_sold, operating_margin,
                   year, month, day, day_of_week, region, retailer, c))[0] for c in canales_todos]

    # ======================================
    # INSIGHTS
    # ======================================
    st.markdown('<div class="section-label">Insights</div>', unsafe_allow_html=True)

    # Insight 1: Mejor retailer
    mejor_ret_idx  = valores_ret.index(max(valores_ret))
    mejor_ret_nom  = retailers_todos[mejor_ret_idx]
    mejor_ret_val  = valores_ret[mejor_ret_idx]
    dif_ret_pct    = ((mejor_ret_val - valor) / valor * 100) if valor > 0 else 0

    if mejor_ret_nom == retailer:
        st.markdown(f"""
        <div class="insight-card insight-green">
            <div class="insight-icon">🏆</div>
            <div>
                <div class="insight-title">Retailer óptimo</div>
                <div class="insight-body"><b>{retailer}</b> es el retailer con mayor pronóstico de ventas
                (${mejor_ret_val:,.0f}) para los parámetros ingresados. ¡Buena elección!</div>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="insight-card insight-yellow">
            <div class="insight-icon">⚠️</div>
            <div>
                <div class="insight-title">Retailer con mayor potencial</div>
                <div class="insight-body"><b>{mejor_ret_nom}</b> supera a {retailer} en un
                <b>{dif_ret_pct:.1f}%</b> (${mejor_ret_val:,.0f} vs ${valor:,.0f}).
                Considera cambiar el retailer para maximizar ventas.</div>
            </div>
        </div>""", unsafe_allow_html=True)

    # Insight 2: Mejor región
    mejor_reg_idx  = valores_reg.index(max(valores_reg))
    mejor_reg_nom  = regiones_todas[mejor_reg_idx]
    mejor_reg_val  = valores_reg[mejor_reg_idx]
    promedio_reg   = sum(valores_reg) / len(valores_reg)
    dif_reg_pct    = ((mejor_reg_val - promedio_reg) / promedio_reg * 100) if promedio_reg > 0 else 0

    if mejor_reg_nom == region:
        st.markdown(f"""
        <div class="insight-card insight-green">
            <div class="insight-icon">📍</div>
            <div>
                <div class="insight-title">Región óptima</div>
                <div class="insight-body"><b>{region}</b> es la región con mayor potencial de ventas,
                un <b>{dif_reg_pct:.1f}%</b> por encima del promedio de todas las regiones (${promedio_reg:,.0f}).</div>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        dif_reg_vs_sel = ((mejor_reg_val - valores_reg[regiones_todas.index(region)]) /
                          valores_reg[regiones_todas.index(region)] * 100) if valores_reg[regiones_todas.index(region)] > 0 else 0
        st.markdown(f"""
        <div class="insight-card insight-yellow">
            <div class="insight-icon">⚠️</div>
            <div>
                <div class="insight-title">Región con mayor potencial</div>
                <div class="insight-body"><b>{mejor_reg_nom}</b> supera a {region} en un
                <b>{dif_reg_vs_sel:.1f}%</b> (${mejor_reg_val:,.0f} vs ${valores_reg[regiones_todas.index(region)]:,.0f}).
                Considera enfocarte en esa región.</div>
            </div>
        </div>""", unsafe_allow_html=True)

    # Insight 3: Mejor canal
    mejor_can_idx = valores_can.index(max(valores_can))
    mejor_can_nom = canales_todos[mejor_can_idx]
    mejor_can_val = valores_can[mejor_can_idx]

    if mejor_can_nom == sales_method:
        st.markdown(f"""
        <div class="insight-card insight-green">
            <div class="insight-icon">🛒</div>
            <div>
                <div class="insight-title">Canal óptimo</div>
                <div class="insight-body"><b>{sales_method}</b> es el canal de venta con mejor
                desempeño proyectado (${mejor_can_val:,.0f}) frente a los demás canales disponibles.</div>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        dif_can_pct = ((mejor_can_val - valores_can[canales_todos.index(sales_method)]) /
                       valores_can[canales_todos.index(sales_method)] * 100) if valores_can[canales_todos.index(sales_method)] > 0 else 0
        st.markdown(f"""
        <div class="insight-card insight-yellow">
            <div class="insight-icon">⚠️</div>
            <div>
                <div class="insight-title">Canal con mayor potencial</div>
                <div class="insight-body"><b>{mejor_can_nom}</b> supera a {sales_method} en un
                <b>{dif_can_pct:.1f}%</b> (${mejor_can_val:,.0f} vs ${valores_can[canales_todos.index(sales_method)]:,.0f}).
                Considera cambiar el canal de venta.</div>
            </div>
        </div>""", unsafe_allow_html=True)

    # Insight 4: Alerta si ningún parámetro es óptimo
    ret_optimo = mejor_ret_nom == retailer
    reg_optimo = mejor_reg_nom == region
    can_optimo = mejor_can_nom == sales_method

    if not ret_optimo and not reg_optimo and not can_optimo:
        st.markdown(f"""
        <div class="insight-card insight-yellow">
            <div class="insight-icon">🔴</div>
            <div>
                <div class="insight-title">Segmento no óptimo</div>
                <div class="insight-body">Ninguno de los tres parámetros seleccionados
                (retailer, región y canal) corresponde al de mayor rendimiento.
                La combinación óptima sería: <b>{mejor_ret_nom} · {mejor_reg_nom} · {mejor_can_nom}</b>.</div>
            </div>
        </div>""", unsafe_allow_html=True)

    # ======================================
    # GRÁFICAS
    # ======================================
    def hacer_grafica(categorias, valores, seleccion, altura=300):
        colores = ["#00c74d" if c == seleccion else "#2a2a2a" for c in categorias]
        fig = go.Figure(go.Bar(
            x=categorias, y=valores,
            marker_color=colores,
            text=[f"${v:,.0f}" for v in valores],
            textposition="outside",
            textfont=dict(color="#cccccc", size=11),
        ))
        fig.update_layout(
            paper_bgcolor="#0a0a0a", plot_bgcolor="#111111",
            font=dict(family="Barlow, sans-serif", color="#aaaaaa"),
            margin=dict(t=20, b=20, l=10, r=10), height=altura,
            xaxis=dict(showgrid=False, tickfont=dict(size=11)),
            yaxis=dict(showgrid=True, gridcolor="#1e1e1e", tickprefix="$", tickfont=dict(size=10)),
            showlegend=False,
        )
        return fig

    st.markdown('<div class="section-label">Comparación por retailer</div>', unsafe_allow_html=True)
    st.plotly_chart(hacer_grafica(retailers_todos, valores_ret, retailer), use_container_width=True)

    st.markdown('<div class="section-label">Comparación por región</div>', unsafe_allow_html=True)
    st.plotly_chart(hacer_grafica(regiones_todas, valores_reg, region), use_container_width=True)

    st.markdown('<div class="section-label">Comparación por canal de venta</div>', unsafe_allow_html=True)
    st.plotly_chart(hacer_grafica(canales_todos, valores_can, sales_method, altura=260), use_container_width=True)

# ======================================
# HISTORIAL
# ======================================
if st.session_state.historial:
    st.markdown('<div class="section-label">Historial de pronósticos</div>', unsafe_allow_html=True)
    df_historial = pd.DataFrame(st.session_state.historial)
    st.dataframe(df_historial, use_container_width=True, hide_index=True)

    csv = df_historial.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇  Exportar historial como CSV",
        data=csv, file_name="pronosticos_adidas.csv", mime="text/csv",
    )

    st.markdown('<div class="btn-limpiar">', unsafe_allow_html=True)
    if st.button("🗑  Limpiar historial"):
        st.session_state.historial = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
