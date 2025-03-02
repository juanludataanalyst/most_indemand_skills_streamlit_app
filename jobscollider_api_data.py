import requests
import os
from datetime import datetime
import json
import time
import random

def fetch_jobscollider_jobs(category_name, category_slug):
    base_url = "https://jobscollider.com/api/search-jobs"
    params = {
        "category": category_slug,
        "limit": 1000  # Máximo por llamada según la documentación
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        print(f"Intentando API para categoría '{category_name}' con slug '{category_slug}': {base_url}")
        response = requests.get(base_url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        jobs = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener {category_name}: {e}")
        return None
    
    today = datetime.now().strftime("%Y-%m-%d")
    jobscollider_dir = os.path.join("data", "jobscollider")
    os.makedirs(jobscollider_dir, exist_ok=True)
    file_name = f"{today}_jobscollider_jobs_{category_name.replace(' ', '_').replace('&', 'and').lower()}.json"
    file_path = os.path.join(jobscollider_dir, file_name)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=4)
    
    print(f"Datos guardados en: {file_path}. Total de trabajos: {len(jobs)}")
    return jobs

def get_jobscollider_jobs():
    categories = [
        ("software_development_jobs", "software-development"),
        ("cybersecurity_jobs", "cybersecurity"),
        ("customer_service_jobs", "customer-service"),
        ("design_jobs", "design"),
        ("marketing_jobs", "marketing"),
        ("sales_jobs", "sales"),
        ("product_jobs", "product"),
        ("business_jobs", "business"),
        ("data_jobs", "data"),
        ("devops_jobs", "devops"),
        ("finance_and_legal_jobs", "finance-legal"),
        ("human_resources_jobs", "human-resources"),
        ("qa_jobs", "qa"),
        ("writing_jobs", "writing"),
        ("project_management_jobs", "project-management"),
        ("all_other_jobs", "all-others")
    ]
    
    all_jobs = []
    for category_name, category_slug in categories:
        jobs = fetch_jobscollider_jobs(category_name, category_slug)
        if jobs:
            all_jobs.extend(jobs)
        # Sleep aleatorio entre 1 y 5 segundos
        sleep_time = random.uniform(1, 5)
        print(f"Esperando {sleep_time:.2f} segundos antes de la siguiente llamada...")
        time.sleep(sleep_time)
    
    return all_jobs

if __name__ == "__main__":
    jobs = get_jobscollider_jobs()
    if jobs:
        print(f"Obtenidas {len(jobs)} ofertas de trabajo en total.")
