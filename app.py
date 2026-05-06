import streamlit as st
import pandas as pd
from database import crear_tabla, guardar_activo, cargar_activos, guardar_amef, cargar_amef_por_equipo

# ==========================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================
st.set_page_config(page_title="APM Confiabilidad", layout="wide")
crear_tabla()

st.title("🛡️ APM - Asset Performance Management")

# Cargamos los datos globales
df_activos = cargar_activos()

# ==========================================
# CREACIÓN DE NAVEGACIÓN POR PESTAÑAS
# ==========================================
tab_registro, tab_amef, tab_dashboard = st.tabs([
    "🏭 1. Gestión de Activos", 
    "⚙️ 2. Motor RCM (AMEF)", 
    "📊 3. Dashboard Gerencial"
])

# ==========================================
# PESTAÑA 1: REGISTRO Y MATRIZ
# ==========================================
with tab_registro:
    with st.form("nuevo_activo"):
        st.subheader("Registrar Nuevo Equipo")
        
        # Menú desplegable con opción de ingreso manual (¡Tu corrección anterior!)
        sistemas_comunes = [
            "Sistema de Propulsión Principal",
            "Sistema de Generación Eléctrica",
            "Sistema de Bombeo y Lastre",
            "Otra Máquina/Sistema (Ingresar nuevo)"
        ]
        seleccion = st.selectbox("Pertenece a la Máquina/Sistema:", sistemas_comunes)
        
        if seleccion == "Otra Máquina/Sistema (Ingresar nuevo)":
            sistema_seleccionado = st.text_input("Escriba el nombre de la nueva máquina:")
        else:
            sistema_seleccionado = seleccion
        
        col1, col2 = st.columns(2)
        with col1:
            tag = st.text_input("TAG del Equipo (Ej: BOM-101)")
            nombre = st.text_input("Nombre del Equipo")
        with col2:
            frec_falla = st.slider("Frecuencia de Falla (1-10)", 1, 10, 5)
            cons_falla = st.slider("Consecuencia (1-10)", 1, 10, 5)
        
        submit = st.form_submit_button("Guardar en Base de Datos")

    if submit:
        if tag and nombre and sistema_seleccionado:
            guardar_activo(sistema_seleccionado, tag, nombre, frec_falla, cons_falla)
            st.success(f"✅ Activo {tag} guardado correctamente.")
            st.rerun() # Recarga la página automáticamente
        else:
            st.warning("⚠️ Faltan datos por completar.")

    st.divider()
    if not df_activos.empty:
        st.subheader("📋 Inventario de Equipos")
        st.dataframe(df_activos, use_container_width=True)
        csv = df_activos.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar Excel (CSV)", data=csv, file_name="inventario.csv", mime="text/csv")
    else:
        st.info("Aún no hay equipos registrados.")

# ==========================================
# PESTAÑA 2: MÓDULO AMEF
# ==========================================
with tab_amef:
    st.header("⚙️ Análisis de Modos y Efectos de Falla")
    if not df_activos.empty:
        umbral_critico = st.slider("Umbral de Criticidad para AMEF", min_value=1, max_value=100, value=25)
        equipos_criticos = df_activos[df_activos['criticidad'] >= umbral_critico]
        
        if not equipos_criticos.empty:
            st.error(f"⚠️ {len(equipos_criticos)} equipo(s) en zona de riesgo requieren AMEF.")
            lista_tags = equipos_criticos['tag'].tolist()
            tag_seleccionado = st.selectbox("Seleccione un equipo crítico:", lista_tags)
            
            with st.form("formulario_amef"):
                funcion = st.text_area("Función del Sistema")
                falla_funcional = st.text_area("Falla Funcional")
                col_a1, col_a2 = st.columns(2)
                with col_a1: modo_falla = st.text_input("Modo de Falla (Causa Raíz)")
                with col_a2: efecto = st.text_input("Efecto de la Falla")
                btn_amef = st.form_submit_button("Guardar AMEF")
                
            if btn_amef and funcion and modo_falla:
                guardar_amef(tag_seleccionado, funcion, falla_funcional, modo_falla, efecto)
                st.success("✅ AMEF registrado.")
                st.rerun()
            
            st.subheader(f"Historial AMEF: {tag_seleccionado}")
            df_amef = cargar_amef_por_equipo(tag_seleccionado)
            if not df_amef.empty: st.dataframe(df_amef, use_container_width=True)
        else:
            st.success("🎉 Ningún equipo supera el umbral crítico.")
    else:
        st.warning("Debe registrar activos primero.")

# ==========================================
# PESTAÑA 3: DASHBOARD GERENCIAL (¡LO NUEVO!)
# ==========================================
with tab_dashboard:
    st.header("📊 Panel de Indicadores de Confiabilidad (KPIs)")
    
    if not df_activos.empty:
        # --- MOTOR DE SIMULACIÓN MATEMÁTICA ---
        # Calculamos KPIs inferidos basados en la matriz cualitativa
        df_kpi = df_activos.copy()
        df_kpi['MTBF_horas'] = (11 - df_kpi['frecuencia']) * 720 # Mientras menor frecuencia, mayor MTBF
        df_kpi['MTTR_horas'] = df_kpi['consecuencia'] * 3.5      # Mientras mayor consecuencia, mayor tiempo de reparación
        df_kpi['Disponibilidad_%'] = (df_kpi['MTBF_horas'] / (df_kpi['MTBF_horas'] + df_kpi['MTTR_horas'])) * 100
        
        # --- VISTA 1: TARJETAS GLOBALES (KPIs de la Planta) ---
        st.subheader("Estado Global de la Instalación")
        col_k1, col_k2, col_k3, col_k4 = st.columns(4)
        col_k1.metric("Total Activos", len(df_kpi))
        col_k2.metric("Disponibilidad Promedio", f"{df_kpi['Disponibilidad_%'].mean():.1f} %")
        col_k3.metric("MTBF Promedio", f"{int(df_kpi['MTBF_horas'].mean())} hrs")
        col_k4.metric("MTTR Promedio", f"{df_kpi['MTTR_horas'].mean():.1f} hrs")
        
        st.divider()
        
        # --- VISTA 2: ANÁLISIS POR SISTEMA ---
        st.subheader("Desempeño por Máquina / Sistema")
        
        col_graf1, col_graf2 = st.columns(2)
        
        with col_graf1:
            st.write("**Criticidad Promedio por Sistema**")
            # Agrupamos por sistema y sacamos el promedio
            kpi_sistema = df_kpi.groupby('sistema')['criticidad'].mean().reset_index()
            st.bar_chart(data=kpi_sistema, x='sistema', y='criticidad', color="#FF4B4B")
            
        with col_graf2:
            st.write("**Matriz de Riesgo Global**")
            st.scatter_chart(data=df_kpi, x="consecuencia", y="frecuencia", size="criticidad", color="#FFA500")

        # --- VISTA 3: TABLA DE DETALLE TÉCNICO ---
        st.divider()
        st.subheader("Detalle Analítico por Equipo")
        # Mostramos solo las columnas que le importan a gerencia
        df_mostrar = df_kpi[['sistema', 'tag', 'nombre', 'MTBF_horas', 'MTTR_horas', 'Disponibilidad_%']]
        st.dataframe(df_mostrar.style.format({
            'MTBF_horas': '{:.0f}', 
            'MTTR_horas': '{:.1f}', 
            'Disponibilidad_%': '{:.2f}%'
        }), use_container_width=True)

    else:
        st.info("Ingresa equipos en la Pestaña 1 para visualizar el Dashboard.")