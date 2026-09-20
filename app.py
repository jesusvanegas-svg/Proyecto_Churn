import streamlit as st
import pickle
import pandas as pd

# 1. Cargar el modelo
with open('modelo_churn.pkl', 'rb') as archivo:
    modelo = pickle.load(archivo)

# 2. Diseño de la interfaz
st.title("📞 Predictor de Riesgo de Abandono (Churn)")
st.write("Ingrese los datos del ticket para predecir si el cliente nos abandonará.")

# 3. Campos para que el usuario interactúe
tiempo_res = st.number_input("Tiempo de Resolución (Minutos)", min_value=0, value=120)
csat = st.slider("Puntuación CSAT (1-5)", 1, 5, 3)

canal = st.selectbox("Canal de Contacto", ["Chat", "Email", "Redes Sociales", "Telefono"])
agente = st.selectbox("Agente Asignado", ["Agente A", "Agente B", "Agente C", "Agente D"])

if st.button("Predecir Riesgo"):
    # Extraer exactamente las columnas con las que el modelo fue entrenado
    columnas_esperadas = modelo.feature_names_in_
    
    # Crear un DataFrame con 1 fila llena de ceros, usando las columnas que el modelo exige
    datos_entrada = pd.DataFrame(0, index=[0], columns=columnas_esperadas)
    
    # Asignar los valores numéricos ingresados (buscando coincidencias en el nombre)
    for col in columnas_esperadas:
        if 'Tiempo' in col or 'Min' in col:
            datos_entrada[col] = tiempo_res
        elif 'CSAT' in col:
            datos_entrada[col] = csat
            
    # Activar con un 1 la columna del Canal y del Agente seleccionado (si existen en el modelo)
    columna_canal = f'Canal_Contacto_{canal}'
    if columna_canal in columnas_esperadas:
        datos_entrada[columna_canal] = 1
        
    columna_agente = f'Agente_Asignado_{agente}'
    if columna_agente in columnas_esperadas:
        datos_entrada[columna_agente] = 1

    # Hacer la predicción
    prediccion = modelo.predict(datos_entrada)
    
    if prediccion[0] == 1:
        st.error("⚠️ ALTO RIESGO: Es muy probable que este cliente abandone el servicio.")
        st.info("💡 Explicabilidad: Tiempos prolongados combinados con baja satisfacción suelen ser críticos.")
    else:
        st.success("✅ BAJO RIESGO: Cliente retenido.")