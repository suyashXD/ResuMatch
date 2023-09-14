import os
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import torch
from transformers import DistilBertTokenizer, DistilBertModel
from concurrent.futures import ProcessPoolExecutor  # Import for parallel processing

# Load DistilBERT tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
model = DistilBertModel.from_pretrained("distilbert-base-uncased")

# Function to preprocess and tokenize text
def preprocess_and_tokenize(text):
    # Tokenize the text
    tokens = tokenizer.encode(text, add_special_tokens=True, truncation=True)
    return tokens

# Function to calculate cosine similarity between embeddings
def calculate_similarity(embedding1, embedding2):
    embedding1 = embedding1.reshape(1, -1)  # Reshape to a 2D array
    embedding2 = embedding2.reshape(1, -1)  # Reshape to a 2D array
    
    return cosine_similarity(embedding1, embedding2)[0][0]

# Load preprocessed candidate and job description data
def load_processed_data():
    candidate_files = os.listdir("preprocessed_data")  # Adjust this path
    candidate_data = {}

    for file in candidate_files:
        with open(os.path.join("preprocessed_data", file), "r", encoding='utf-8', errors='ignore') as f:
            candidate_data[file] = f.read()

    try:
        with open("data//hugging_face_job_descriptions//training_data.csv", "r", encoding='utf-8') as f:  # Adjust this path
            job_descriptions = pd.read_csv(f)
    except UnicodeDecodeError:
        # Handle encoding errors here or skip problematic rows
        pass

    return candidate_data, job_descriptions

# Function to calculate similarity for a batch of candidates
def calculate_similarity_batch(description_embedding, candidate_embeddings_batch):
    similarities = []
    for candidate_embedding in candidate_embeddings_batch:
        similarity = calculate_similarity(description_embedding, candidate_embedding)
        similarities.append(similarity)
    return similarities

if __name__ == "__main__":
    candidate_data, job_descriptions = load_processed_data()
    
    # Process and tokenize job descriptions
    job_descriptions["tokens"] = job_descriptions["job_description"].apply(preprocess_and_tokenize)
    
    # Tokenize and embed candidate details
    candidate_embeddings = {}
    for candidate_file, candidate_text in candidate_data.items():
        tokens = preprocess_and_tokenize(candidate_text)
        with torch.no_grad():
            embedding = model(torch.tensor([tokens]))[0][:, 0, :].numpy()
        candidate_embeddings[candidate_file] = embedding

    # Initialize a ProcessPoolExecutor for parallel processing
    with ProcessPoolExecutor() as executor:
        similarities = {}  # Dictionary to store similarity scores

        for index, row in job_descriptions.iterrows():
            description_embedding = model(torch.tensor([row["tokens"]]))[0][:, 0, :].detach().numpy()
            job_title = row["position_title"]
            similarities[job_title] = {}

            # Split candidates into batches for parallel processing
            candidate_files = list(candidate_embeddings.keys())
            batch_size = 200  # Adjust batch size as needed
            for i in range(0, len(candidate_files), batch_size):
                candidate_batch = candidate_files[i:i + batch_size]
                candidate_embeddings_batch = [candidate_embeddings[file] for file in candidate_batch]

                # Calculate similarity for the batch in parallel
                batch_similarities = executor.submit(calculate_similarity_batch, description_embedding, candidate_embeddings_batch)
                batch_similarities = batch_similarities.result()

                # Store batch results in the similarities dictionary
                for j, candidate_file in enumerate(candidate_batch):
                    similarities[job_title][candidate_file] = batch_similarities[j]

    # Store similarity scores for later use
    with open("similarity_scores.pkl", "wb") as f:
        pickle.dump(similarities, f)
