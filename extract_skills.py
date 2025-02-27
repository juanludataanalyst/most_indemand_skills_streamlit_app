import json
import re
import os
import hashlib
from bs4 import BeautifulSoup

# Cargar diccionario de tecnologías
with open('data/skills_definition.json', 'r') as f:
    skills = json.load(f)

# Compilar patrones de tecnologías una vez
patterns = {key: re.compile(r'\b(' + '|'.join(map(re.escape, variations)) + r')\b', re.IGNORECASE) 
            for key, variations in skills.items()}

# Funciones comunes
def generate_job_id(description):
    return hashlib.md5(description.encode('utf-8')).hexdigest()

def clean_html(html_text):
    """Limpia etiquetas HTML y devuelve texto plano."""
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.get_text()

def extract_technologies(description):
    """Extrae tecnologías solo del description."""
    found_technologies = set()
    cleaned_description = clean_html(description) if description else ""
    
    for key, pattern in patterns.items():
        if pattern.search(cleaned_description):
            found_technologies.add(key)
    
    return list(found_technologies)

# Procesadores por fuente
def process_source_indeed(job, date, country, role):
    title = job.get("title", "")
    company = job.get("company", "")
    description = job.get("description", "")
    salary = job.get("salary", "No especificado")
    employment_type = job.get("employment_type", "No especificado")
    technologies = extract_technologies(description)
    job_id = generate_job_id(description)
    location = company.split('\n')[1] if '\n' in company else "Ubicación no especificada"
    company_cleaned = company.split('\n')[0] if '\n' in company else company

    return {
        "job_id": job_id,
        "title": title,
        "company": company_cleaned,
        "location": location,
        "skills": technologies,
        "tags": [],
        "salary": salary,
        "employment_type": employment_type,
        "date": date,
        "country": country,
        "role": role
    }

def process_source_remotive(job, subdir_date):
    title = job.get("title", "")
    company = job.get("company_name", "")
    description = job.get("description", "")
    salary = job.get("salary", "No especificado") or "No especificado"
    employment_type = job.get("job_type", "No especificado").replace("_", " ").title()
    tags = job.get("tags", [])
    technologies = extract_technologies(description)
    job_id = generate_job_id(description)
    location = job.get("candidate_required_location", "Ubicación no especificada")
    role = job.get("category", "Rol no especificado")
    date = job.get("publication_date", subdir_date).split('T')[0]
    country = location if any(c in location.lower() for c in ["colombia", "india", "us"]) else location

    return {
        "job_id": job_id,
        "title": title,
        "company": company,
        "location": location,
        "skills": technologies,
        "tags": tags,
        "salary": salary,
        "employment_type": employment_type,
        "date": date,
        "country": country,
        "role": role
    }

def process_source_remoteok(job, subdir_date):
    title = job.get("position", "")
    company = job.get("company", "")
    description = job.get("description", "")
    salary = f"${job.get('salary_min', 'No especificado')}-{job.get('salary_max', 'No especificado')}" if job.get('salary_min') else "No especificado"
    employment_type = "No especificado"  # RemoteOK no proporciona este dato explícitamente
    tags = job.get("tags", [])
    technologies = extract_technologies(description)
    job_id = generate_job_id(description)
    location = job.get("location", "Ubicación no especificada")
    role = next((tag for tag in tags if tag in ["design", "sales", "qa", "devops", "crypto"]), title.split()[0])  # Inferir rol desde tags o título
    date = job.get("date", subdir_date).split('T')[0]
    country = location if any(c in location.lower() for c in ["colombia", "india", "us"]) else location

    return {
        "job_id": job_id,
        "title": title,
        "company": company,
        "location": location,
        "skills": technologies,
        "tags": tags,
        "salary": salary,
        "employment_type": employment_type,
        "date": date,
        "country": country,
        "role": role
    }

# Función principal para procesar archivos
def process_json_files(directory):
    processed_data = []
    
    # Procesar Indeed
    indeed_path = os.path.join(directory, 'indeed')
    if os.path.exists(indeed_path):
        for subdir in os.listdir(indeed_path):
            subdir_path = os.path.join(indeed_path, subdir)
            if os.path.isdir(subdir_path):
                try:
                    date, country, role = subdir.split('_')
                except ValueError:
                    print(f"Subdirectorio {subdir} en indeed no sigue el formato esperado (date_country_role). Omitiendo.")
                    continue
                
                for file_name in os.listdir(subdir_path):
                    if file_name.endswith('.json'):
                        file_path = os.path.join(subdir_path, file_name)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                        except (FileNotFoundError, json.JSONDecodeError) as e:
                            print(f"Error con {file_path}: {e}")
                            continue
                        for job in data:
                            processed_job = process_source_indeed(job, date, country, role)
                            processed_data.append(processed_job)

    # Procesar Remotive
    remotive_path = os.path.join(directory, 'remotive')
    if os.path.exists(remotive_path):
        for file_name in os.listdir(remotive_path):
            if file_name.endswith('.json'):
                file_path = os.path.join(remotive_path, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error con {file_path}: {e}")
                    continue
                subdir_date = file_name.split('_')[0]
                for job in data.get("jobs", []):
                    processed_job = process_source_remotive(job, subdir_date)
                    processed_data.append(processed_job)

    # Procesar RemoteOK
    remoteok_path = os.path.join(directory, 'remoteok')
    if os.path.exists(remoteok_path):
        for file_name in os.listdir(remoteok_path):
            if file_name.endswith('.json'):
                file_path = os.path.join(remoteok_path, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error con {file_path}: {e}")
                    continue
                subdir_date = file_name.split('_')[0]
                for job in data:  # RemoteOK es una lista directa
                    processed_job = process_source_remoteok(job, subdir_date)
                    processed_data.append(processed_job)

    return processed_data

# Ejecución
data_directory = os.path.join(os.getcwd(), 'data')
processed_data = process_json_files(data_directory)

output_file_path = os.path.join('output_data', 'joined_data.json')
os.makedirs('output_data', exist_ok=True)
try:
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)
    print(f"Datos guardados en: {output_file_path}")
except Exception as e:
    print(f"Error al guardar el archivo: {e}")