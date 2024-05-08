import streamlit as st
import pandas as pd
from funciones import dni_exists, consultar_estudios
import altair as alt

st.title('Análisis de estudios')

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
    st.subheader('Estudios anteriores')
    data = consultar_estudios(st.session_state['dni'])
    st.dataframe(data, hide_index= True)

    st.subheader('Gráficos')
    st.write('**Selecciona la variable que quieren analizar**')
    variable = st.selectbox('Variable', ('globulos_rojos', 'hemoglobina', 'glucosa', 'colesterol'))

    data['fecha_estudio'] = pd.to_datetime(data['fecha_estudio']) + pd.DateOffset(days=1)
    
    # Crear un gráfico con Altair
    line = alt.Chart(data).mark_line().encode(
        x=alt.X('fecha_estudio', axis=alt.Axis(title='Fecha del Estudio', format='%d/%m/%Y')),
        y=alt.Y(variable, axis=alt.Axis(title=variable))
    )

    points = alt.Chart(data).mark_point(color='red', size=60).encode(
        x='fecha_estudio',
        y=variable,
        tooltip=[alt.Tooltip('fecha_estudio', title='Fecha del Estudio', format='%d/%m/%Y'), alt.Tooltip(variable, title=variable)]
    )

    chart = (line + points).properties(
        title=f'Evolución de {variable}'
    )

    # Mostrar el gráfico en Streamlit
    st.altair_chart(chart, use_container_width=True)
    