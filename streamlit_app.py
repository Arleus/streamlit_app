import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Función para cargar datos desde un archivo local con la codificación correcta
@st.cache_data()
def load_data(file_path):
    try:
        # Intenta leer el archivo CSV con diferentes codificaciones
        data = pd.read_csv(file_path, encoding='latin1')
    except UnicodeDecodeError:
        # Si hay un error de decodificación, intenta con utf-8
        data = pd.read_csv(file_path, encoding='utf-8')
    except Exception as e:
        # Maneja otras excepciones, por ejemplo, si la ruta del archivo es incorrecta
        st.error(f"Error al cargar el archivo: {e}")
        return None
    return data

# Especificar la ruta del archivo CSV
file_path = r'C:\Users\Arturo\streamlit_app\microdato.csv'

# Cargar datos desde el archivo CSV local
data = load_data(file_path)

if data is not None:
    # Título del dashboard
    st.title('Dashboard de Gestión de Inventarios')

    # Mostrar datos
    st.subheader('Datos del Inventario')
    st.write(data)

    # Verificar y mostrar las columnas específicas
    specific_columns = ['id', 'url', 'supermarket', 'zip_code', 'category', 'name', 'description', 
                        'trademark', 'trademark_propietary_flag', 'price', 'reference_price', 
                        'reference_unit', 'offer_flag', 'offer_price', 'offer_type', 'insert_date']
    
    missing_columns = [col for col in specific_columns if col not in data.columns]
    
    if not missing_columns:
        # Mostrar las columnas específicas en una tabla
        st.subheader('Columnas Específicas')
        st.write(data[specific_columns])

        # Selección manual de columnas para gráfico de líneas
        st.subheader('Análisis de Precios')
        selected_columns = st.multiselect('Selecciona columnas para el gráfico de líneas', 
                                          options=['price', 'offer_price', 'reference_price'],
                                          default=['price'])

        if selected_columns:
            st.line_chart(data[selected_columns])
        else:
            st.info('Selecciona al menos una columna para visualizar el gráfico.')

    else:
        st.error(f"No se encontraron todas las columnas necesarias: {missing_columns}")

    # Filtros y visualizaciones adicionales
    # Por ejemplo, puedes añadir un filtro por categoría
    category = st.selectbox('Selecciona la Categoría', data['category'].unique())
    filtered_data = data[data['category'] == category]
    st.write(filtered_data)

    # Análisis exploratorio de datos
    st.subheader('Análisis Exploratorio de Datos')

    if 'category' in data.columns:  
        category_counts = data['category'].value_counts()
        plt.figure(figsize=(10, 6))
        sns.barplot(x=category_counts.index, y=category_counts.values)
        plt.title('Distribución de Categorías')
        plt.xlabel('Categoría')
        plt.ylabel('Cantidad')
        plt.xticks(rotation=45)

        fig, ax = plt.gcf(), plt.gca()
        st.pyplot(fig)

    # Indicadores de gestión
    st.subheader('Indicadores de Gestión')

    total_registros = len(data)
    promedio_precios = data['price'].mean()

    st.write(f'Total de Registros: {total_registros}')
    st.write(f'Promedio de Precios: ${promedio_precios:.2f}')

else:
    st.error("No se pudo cargar el dataset. Por favor, verifica la ruta del archivo.")