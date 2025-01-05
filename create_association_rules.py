import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import json
import numpy as np  # Import numpy for vectorized operations
import os  # Para crear directorios si no existen

# Crear un directorio para guardar los archivos JSON por roles
output_dir = 'output_data/roles'
os.makedirs(output_dir, exist_ok=True)

# Leer el archivo CSV de habilidades
skills_df = pd.read_csv('output_data/skills_data_table.csv')

# Iterar sobre cada role único en el DataFrame
roles = skills_df['role'].unique()
for role in roles:
    # Filtrar el DataFrame para el role actual
    role_df = skills_df[skills_df['role'] == role]
    
    # Crear una tabla binaria para el role
    skills_encoded = (
        role_df.groupby(['title', 'skills']).size().unstack(fill_value=0)
        .transform(lambda x: x > 0)  # Convertir a booleanos (True/False)
    )
    
    # Aplicar el algoritmo Apriori
    frequent_itemsets = apriori(skills_encoded, min_support=0.1, use_colnames=True)
    
    # Generar las reglas de asociación (sin `num_itemsets`)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1, num_itemsets=2)
    
    # Crear una estructura simplificada para el JSON
    simplified_rules = []
    for _, row in rules.iterrows():
        antecedents = list(row['antecedents'])
        consequents = list(row['consequents'])
        
        simplified_rules.append({
            "antecedents": antecedents,
            "consequents": consequents,
            "support": row['support'],
            "confidence": row['confidence'],
            "lift": row['lift']
        })
    
    # Guardar las reglas en un archivo JSON
    role_file = f"{output_dir}/{role}_association_rules.json"
    with open(role_file, 'w') as f:
        json.dump(simplified_rules, f, indent=4)
    
    print(f"Archivo JSON creado para el role: {role}")
