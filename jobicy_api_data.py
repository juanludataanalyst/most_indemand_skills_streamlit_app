import requests
import os
from datetime import datetime
import json
import time
import random

def fetch_jobicy_jobs(category_name, category_slug):
    base_url = "https://jobicy.com/api/v2/remote-jobs"
    params = {
        "count": 50,  # Máximo por llamada según documentación
        "industry": category_slug
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
    jobicy_dir = os.path.join("data", "jobicy")
    os.makedirs(jobicy_dir, exist_ok=True)
    file_name = f"{today}_jobicy_jobs_{category_name.replace(' ', '_').replace('&', 'and').lower()}.json"
    file_path = os.path.join(jobicy_dir, file_name)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=4)
    
    print(f"Datos guardados en: {file_path}. Total de trabajos: {len(jobs)}")
    return jobs

def get_jobicy_jobs():
    # Lista de categorías oficiales con slugs según tu JSON
    categories = [
        ("remote_business_development_jobs", "business"),
        ("remote_content_and_editorial_jobs", "copywriting"),  # Cambiado de copywriting para reflejar nombre oficial
        ("remote_creative_and_design_jobs", "design-multimedia"),
        ("remote_customer_success_jobs", "supporting"),
        ("remote_data_science_and_analytics_jobs", "data-science"),
        ("remote_devops_and_infrastructure_jobs", "admin"),  # Corregido de devops-sysadmin
        ("remote_finance_and_accounting_jobs", "accounting-finance"),
        ("remote_hr_and_recruiting_jobs", "hr"),
        ("remote_legal_and_compliance_jobs", "legal"),  # Añadido
        ("remote_marketing_and_sales_jobs", "marketing"),
        ("remote_product_and_operations_jobs", "management"),
        ("remote_programming_jobs", "dev"),
        ("remote_sales_jobs", "seller"),
        ("remote_seo_jobs", "seo"),
        ("remote_social_media_marketing_jobs", "smm"),
        ("remote_software_engineering_jobs", "engineering"),
        ("remote_technical_support_jobs", "technical-support"),
        ("remote_web_and_app_design_jobs", "web-app-design")  # Cubre UI/UX implícitamente
    ]
    
    all_jobs = []
    for category_name, category_slug in categories:
        jobs = fetch_jobicy_jobs(category_name, category_slug)
        if jobs:
            all_jobs.extend(jobs)
        # Sleep aleatorio entre 1 y 5 segundos
        sleep_time = random.uniform(1, 5)
        print(f"Esperando {sleep_time:.2f} segundos antes de la siguiente llamada...")
        time.sleep(sleep_time)
    
    return all_jobs

if __name__ == "__main__":
    jobs = get_jobicy_jobs()
    if jobs:
        print(f"Obtenidas {len(jobs)} ofertas de trabajo en total.")