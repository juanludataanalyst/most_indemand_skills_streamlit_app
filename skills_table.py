import pandas as pd
import json

# Leer el archivo JSON
with open("output_data/joined_data_mapped.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convertir el JSON a un DataFrame
df = pd.DataFrame(data)

# Desglosar la lista de skills en filas individuales, manteniendo todas las apariciones
skills_df = df.explode('skills')

# Seleccionar solo las columnas necesarias para el análisis, incluyendo 'source' y 'date'
skills_df = skills_df[['job_id', 'skills', 'country', 'role', 'title', 'source', 'date']]

# Guardar el resultado en un archivo CSV
skills_df.to_csv('output_data/skills_data_table.csv', index=False)

print("Archivo 'skills_data_table.csv' creado con éxito. Aquí tienes un adelanto:")
print(skills_df.head())