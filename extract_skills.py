import json
import re
import os
import hashlib
from bs4 import BeautifulSoup
from datetime import datetime

# Cargar diccionario de tecnologías
with open('data/skills_definition.json', 'r') as f:
    skills = json.load(f)

patterns = {key: re.compile(r'\b(' + '|'.join(map(re.escape, variations)) + r')\b', re.IGNORECASE) 
            for key, variations in skills.items()}

# Funciones comunes
def generate_job_id(description):
    return hashlib.md5(description.encode('utf-8')).hexdigest()

def clean_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.get_text()

def extract_technologies(description):
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
        "role": role,
        "source": "indeed"
    }

def process_source_remotive_historic(job, subdir_date):
    title = job.get("title", "")
    company = job.get("company_name", "Empresa no especificada")
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
        "role": role,
        "source": "remotive"
    }

def process_source_remotive(job, subdir_date):
    title = job.get("title", "")
    company = job.get("company", "Empresa no especificada")
    description = job.get("description", "")
    salary = "No especificado"
    employment_type = job.get("type", "No especificado").replace("_", " ").title()
    technologies = extract_technologies(description)
    job_id = job.get("id", generate_job_id(description))
    location = job.get("location", "Ubicación no especificada")
    role = job.get("category", "Desconocido")
    date = job.get("pubDate", subdir_date)
    try:
        date_obj = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
        date = date_obj.strftime("%Y-%m-%d")
    except ValueError:
        date = subdir_date
    country = location if any(c in location.lower() for c in ["colombia", "india", "us"]) else location

    return {
        "job_id": str(job_id),
        "title": title,
        "company": company,
        "location": location,
        "skills": technologies,
        "tags": [],
        "salary": salary,
        "employment_type": employment_type,
        "date": date,
        "country": country,
        "role": role,
        "source": "remotive"
    }

def process_source_remoteok(job, subdir_date):
    title = job.get("position", "")
    company = job.get("company", "")
    description = job.get("description", "")
    salary = f"${job.get('salary_min', 'No especificado')}-{job.get('salary_max', 'No especificado')}" if job.get('salary_min') else "No especificado"
    employment_type = "No especificado"
    tags = job.get("tags", [])
    technologies = extract_technologies(description)
    job_id = generate_job_id(description)
    location = job.get("location", "Ubicación no especificada")
    role = next((tag for tag in tags if tag in ["design", "sales", "qa", "devops", "crypto"]), title.split()[0])
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
        "role": role,
        "source": "remoteok"
    }

def process_source_weworkremotely(job, subdir_date):
    title_full = job.get("title", "")
    if ': ' in title_full:
        company, title = title_full.split(': ', 1)
    else:
        company = "Empresa no especificada"
        title = title_full
    description = job.get("description", "")
    salary = "No especificado"
    employment_type = job.get("type", "No especificado")
    technologies = extract_technologies(description)
    job_id = generate_job_id(description)
    location = job.get("region", "Ubicación no especificada")
    role = job.get("category", "Rol no especificado")
    date = job.get("pubDate", subdir_date)
    try:
        date_obj = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
        date = date_obj.strftime("%Y-%m-%d")
    except ValueError:
        date = subdir_date
    country = location if any(c in location.lower() for c in ["colombia", "india", "us"]) else location

    return {
        "job_id": job_id,
        "title": title,
        "company": company,
        "location": location,
        "skills": technologies,
        "tags": [],
        "salary": salary,
        "employment_type": employment_type,
        "date": date,
        "country": country,
        "role": role,
        "source": "weworkremotely"
    }

def process_source_jobicy(job, subdir_date, category_from_file=None):
    title = job.get("jobTitle", "").replace("Remote ", "", 1) if job.get("jobTitle", "").startswith("Remote ") else job.get("jobTitle", "")
    company = job.get("companyName", "Empresa no especificada")
    description = job.get("jobDescription", "")
    salary = "No especificado"
    if job.get("annualSalaryMin") and job.get("annualSalaryMax") and job.get("salaryCurrency"):
        salary = f"{job['salaryCurrency']} {job['annualSalaryMin']} - {job['annualSalaryMax']}"
    employment_type = job.get("jobType", ["No especificado"])[0].replace("-", " ").title()
    technologies = extract_technologies(description)
    job_id = str(job.get("id", generate_job_id(description)))
    location = job.get("jobGeo", "Ubicación no especificada")
    role = category_from_file if category_from_file else "Desconocido"  # Usar categoría del archivo
    date = job.get("pubDate", subdir_date)
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        date = date_obj.strftime("%Y-%m-%d")
    except ValueError:
        date = subdir_date
    country = location if any(c in location.lower() for c in ["colombia", "india", "us"]) else location

    return {
        "job_id": job_id,
        "title": title,
        "company": company,
        "location": location,
        "skills": technologies,
        "tags": [],
        "salary": salary,
        "employment_type": employment_type,
        "date": date,
        "country": country,
        "role": role,
        "source": "jobicy"
    }

