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
csv_file_id = '1BbXDXhT7CPh_Ihh8svcOYV2RTPYOLdxH'
csv_data = download_file_from_drive(csv_file_id)
if csv_data:
    data = pd.read_csv(io.StringIO(csv_data))
else:
    data = pd.DataFrame()  # Evitar errores si no hay datos

# Configuración de la barra lateral
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Skills by Role", "Skills to learn","Raw Data Viewer", "Contact"],
        icons=["bar-chart", "book","folder", "envelope"],
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



elif selected == "Skills to learn":
    import json  # Asegúrate de importar json para manejar datos JSON

    st.title("Skills to learn")

    # Diccionario con roles y IDs de archivos en Google Drive
    roles_to_files = {
        "Data Analyst": "1Qp09y7LzPxSxOGNEEWn4zGAypmZQnklh",
        "Data Scientist": "1s32wd6K9Mony3Mz2KUepsW5dIlKBjYkQ",
        "Data Engineer" : "16V2DkWiMQwQBLgxdon7Zv3Hpt2g9OZaQ",
        "Software Engineer" : "1iH47GvvQUXgaC5BcNBwASAJ_WzOmtBOR",
        "Cybersecurity Engineer" : "1Qp09y7LzPxSxOGNEEWn4zGAypmZQnklh"
    }
    selected_role = st.selectbox("Select a role ", list(roles_to_files.keys()))
    file_id = roles_to_files.get(selected_role)
    

    if file_id:
        # Descargar y cargar los datos JSON
        json_data = download_file_from_drive(file_id)
        if json_data:
            try:
                parsed_json = json.loads(json_data)  # Convertir el texto en un objeto JSON
                #st.json(parsed_json)  # Mostrar JSON formateado en Streamlit
            except json.JSONDecodeError:
                st.error("The file is not a valid JSON format.")
        else:
            st.error("Could not load JSON data from Google Drive.")
    else:
        st.error("File ID not found for the selected role.")



        # Convertirlo a un DataFrame
    association_rules_data = pd.DataFrame([
        {
            "antecedent_1": rule["antecedents"][0] if len(rule["antecedents"]) > 0 else None,
            "antecedent_2": rule["antecedents"][1] if len(rule["antecedents"]) > 1 else None,
            "consequent": rule["consequents"][0],
            "support": rule["support"],
            "confidence": rule["confidence"],
            "lift": rule["lift"]
        } for rule in parsed_json
    ])


    association_rules_data["antecedent"] = association_rules_data[["antecedent_1", "antecedent_2"]].fillna("").apply(lambda x: " and ".join(filter(None, x)), axis=1)

#selected_antecedent = st.selectbox("Select a skill you master ", list(association_rules_data["antecedent"].unique()))

        # Crear un selectbox para seleccionar una skill (antecedent)
    selected_antecedent = st.selectbox(
        "Select a skill in which you are a master",
        options=[""] + list(association_rules_data["antecedent"].unique())  # Agrega una opción vacía como inicial
    )

    # Si no hay selección (opción inicial)
    if selected_antecedent == "":
        st.info("Select one to get your next skill to learn")
    else:
        # Filtrar los datos para el antecedente seleccionado
        filtered_data = association_rules_data[association_rules_data["antecedent"] == selected_antecedent]

        # Mostrar los resultados en texto
        if not filtered_data.empty:
            # Obtener la fila con el máximo "confidence"
            row = filtered_data.loc[filtered_data["confidence"].idxmax()]
            st.write(
    f"""
    ### Recommended Skill to Learn ->   <span style="text-align: right; font-size: 1.5em;"> { row['consequent'] } </span> 

    **Why this recommendation?**

    * **High correlation:** **{row['confidence']:.1%}** of the time **{row['antecedent']}** appears in a job posting, **{row['consequent']}** also appears.

    * **Joint frequency:** Both skills appear together in **{row['support']:.2%}** of the analyzed job postings.
    * **Impact on your employability:** By acquiring this skill your chances of finding a job that matches your profile will multiply by a factor of **{row['lift']:.1f}x**
    """,
    unsafe_allow_html=True
)
        else:
            st.write("No data available for the selected skill.")



  
elif selected == "Raw Data Viewer":
    import json  # Asegúrate de importar json para manejar datos JSON
    
    st.title("Raw Data Viewer")

    

    # Diccionario con roles y IDs de archivos en Google Drive
    roles_to_files = {
        "Data Analyst": "1Qp09y7LzPxSxOGNEEWn4zGAypmZQnklh",
        "Data Scientist": "1s32wd6K9Mony3Mz2KUepsW5dIlKBjYkQ",
        "Data Engineer" : "16V2DkWiMQwQBLgxdon7Zv3Hpt2g9OZaQ",
        "Software Engineer" : "1iH47GvvQUXgaC5BcNBwASAJ_WzOmtBOR",
        "Cybersecurity Engineer" : "1Qp09y7LzPxSxOGNEEWn4zGAypmZQnklh"
    }
    selected_role = st.selectbox("Select a role to view JSON:", list(roles_to_files.keys()))
    file_id = roles_to_files.get(selected_role)

    if file_id:
        # Descargar y cargar los datos JSON
        json_data = download_file_from_drive(file_id)
        if json_data:
            try:
                parsed_json = json.loads(json_data)  # Convertir el texto en un objeto JSON
                
            except json.JSONDecodeError:
                st.error("The file is not a valid JSON format.")
        else:
            st.error("Could not load JSON data from Google Drive.")
    else:
        st.error("File ID not found for the selected role.")


         # Convertirlo a un DataFrame
    association_rules_data = pd.DataFrame([
        {
            "antecedent_1": rule["antecedents"][0] if len(rule["antecedents"]) > 0 else None,
            "antecedent_2": rule["antecedents"][1] if len(rule["antecedents"]) > 1 else None,
            "consequent": rule["consequents"][0],
            "support": rule["support"],
            "confidence": rule["confidence"],
            "lift": rule["lift"]
        } for rule in parsed_json
    ])


    association_rules_data["antecedent"] = association_rules_data[["antecedent_1", "antecedent_2"]].fillna("").apply(lambda x: " and ".join(filter(None, x)), axis=1)




    st.dataframe(association_rules_data.drop(["antecedent_1", "antecedent_2"],axis = 1))
    st.json(parsed_json)  # Mostrar JSON formateado en Streamlit

elif selected == "Contact":
    st.title("Contact Us")
    st.write("For inquiries, please reach out via email.")
    st.write("juanludataanalyst@gmail.com")
