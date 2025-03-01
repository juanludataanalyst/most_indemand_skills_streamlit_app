import json
from bs4 import BeautifulSoup

# Mapeo de roles a categorías genéricas
role_mapping = {
    # Remotive (base)
    "DevOps / Sysadmin": "DevOps Engineer",
    "Design": "Designer",
    "QA": "QA Engineer",
    "Data Analysis": "Data Science",
    "Project Management": "Product Manager",
    "Product": "Product Manager",
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
    "Product": "Product Manager",
    "Design": "Designer",
    "All Other Remote": "Other",
    "Management and Finance": "Finance",
    "Front-End Programming": "Software Developer",
    "Sales and Marketing": "Sales",
    "Full-Stack Programming": "Software Developer",
    "Customer Support": "Customer Support",
    "Back-End Programming": "Software Developer",
    "Data Science": "Data Science",
    # Indeed (ajuste específico)
    "Software Engineer": "Software Developer",
    # Jobicy (mapeo de categorías de la API)
    "remote_business_development_jobs": "Sales",
    "remote_content_and_editorial_jobs": "Writer",
    "remote_creative_and_design_jobs": "Designer",
    "remote_customer_success_jobs": "Customer Support",
    "remote_data_science_and_analytics_jobs": "Data Science",
    "remote_devops_and_infrastructure_jobs": "DevOps Engineer",
    "remote_finance_and_accounting_jobs": "Finance",
    "remote_hr_and_recruiting_jobs": "HR Specialist",
    "remote_marketing_and_sales_jobs": "Marketer",
    "remote_product_and_operations_jobs": "Product Manager",
    "remote_programming_jobs": "Software Developer",
    "remote_sales_jobs": "Sales",
    "remote_seo_jobs": "Marketer",
    "remote_social_media_marketing_jobs": "Marketer",
    "remote_software_engineering_jobs": "Software Developer",
    "remote_technical_support_jobs": "Customer Support",
    "remote_web_and_app_design_jobs": "Designer"
}

def clean_html(html_text):
    if html_text:
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.get_text()
    return ""

def map_role(role, title=None, source=None):
    # Para Indeed, mantener roles originales
    if source == "indeed":
        return role
    # Para otras fuentes, usar el mapeo
    return role_mapping.get(role, role)

# Leer el archivo joined_data.json
with open("output_data/joined_data.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

# Mapear los roles
for job in data:
    job['role'] = map_role(job['role'], job.get('title'), job['source'])

# Guardar el resultado en un nuevo archivo
output_file_path = "output_data/joined_data_mapped.json"
with open(output_file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"Datos con roles mapeados guardados en: {output_file_path}")