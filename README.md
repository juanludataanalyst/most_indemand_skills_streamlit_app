# Most In-Demand Skills Streamlit App
![imagen](https://github.com/user-attachments/assets/9ae51bd3-a912-4262-b765-24cef23d4a08)

## Overview

📋 This Streamlit-based web application identifies and analyzes the most in-demand skills for various job roles across different countries, extracted from job descriptions scraped using two companion repositories:

- **[Indeed Data Scraper (Requests-based)](https://github.com/juanludataanalyst/indeed_data_scraper_request)**
- **[Indeed Data Scraper (Selenium-based)](https://github.com/juanludataanalyst/indeed_data_scraper_selenium)**

The application processes job data to recommend skills that users should learn to enhance their career opportunities.



## ⭐ Key Features

### 📊 Data Extraction (`extract_skills.py`)

- **Input**: Job data stored in the `data` directory, organized by date, country, and role (e.g., `2024-11-01_Spain_Data Scientist`). Each subdirectory contains JSON files with job descriptions, including fields such as job title, company, description, salary, and company type.
- **Output**: Generates a `skills_data_table.csv` file summarizing job IDs, skills, countries, roles, and job titles.

### 🔗 Association Rules (`create_association_rules.py`)

- Implements the Apriori algorithm to generate association rules for skills within specific roles.
- **Purpose**: Helps determine how skills are related, enabling the app to recommend which skills users should prioritize learning.

### 🌟 Streamlit Application

- **Skills by Role**: Displays the percentage of job postings that mention each skill, segmented by role and country.
- **Skill to learn**: Suggests skills to learn based on association rules and user preferences.
- **Raw Data Viewer**: Provides access to view the extracted and processed data directly.

## 🚀 Installation and Usage

1. Clone this repository:

    ```bash
    git clone https://github.com/juanludataanalyst/most_indemand_skills_streamlit_app.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    streamlit run app.py
    ```

## 📂 Data Sources

- Job data is sourced from the two scraping repositories, each focusing on different methodologies (Requests and Selenium).
- Skills data is processed from job descriptions stored in structured JSON files.

## 🔮 Future Work

- Integrate more robust data visualizations.
- Expand association rules to include advanced metrics.
- Support for additional languages and regions.
