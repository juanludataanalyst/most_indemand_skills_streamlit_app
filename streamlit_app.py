import streamlit as st
import pandas as pd
import requests
import io
import altair as alt
from streamlit_option_menu import option_menu

# Función para descargar archivo desde Google Drive
def download_file_from_drive(file_id):
    file_url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(file_url)
    if response.status_code == 200:
        return response.text
    else:
        st.error("Error al descargar el archivo.")
        return None

# Descargar datos principales (CSV)
csv_file_id = '1zB4kNcj5sje2-jjT8yhuBURlLefHD9bP'
csv_data = download_file_from_drive(csv_file_id)
if csv_data:
    data = pd.read_csv(io.StringIO(csv_data))
else:
    data = pd.DataFrame()  # Evitar errores si no hay datos

# Configuración de la barra lateral - MODIFICADO: eliminado "Skills to learn" y "Raw Data Viewer"
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Skills by Role", "Contact"],  # Eliminadas las opciones no deseadas
        icons=["bar-chart", "envelope"],  # Eliminados los iconos correspondientes
        menu_icon="cast",
        default_index=0,
    )

# Opciones de la aplicación
if selected == "Skills by Role":
    st.title("Top Most in Demand Skills")

    if not data.empty:
        # Menú para seleccionar rol y país
        roles = data['role'].unique()
        selected_role = st.selectbox("Select a role:", roles)
        
        countries = ['All'] + data['country'].unique().tolist()
        selected_country = st.selectbox("Select a country:", countries)

        # Filtrar datos según selección
        if selected_country == 'All':
            df_filtered = data[data['role'] == selected_role]
        else:
            df_filtered = data[(data['role'] == selected_role) & (data['country'] == selected_country)]

        total_jobs = df_filtered['job_id'].nunique()
        skill_counts = df_filtered['skills'].value_counts()
        skills_percentage = (skill_counts / total_jobs * 100).reset_index()
        skills_percentage.columns = ['skill', 'percentage']
        skills_percentage['percentage'] = skills_percentage['percentage'].round(1)
        skills_percentage['percentage'] = skills_percentage['percentage'].astype(float)
        st.markdown(f"**Total Jobs:** {total_jobs}")

        # Crear gráfica
        df_chart = skills_percentage.sort_values("percentage", ascending=False).head(15)
        bars = alt.Chart(df_chart).mark_bar(size=20).encode(
            x=alt.X("percentage:Q", title="Proportion of offers (%)"),
            y=alt.Y("skill:N", sort="-x", title="Skill"),
            color=alt.Color("percentage:Q", scale=alt.Scale(scheme="oranges"), legend=None)
        )
        text = bars.mark_text(
            align="left", baseline="middle", dx=3, fontSize=14
        ).transform_calculate(
            percentage_text="datum.percentage + '%' "  # Agregar el símbolo de porcentaje
        ).encode(
            text=alt.Text("percentage_text:N")  # Usar la columna calculada
        )
        st.altair_chart((bars + text).properties(width=800, height=500))

        # Mostrar tabla
        st.dataframe(skills_percentage.style.format({'percentage': '{:.1f}%'}), use_container_width=True)
    else:
        st.warning("No data available to display.")

# Las secciones "Skills to learn" y "Raw Data Viewer" han sido eliminadas completamente

elif selected == "Contact":
    st.title("Contact Us")
    st.write("For inquiries, please reach out via email.")
    st.write("juanludataanalyst@gmail.com")