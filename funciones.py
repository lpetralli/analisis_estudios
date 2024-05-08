import streamlit as st
import psycopg2
import pandas as pd

# Configuración de la conexión con la base de datos
def get_db_connection():
    user = 'mpxkpnvb'
    password = 'xF3SiYaL2rtKywEaWFkDm8MMVM76L1Bs'
    host = 'berry.db.elephantsql.com'
    port = '5432'
    dbname = 'mpxkpnvb'
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return conn

# Defino función para dar de alta usuarios 
def insert_user(dni, nombre, apellido, edad, altura, peso, enfermedad, fuma, ejercicio, alergias, media_globulos_rojos, media_hemoglobina, media_glucosa, media_colesterol):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "INSERT INTO usuarios (dni, nombre, apellido, edad, altura, peso, enfermedad, fuma, ejercicio, alergias, media_globulos_rojos, media_hemoglobina, media_glucosa, media_colesterol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(query, (dni, nombre, apellido, edad, altura, peso, enfermedad, fuma, ejercicio, alergias, media_globulos_rojos, media_hemoglobina, media_glucosa, media_colesterol))
            conn.commit()
            st.success("Usuario registrado exitosamente.")
    except psycopg2.Error as e:
        st.error(f"Se produjo un error al guardar el usuario: {e}")
    finally:
        conn.close()


# Defino una función para insertar estudios
def insert_estudio(dni, globulos_rojos, hemoglobina, glucosa, colesterol, fecha_estudio):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "INSERT INTO estudios (dni, globulos_rojos, hemoglobina, glucosa, colesterol, fecha_estudio) VALUES (%s, %s, %s, %s, %s, %s)"
            cur.execute(query, (dni, globulos_rojos, hemoglobina, glucosa, colesterol, fecha_estudio))
            conn.commit()
            st.success("Estudio registrado exitosamente.")
    except psycopg2.Error as e:
        st.error(f"Se produjo un error al guardar el estudio: {e}")
    finally:
        conn.close()

# Defino una función para validar si el usuario ya existe
def dni_exists(dni):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            query = "SELECT * FROM usuarios WHERE dni = %s"
            cur.execute(query, (dni,))
            result = cur.fetchone()
            return result is not None
    finally:
        conn.close()

# Defino una función para consultar estudios por DNI
def consultar_estudios(dni):
    conn = get_db_connection()
    if conn is None:
        return pd.DataFrame()  # Devolver un DataFrame vacío si no hay conexión

    try:
        # Actualización de la consulta para incluir un INNER JOIN
        query = """
        SELECT e.*, u.media_globulos_rojos, u.media_hemoglobina, u.media_glucosa, u.media_colesterol
        FROM estudios e
        INNER JOIN usuarios u ON e.dni = u.dni
        WHERE e.dni = %s
        """
        df = pd.read_sql(query, conn, params=(dni,))
        return df
    except Exception as e:
        print(f"Error al realizar la consulta: {e}")
        return pd.DataFrame()  # Devolver un DataFrame vacío en caso de error
    finally:
        conn.close()



#Defino la función del cálculo de medias
def analisis_pacientes(dni, nombre, apellido, edad, altura, peso, enfermedad, fuma, ejercicio, alergias):
    # Cargar los datos de los pacientes desde el archivo Excel
    pacientes_df = pd.read_excel('Pacientes_Ejemplo.xlsx')
    
    # Definir los criterios de filtrado basados en los argumentos de la función
    criterios = {
        'edad': edad,
        'enfermedad': enfermedad,
        'fuma': fuma,
        'ejercicio': ejercicio
    }

    # Crear un filtro que solo incluya los criterios no nulos
    filtro = {k: v for k, v in criterios.items() if pd.notna(v)}
    print(f"Filtro aplicado: {filtro}")

    # Filtrar el DataFrame de pacientes basado en el filtro
    subgrupo_df = pacientes_df.loc[(pacientes_df[list(filtro.keys())] == pd.Series(filtro)).all(axis=1)]

    print("Subgrupo filtrado:")
    print(subgrupo_df)

    # Calcular medias de las columnas relevantes
    media_globulos_rojos = subgrupo_df['globulos_rojos'].mean() if 'globulos_rojos' in subgrupo_df.columns else None
    media_hemoglobina = subgrupo_df['hemoglobina'].mean() if 'hemoglobina' in subgrupo_df.columns else None
    media_glucosa = subgrupo_df['glucosa'].mean() if 'glucosa' in subgrupo_df.columns else None
    media_colesterol = subgrupo_df['colesterol'].mean() if 'colesterol' in subgrupo_df.columns else None
    
    return media_globulos_rojos, media_hemoglobina, media_glucosa, media_colesterol