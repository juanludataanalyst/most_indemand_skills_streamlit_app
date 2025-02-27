import requests
import os
from datetime import datetime
import xml.etree.ElementTree as ET
import json

def get_weworkremotely_jobs():
    url = "https://weworkremotely.com/remote-jobs.rss"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        jobs = []
        namespaces = {'media': 'http://search.yahoo.com/mrss/'}
        
        for item in root.findall('.//item'):
            title = item.find('title').text if item.find('title') is not None else ""
            # Extraer compañía del título (antes de ":")
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
        file_path = os.path.join(wwr_dir, f"{today}_weworkremotely_jobs.json")
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=4)
        
        print(f"Datos guardados en: {file_path}")
        return jobs
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    jobs = get_weworkremotely_jobs()
    if jobs:
        print(f"Obtenidas {len(jobs)} ofertas de trabajo.")