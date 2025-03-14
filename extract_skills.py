import json
import os
import hashlib
import re
from datetime import datetime

# Cargar diccionario de tecnologías/skills
with open('data/skills_definition.json', 'r', encoding='utf-8') as f:
    skills = json.load(f)

# Crear patrones de expresiones regulares para las tecnologías
patterns = {key: re.compile(r'\b(' + '|'.join(map(re.escape, variations)) + r')\b', re.IGNORECASE)
            for key, variations in skills.items()}

# Función para generar un ID único basado en date, title y source
def generate_unique_id(date, title, source):
    # Si date no está presente, usamos una cadena por defecto
    date = date if date else "Unknown"
    unique_string = f"{date}_{title}_{source}"
    return hashlib.md5(unique_string.encode('utf-8')).hexdigest()

# Función para extraer skills de la descripción
def extract_skills(description):
    found_skills = set()
    if not description:
        return []
    for key, pattern in patterns.items():
        if pattern.search(description):
            found_skills.add(key)
    return list(found_skills)

# Función para procesar una oferta de trabajo
def process_job(job, source):
    # Campos obligatorios con valores por defecto si faltan
    processed = {
        "id": generate_unique_id(
            job.get("date", "Unknown"),  # Usamos el campo date de la oferta
            job.get("title", "Unknown"),
            source
        ),
        "title": job.get("title", "Not specified"),
        "company": job.get("company", "Not specified"),
        "date": job.get("date", "Not specified"),
        "description": job.get("description", "Not specified"),
        "link": job.get("link", "Not specified"),
        "location": job.get("location", "Not available"),
        "source": source,
        "skills": extract_skills(job.get("description", ""))
    }

    # Campos opcionales (solo se incluyen si están presentes)
    optional_fields = [
        "type", "category", "tags", "salary", "salary_min", "salary_max",
        "id_source", "employment_type", "jobtype", "region", "pubDate"
    ]
    for field in optional_fields:
        if field in job:
            processed[field] = job[field]

    return processed

# Función para procesar archivos JSON de todas las fuentes y eliminar duplicados
def process_json_files(directory):
    processed_data = []
    seen_ids = set()  # Para rastrear IDs únicos y eliminar duplicados
    sources = [
        "aijobs", "remotive", "remoteok", "weworkremotely", "jobicy", "jobscollider"
    ]

    for source in sources:
        source_path = os.path.join(directory, source)
        if os.path.exists(source_path):
            for file_name in os.listdir(source_path):
                if file_name.endswith('.json'):
                    file_path = os.path.join(source_path, file_name)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                    except (FileNotFoundError, json.JSONDecodeError) as e:
                        print(f"Error con {file_path}: {e}")
                        continue
                    
                    # Procesar cada oferta en el archivo
                    for job in data:
                        processed_job = process_job(job, source)
                        # Solo añadir si el ID no se ha visto antes
                        if processed_job["id"] not in seen_ids:
                            seen_ids.add(processed_job["id"])
                            processed_data.append(processed_job)
                        else:
                            print(f"Oferta duplicada encontrada y omitida: ID {processed_job['id']}")
        else:
            print(f"Directorio {source_path} no encontrado, omitiendo fuente {source}")

    return processed_data

# Ejecución principal
if __name__ == "__main__":
    data_directory = os.path.join(os.getcwd(), 'data_joboffers')
    processed_data = process_json_files(data_directory)

    output_file_path = os.path.join('output_data', 'joined_data_standar.json')
    os.makedirs('output_data', exist_ok=True)
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, ensure_ascii=False, indent=4)
        print(f"Datos guardados en: {output_file_path}")
        print(f"Total de ofertas procesadas (sin duplicados): {len(processed_data)}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")