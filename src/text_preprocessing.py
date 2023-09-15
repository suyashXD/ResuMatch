import os
import pandas as pd
from transformers import DistilBertTokenizer
import torch
from concurrent.futures import ProcessPoolExecutor  # Import for parallel processing
from functools import lru_cache  # Import for caching

# Set the paths to your data directories
candidate_details_dir = "candidate_details"
job_descriptions_csv = "data\\hugging_face_job_descriptions\\training_data.csv"
output_dir = "preprocessed_data"

# Initialize DistilBERT tokenizer
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Function to preprocess and tokenize text
@lru_cache(maxsize=None)  # Cache tokenization results
def preprocess_and_tokenize(text):
    # Tokenize the text
    tokens = tokenizer.tokenize(text)
    # Convert tokens to IDs
    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    return input_ids

# Function to process a single text file
def process_candidate_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    # Preprocess and tokenize the text
    input_ids = preprocess_and_tokenize(text)
    return input_ids

# Load job descriptions from CSV
job_descriptions_df = pd.read_csv(job_descriptions_csv)

# Define a function for parallel processing
def process_candidate_parallel(file_name):
    if file_name.endswith(".txt"):
        candidate_file_path = os.path.join(candidate_details_dir, file_name)
        # Process the candidate file
        input_ids = process_candidate_file(candidate_file_path)
        
        # Save the preprocessed data to the output directory
        output_file_path = os.path.join(output_dir, f"{file_name.replace('.txt', '.pt')}")
        torch.save(input_ids, output_file_path)

# Initialize a ProcessPoolExecutor for parallel processing
with ProcessPoolExecutor() as executor:
    # Use parallel processing to process multiple candidate files concurrently
    executor.map(process_candidate_parallel, os.listdir(candidate_details_dir))

print("Text preprocessing and tokenization complete.")