def process_source_jobscollider(job, subdir_date):
    title = job.get("title", "")
    company = job.get("company", "Empresa no especificada")
    description = job.get("description", "")
    salary = "No especificado"
    employment_type = job.get("type", "No especificado").replace("_", " ").title()
    technologies = extract_technologies(description)
    job_id = generate_job_id(description)
    location = job.get("region", "Ubicación no especificada")
    role = job.get("category", "Rol no especificado")
    pub_date = job.get("pubDate", subdir_date)  # Usamos el valor directamente

    # Si pubDate no está en el formato esperado, usar la fecha del directorio
    if not isinstance(pub_date, str) or len(pub_date) != 10 or pub_date[4] != '-' or pub_date[7] != '-':
        print(f"Formato de fecha inválido: {pub_date}. Usando fecha del directorio: {subdir_date}")
        pub_date = subdir_date

    country = location if any(c in location.lower() for c in ["colombia", "india", "us"]) else location

    return {
        "job_id": job_id,
        "title": title,
        "company": company,
        "location": location,
        "skills": technologies,
        "tags": [],
        "salary": salary,
        "employment_type": employment_type,
        "date": pub_date,  # Usamos pub_date directamente
        "country": country,
        "role": role,
        "source": "jobscollider"
    }

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

    # Procesar Remotive histórico (API)
    remotive_historic_path = os.path.join(directory, 'remotive_historic')
    if os.path.exists(remotive_historic_path):
        for file_name in os.listdir(remotive_historic_path):
            if file_name.endswith('.json'):
                file_path = os.path.join(remotive_historic_path, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error con {file_path}: {e}")
                    continue
                subdir_date = file_name.split('_')[0]
                if isinstance(data, dict) and "jobs" in data:
                    for job in data["jobs"]:
                        processed_job = process_source_remotive_historic(job, subdir_date)
                        processed_data.append(processed_job)
                else:
                    print(f"Formato inesperado en {file_path}. Omitiendo archivo histórico.")

    # Procesar Remotive feed (RSS)
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
                for job in data:
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
                for job in data:
                    processed_job = process_source_remoteok(job, subdir_date)
                    processed_data.append(processed_job)

    # Procesar We Work Remotely
    wwr_path = os.path.join(directory, 'weworkremotely')
    if os.path.exists(wwr_path):
        for file_name in os.listdir(wwr_path):
            if file_name.endswith('.json'):
                file_path = os.path.join(wwr_path, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error con {file_path}: {e}")
                    continue
                subdir_date = file_name.split('_')[0]
                for job in data:
                    processed_job = process_source_weworkremotely(job, subdir_date)
                    processed_data.append(processed_job)

    # Procesar Jobicy (actualizado para API con categorías desde el nombre del archivo)
    jobicy_path = os.path.join(directory, 'jobicy')
    if os.path.exists(jobicy_path):
        for file_name in os.listdir(jobicy_path):
            if file_name.endswith('.json'):
                file_path = os.path.join(jobicy_path, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error con {file_path}: {e}")
                    continue
                subdir_date = file_name.split('_')[0]
                # Extraer la categoría del nombre del archivo (ej. "remote_data_science_and_analytics_jobs")
                category_part = file_name.split('jobicy_jobs_')[1].replace('.json', '')
                job_list = data.get("jobs", [])
                for job in job_list:
                    processed_job = process_source_jobicy(job, subdir_date, category_part)
                    processed_data.append(processed_job)

    # Procesar JobsCollider
    jobscollider_path = os.path.join(directory, 'jobscollider')
    if os.path.exists(jobscollider_path):
        for file_name in os.listdir(jobscollider_path):
            if file_name.endswith('.json'):
                file_path = os.path.join(jobscollider_path, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error con {file_path}: {e}")
                    continue
                subdir_date = file_name.split('_')[0]
                for job in data:
                    processed_job = process_source_jobscollider(job, subdir_date)
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