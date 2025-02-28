import json
from bs4 import BeautifulSoup

# Mapeo de roles a categorías genéricas
role_mapping = {
    # Remotive (base)
    "DevOps / Sysadmin": "DevOps Engineer",
    "Design": "Designer",
    "QA": "QA Engineer",
    "Data Analysis": "Data Science",
    "Project Management": "Product Manager",  # Unificado con Product Manager
    "Product": "Product Manager",  # Unificado con Project Manager
    "Customer Service": "Customer Support",
    "Human Resources": "HR Specialist",
    "Finance / Legal": "Finance",
    "Marketing": "Marketer",
    "Writing": "Writer",
    "Sales / Business": "Sales",
    "Software Development": "Software Developer",
    "All others": "Other",
    # RemoteOK
    "design": "Designer",
    "Search": "Marketer",
    "crypto": "Software Developer",
    "Technical": "Software Developer",
    "Senior": "Other",
    "sales": "Sales",
    "devops": "DevOps Engineer",
    "Crypto": "Software Developer",
    "Don't": "Other",
    "don't": "Other",
    "Audio": "Other",
    "Gaming": "Other",
    "Backend": "Software Developer",
    "Software": "Software Developer",
    "Pathologist": "Other",
    "Community": "Customer Support",
    "Engineering": "Other",
    "Radiologist": "Other",
    "Frontend": "Software Developer",
    "Content": "Marketer",
    "Referral": "Other",
    "Full": "Software Developer",
    "Servicing": "Customer Support",
    "Operations": "Other",
    "Want": "Other",
    "Care": "Customer Support",
    "Internet": "Other",
    "Rails": "Software Developer",
    "Media": "Marketer",
    "Junior": "Other",
    "Join": "Other",
    "Fully": "Other",
    "Director": "Other",
    "Digital": "Marketer",
    "Deputy": "Other",
    "Android": "Software Developer",
    "Norwegian": "Other",
    "Danish": "Other",
    "Coding": "Software Developer",
    "Power": "Other",
    "Tutor": "Customer Support",
    "Membership": "Customer Support",
    "Head": "Other",
    "IT": "Software Developer",
    "qa": "QA Engineer",
    # WeWorkRemotely
    "DevOps and Sysadmin": "DevOps Engineer",
    "Product": "Product Manager",  # Unificado con Project Manager
    "Design": "Designer",
    "All Other Remote": "Other",
    "Management and Finance": "Finance",  # Correcto como Finance
    "Front-End Programming": "Software Developer",
    "Sales and Marketing": "Sales",
    "Full-Stack Programming": "Software Developer",
    "Customer Support": "Customer Support",
    "Back-End Programming": "Software Developer",
    "Data Science": "Data Science",
    # Indeed (ajuste específico)
    "Software Engineer": "Software Developer"
}

def clean_html(html_text):
    if html_text:
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.get_text()
    return ""

def map_role(role, title=None, source=None):
    # Para Jobicy, intentar extraer del título si es "Desconocido"
    if source == "jobicy" and role == "Desconocido" and title:
        title_lower = title.lower()
        if "analyst" in title_lower or "data" in title_lower:
            return "Data Science"
        elif "engineer" in title_lower or "devops" in title_lower:
            return "DevOps Engineer"
        elif "developer" in title_lower or "software" in title_lower or "programmer" in title_lower:
            return "Software Developer"
        elif "design" in title_lower or "ux" in title_lower or "ui" in title_lower:
            return "Designer"
        elif "qa" in title_lower or "quality" in title_lower:
            return "QA Engineer"
        elif "manager" in title_lower or "project" in title_lower:
            return "Product Manager"
        elif "support" in title_lower or "customer" in title_lower:
            return "Customer Support"
        elif "marketing" in title_lower or "sales" in title_lower:
            return "Sales"
        elif "writer" in title_lower or "content" in title_lower:
            return "Writer"
        else:
            return "Other"
    # Para Indeed, mantener roles originales
    if source == "indeed":
        return role
    # Para otras fuentes, usar el mapeo
    return role_mapping.get(role, role)

# Leer el archivo joined_data.json
with open("output_data/joined_data.json", 'r', encoding="utf-8") as f:
    data = json.load(f)

# Mapear los roles
for job in data:
    job["role"] = map_role(job["role"], job.get("title"), job["source"])

# Guardar el resultado en un nuevo archivo
output_file_path = "output_data/joined_data_mapped.json"
with open(output_file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Datos con roles mapeados guardados en: {output_file_path}")