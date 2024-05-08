import streamlit as st
from funciones import insert_estudio, dni_exists

import streamlit as st

# st.session_state['usuario_encontrado'] = False

st.title('Carga de estudios')

dni = st.text_input('DNI')


if st.button('Buscar'):
    if dni_exists(dni):
        # st.success('Usuario encontrado')
        # Establecer un indicador en el estado de la sesión
        st.session_state['usuario_encontrado'] = True
        st.session_state['dni'] = dni
    else:
        st.error('Usuario no encontrado')
        st.session_state['usuario_encontrado'] = False

# Chequear el estado de la sesión para mantener los campos visibles
if st.session_state.get('usuario_encontrado', False):

    #Datos del estudio
    st.subheader('Cargá los datos de tu estudio:')
    fecha_estudio = st.date_input('Fecha del estudio')
    globulos_rojos = st.number_input('Glóbulos Rojos', step=1)
    hemoglobina = st.number_input('Hemoglobina', step=1)
    glucosa = st.number_input('Glucosa', step=1)
    colesterol = st.number_input('Colesterol', step=1)


    if st.button('Guardar'):
        if not fecha_estudio or not globulos_rojos or not hemoglobina or not glucosa or not colesterol:
            st.error("Por favor, completa todos los campos.")
        else:
            insert_estudio(st.session_state['dni'], globulos_rojos, hemoglobina, glucosa, colesterol, fecha_estudio)
            st.session_state['usuario_encontrado'] = False


    



