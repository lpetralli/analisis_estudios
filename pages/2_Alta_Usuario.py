import streamlit as st
from funciones import insert_user, analisis_pacientes

st.session_state['usuario_encontrado'] = False

st.title('Alta de usuarios')

dni = st.text_input('DNI')
nombre = st.text_input('Nombre')
apellido = st.text_input('Apellido')
edad = st.number_input('Edad', step= 1 )
altura = st.number_input('Altura')
peso = st.number_input('Peso')
enfermedad = st.text_input('¿Tenés alguna enfermedad?')
fuma = st.selectbox('¿Fumás?', ('Sí', 'No'))
ejercicio = st.selectbox('¿Hacés ejercicio?', ('Sí', 'No'))
alergias = st.text_input('¿Tenés alguna alergia?')



# Defino una función para validar que no se repitan los emails

if st.button('Guardar'):
    if not dni or not nombre or not apellido or not edad or not altura or not peso or not enfermedad or not fuma or not ejercicio or not alergias:
        st.error("Por favor, completa todos los campos.")
    else:
        media_globulos_rojos, media_hemoglobina, media_glucosa, media_colesterol = analisis_pacientes(dni, nombre, apellido, edad, altura, peso, enfermedad, fuma, ejercicio, alergias)
        insert_user(dni, nombre, apellido, edad, altura, peso, enfermedad, fuma, ejercicio, alergias, media_globulos_rojos, media_hemoglobina, media_glucosa, media_colesterol)
        
