import requests
import os
from datetime import datetime
import xml.etree.ElementTree as ET
import json
import time
import random
from bs4 import BeautifulSoup

def fetch_jobscollider_jobs(url, category_name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        print(f"Intentando RSS: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con {url}: {e}")
        return None

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        jobs = []
        namespaces = {'content': 'http://purl.org/rss/1.0/modules/content/'}
        
        for item in root.findall('.//item'):
            title = item.find('title').text if item.find('title') is not None else ""
            company = title.split(': ', 1)[0] if ': ' in title else "Empresa no especificada"
            description = item.find('description').text if item.find('description') is not None else ""
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
            link = item.find('link').text if item.find('link') is not None else ""
            guid = item.find('guid').text if item.find('guid') is not None else ""

            # Limpiar el HTML del campo description
            cleaned_description = clean_html(description)

            # Formatear la fecha
            try:
                date_obj = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
                formatted_date = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                formatted_date = datetime.now().strftime("%Y-%m-%d")

            job = {
                "title": title,
                "company": company,
                "region": "Ubicación no especificada",  # Campo no existente, se asigna un valor por defecto
                "category": category_name,  # Asignamos la categoría de la llamada a la API
                "type": "No especificado",  # Campo no existente, se asigna un valor por defecto
                "description": cleaned_description,
                "pubDate": formatted_date,
                "link": link,
                "guid": guid,
                "source": "jobscollider"
            }
            jobs.append(job)
        
        today = datetime.now().strftime("%Y-%m-%d")
        jc_dir = os.path.join("data", "jobscollider")
        os.makedirs(jc_dir, exist_ok=True)
        file_name = f"{today}_jobscollider_jobs_{category_name}.json"
        file_path = os.path.join(jc_dir, file_name)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=4, ensure_ascii=False)
        
        print(f"Datos guardados en: {file_path}. Total de trabajos: {len(jobs)}")
        return jobs
    else:
        print(f"Error: {response.status_code} para {url}")
        return None

def clean_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.get_text()

def get_jobscollider_jobs():
    # Lista de feeds por categoría según la documentación de JobsCollider
    feeds = [
        ("software_development", "https://jobscollider.com/remote-software-development-jobs.rss"),
        ("cybersecurity", "https://jobscollider.com/remote-cybersecurity-jobs.rss"),
        ("customer_service", "https://jobscollider.com/remote-customer-service-jobs.rss"),
        ("design", "https://jobscollider.com/remote-design-jobs.rss"),
        ("marketing", "https://jobscollider.com/remote-marketing-jobs.rss"),
        ("sales", "https://jobscollider.com/remote-sales-jobs.rss"),
        ("product", "https://jobscollider.com/remote-product-jobs.rss"),
        ("business", "https://jobscollider.com/remote-business-jobs.rss"),
        ("data", "https://jobscollider.com/remote-data-jobs.rss"),
        ("devops", "https://jobscollider.com/remote-devops-jobs.rss"),
        ("finance_legal", "https://jobscollider.com/remote-finance-legal-jobs.rss"),
        ("human_resources", "https://jobscollider.com/remote-human-resources-jobs.rss"),
        ("qa", "https://jobscollider.com/remote-qa-jobs.rss"),
        ("writing", "https://jobscollider.com/remote-writing-jobs.rss"),
        ("project_management", "https://jobscollider.com/remote-project-management-jobs.rss"),
        ("all_others", "https://jobscollider.com/remote-all-others-jobs.rss")
    ]
    
    all_jobs = []
    for category_name, url in feeds:
        jobs = fetch_jobscollider_jobs(url, category_name)
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