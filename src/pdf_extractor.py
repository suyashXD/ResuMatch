from fastapi import concurrency
import pandas as pd
import os
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Function to format the resume content
def format_resume_content(html_content):
    formatted_resume = []
    
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract candidate ID
    candidate_id_span = soup.find('span', class_='field fName')
    if candidate_id_span:
        candidate_id = candidate_id_span.find_next('span', class_='field')
        if candidate_id:
            candidate_id = candidate_id.text.strip()
            formatted_resume.append(f"Candidate ID: {candidate_id}\n")
    
    # Extract sections
    sections = soup.find_all('div', class_='section')
    
    for section in sections:
        # Extract section title
        section_title = section.find('div', class_='sectiontitle')
        if section_title:
            section_title_text = section_title.text.strip()
            formatted_resume.append(f"{section_title_text}\n{'-' * len(section_title_text)}")
        
        # Extract section content
        section_content = section.find_all('p', align='LEFT')
        if section_content:
            for content in section_content:
                content_text = content.text.strip()
                formatted_resume.append(content_text)
    
    return '\n'.join(formatted_resume)

# Function to process a single row of the DataFrame
def process_resume(row):
    candidate_id = row['ID']
    resume_html = row['Resume_html']

    # Format the resume content from HTML
    formatted_resume_text = format_resume_content(resume_html)

    return candidate_id, formatted_resume_text

# Get the absolute path of the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate up two levels to reach the project root directory
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))

# Construct the full path to the CSV file
csv_file_path = os.path.join(project_root, 'resumatch', 'data', 'kaggle_resume_dataset', 'Resume.csv')

# Load the CSV file
df = pd.read_csv(csv_file_path)

# Create a directory to store candidate details if it doesn't exist
output_dir = os.path.join(project_root, 'resumatch', 'candidate_details')
os.makedirs(output_dir, exist_ok=True)

# Process resumes in parallel using ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust max_workers as needed
    future_to_candidate = {executor.submit(process_resume, row): row for _, row in df.iterrows()}
    
    for future in concurrency.futures.as_completed(future_to_candidate):
        candidate_id, formatted_resume_text = future.result()
        output_file_path = os.path.join(output_dir, f'candidate_{candidate_id}.txt')
        
        # Write the formatted resume details to the file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(formatted_resume_text)
        
        print(f"Details saved for Candidate ID: {candidate_id} in {output_file_path}")
