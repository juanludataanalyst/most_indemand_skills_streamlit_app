import requests
import os
from datetime import datetime
import xml.etree.ElementTree as ET
import json

def get_jobicy_jobs():
    url = "https://jobicy.com/feed/newjobs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        print(f"Intentando RSS: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP: {e}")
        print(f"Respuesta del servidor: {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return None
    
    if response.status_code == 200:
        print("Contenido crudo del RSS (primeros 1000 caracteres):")
        print(response.text[:1000])
        
        try:
            root = ET.fromstring(response.content)
            jobs = []
            
            for job_elem in root.findall('.//job'):
                job = {
                    "name": job_elem.find('name').text if job_elem.find('name') is not None else "",
                    "company": job_elem.find('company').text if job_elem.find('company') is not None else "Empresa no especificada",
                    "description": job_elem.find('description').text if job_elem.find('description') is not None else "",
                    "pubdate": job_elem.find('pubdate').text if job_elem.find('pubdate') is not None else "",
                    "link": job_elem.find('link').text if job_elem.find('link') is not None else "",
                    "region": job_elem.find('region').text if job_elem.find('region') is not None else "Ubicación no especificada",
                    "jobtype": job_elem.find('jobtype').text if job_elem.find('jobtype') is not None else "No especificado",
                }
                jobs.append(job)
            
            print(f"Número de trabajos encontrados: {len(jobs)}")
            
            today = datetime.now().strftime("%Y-%m-%d")
            jobicy_dir = os.path.join("data", "jobicy")
            os.makedirs(jobicy_dir, exist_ok=True)
            file_path = os.path.join(jobicy_dir, f"{today}_jobicy_jobs.json")
            
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(jobs, f, indent=4)
            
            print(f"Datos guardados en: {file_path}")
            return jobs
        except ET.ParseError as e:
            print(f"Error al parsear XML: {e}")
            print("Contenido recibido:")
            print(response.text)
            return None
    else:
        print(f"Error inesperado: {response.status_code}")
        return None

if __name__ == "__main__":
    jobs = get_jobicy_jobs()
    if jobs:
        print(f"Obtenidas {len(jobs)} ofertas de trabajo.")
    else:
        print("No se obtuvieron trabajos.")