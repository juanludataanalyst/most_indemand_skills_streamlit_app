import requests
import pandas as pd

def get_remotive_jobs():
    url = "https://remotive.io/api/remote-jobs"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Guardar JSON original
        with open("data_remotive/remotive_jobs.json", "w", encoding="utf-8") as f:
            import json
            json.dump(data, f, indent=4)
        
        
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    df_jobs = get_remotive_jobs()

