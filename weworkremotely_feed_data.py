import requests
import os
from datetime import datetime
import xml.etree.ElementTree as ET
import json
import time
import random

def fetch_weworkremotely_jobs(url, category_name):
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
        namespaces = {'media': 'http://search.yahoo.com/mrss/'}
        
        for item in root.findall('.//item'):
            title = item.find('title').text if item.find('title') is not None else ""
            company = title.split(': ', 1)[0] if ': ' in title else "Empresa no especificada"
            job = {
                "title": title,
                "company": company,
                "region": item.find('region').text if item.find('region') is not None else "Ubicación no especificada",
                "category": item.find('category').text if item.find('category') is not None else "Rol no especificado",
                "type": item.find('type').text if item.find('type') is not None else "No especificado",
                "description": item.find('description').text if item.find('description') is not None else "",
                "pubDate": item.find('pubDate').text if item.find('pubDate') is not None else "",
                "link": item.find('link').text if item.find('link') is not None else "",
                "media_content": item.find('media:content', namespaces).get('url') if item.find('media:content', namespaces) is not None else ""
            }
            jobs.append(job)
        
        today = datetime.now().strftime("%Y-%m-%d")
        wwr_dir = os.path.join("data", "weworkremotely")
        os.makedirs(wwr_dir, exist_ok=True)
        file_name = f"{today}_weworkremotely_jobs_{category_name}.json"
        file_path = os.path.join(wwr_dir, file_name)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=4)
        
        print(f"Datos guardados en: {file_path}. Total de trabajos: {len(jobs)}")
        return jobs
    else:
        print(f"Error: {response.status_code} para {url}")
        return None

def get_weworkremotely_jobs():
    # Lista de feeds por categoría según la documentación
    feeds = [
        ("general", "https://weworkremotely.com/remote-jobs.rss"),
        ("remote_customer_support_jobs", "https://weworkremotely.com/categories/remote-customer-support-jobs.rss"),
        ("remote_product_jobs", "https://weworkremotely.com/categories/remote-product-jobs.rss"),
        ("remote_full_stack_programming_jobs", "https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss"),
        ("remote_back_end_programming_jobs", "https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss"),
        ("remote_front_end_programming_jobs", "https://weworkremotely.com/categories/remote-front-end-programming-jobs.rss"),
        ("remote_sales_and_marketing_jobs", "https://weworkremotely.com/categories/remote-sales-and-marketing-jobs.rss"),
        ("remote_management_and_finance_jobs", "https://weworkremotely.com/categories/remote-management-and-finance-jobs.rss"),
        ("remote_design_jobs", "https://weworkremotely.com/categories/remote-design-jobs.rss"),
        ("remote_devops_sysadmin_jobs", "https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss"),
        ("all_other_remote_jobs", "https://weworkremotely.com/categories/all-other-remote-jobs.rss")
    ]
    
    all_jobs = []
    for category_name, url in feeds:
        jobs = fetch_weworkremotely_jobs(url, category_name)
        if jobs:
            all_jobs.extend(jobs)
        # Sleep aleatorio entre 1 y 5 segundos
        sleep_time = random.uniform(1, 5)
        print(f"Esperando {sleep_time:.2f} segundos antes de la siguiente llamada...")
        time.sleep(sleep_time)
    
    return all_jobs

if __name__ == "__main__":
    jobs = get_weworkremotely_jobs()
    if jobs:
        print(f"Obtenidas {len(jobs)} ofertas de trabajo en total.")