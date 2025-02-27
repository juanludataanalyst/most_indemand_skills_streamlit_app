import requests
import os
from datetime import datetime

def get_remoteok_jobs():
    url = "https://remoteok.com/api"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        # La API devuelve una lista, el primer elemento es metadata
        if isinstance(data, list) and len(data) > 1:
            jobs = data[1:]  # Excluir el primer elemento (legal info)
        else:
            print("Formato inesperado de la API.")
            return None
        
        # Crear directorio y archivo con fecha actual
        today = datetime.now().strftime("%Y-%m-%d")  # Ej. "2025-02-26"
        remoteok_dir = os.path.join("data", "remoteok")
        os.makedirs(remoteok_dir, exist_ok=True)
        file_path = os.path.join(remoteok_dir, f"{today}_remoteok_jobs.json")
        
        # Guardar JSON original (solo los jobs)
        with open(file_path, "w", encoding="utf-8") as f:
            import json
            json.dump(jobs, f, indent=4)
        
        print(f"Datos guardados en: {file_path}")
        return jobs
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    jobs = get_remoteok_jobs()
    if jobs:
        print(f"Obtenidas {len(jobs)} ofertas de trabajo.")