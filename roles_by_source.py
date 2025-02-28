import json
import pandas as pd
from collections import Counter

# Leer el archivo joined_data.json
with open("output_data/joined_data.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convertir a DataFrame
df = pd.DataFrame(data)

# Fuentes que estamos manejando (excluyendo 'remotive' general)
sources = ['indeed', 'remoteok', 'weworkremotely', 'jobicy']

# Diccionario para almacenar roles por fuente
roles_by_source = {}

# Analizar roles por cada fuente principal
for source in sources:
    source_df = df[df['source'] == source]
    if not source_df.empty:
        role_counts = Counter(source_df['role'].dropna())
        roles_by_source[source] = role_counts
    else:
        roles_by_source[source] = Counter()

# Separar Remotive histórico y feed
remotive_historic_df = df[(df['source'] == 'remotive') & (df['job_id'].apply(lambda x: len(str(x)) > 10))]  # Hash largo
remotive_feed_df = df[(df['source'] == 'remotive') & (df['job_id'].apply(lambda x: len(str(x)) <= 10))]  # ID corto
roles_by_source['remotive_historic'] = Counter(remotive_historic_df['role'].dropna())
roles_by_source['remotive_feed'] = Counter(remotive_feed_df['role'].dropna())

# Imprimir resultados
print("=== Análisis de Roles por Fuente ===")
for source, role_counts in roles_by_source.items():
    print(f"\nFuente: {source}")
    if role_counts:
        total_offers = sum(role_counts.values())
        print(f"Total de ofertas: {total_offers}")
        print("Roles y número de ofertas:")
        for role, count in sorted(role_counts.items()):
            print(f"  - {role}: {count}")
    else:
        print("  (No hay datos para esta fuente)")

# Guardar resultados en un archivo
with open("output_data/roles_analysis.json", "w", encoding="utf-8") as f:
    json.dump(roles_by_source, f, indent=4, ensure_ascii=False)
print("\nResultados guardados en 'output_data/roles_analysis.json'")