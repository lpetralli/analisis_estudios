import streamlit as st
import pandas as pd 

st.title('Data Pacientes')


pacientes = pd.read_excel('Pacientes_Ejemplo.xlsx')



st.write('Pacientes que vamos a usar simulando el dataset que encontraron: ')
st.dataframe(pacientes, hide_index= True)

st.session_state['usuario_encontrado'] = False

