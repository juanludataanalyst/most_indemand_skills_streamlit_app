import requests
import os
from datetime import datetime
import xml.etree.ElementTree as ET
import json

def get_remotive_jobs():
    url = "https://remotive.com/remote-jobs/feed"
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
        root = ET.fromstring(response.content)
        jobs = []
        
        for item in root.findall('.//item'):
            job = {
                "id": item.find('guid').text.split('-')[-1] if item.find('guid') is not None else generate_job_id(item.find('description').text or ""),
                "title": item.find('title').text if item.find('title') is not None else "",
                "company": item.find('company').text if item.find('company') is not None else "Empresa no especificada",
                "description": item.find('description').text if item.find('description') is not None else "",
                "pubDate": item.find('pubDate').text if item.find('pubDate') is not None else "",
                "link": item.find('link').text if item.find('link') is not None else "",
                "category": item.find('category').text if item.find('category') is not None else "Rol no especificado",
                "type": item.find('type').text if item.find('type') is not None else "No especificado",
                "location": item.find('location').text if item.find('location') is not None else "Ubicación no especificada"
            }
            jobs.append(job)
        
        today = datetime.now().strftime("%Y-%m-%d")
        remotive_dir = os.path.join("data", "remotive")
        os.makedirs(remotive_dir, exist_ok=True)
        file_path = os.path.join(remotive_dir, f"{today}_remotive_jobs.json")
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=4)
        
        print(f"Datos guardados en: {file_path}. Total de trabajos: {len(jobs)}")
        return jobs
    else:
        print(f"Error inesperado: {response.status_code}")
        return None

if __name__ == "__main__":
    jobs = get_remotive_jobs()
    if jobs:
        print(f"Obtenidas {len(jobs)} ofertas de trabajo.")