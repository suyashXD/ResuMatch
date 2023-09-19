import pickle
import csv
import unicodedata  # Import the unicodedata module

# Function to load similarity scores
def load_similarity_scores():
    with open("similarity_scores.pkl", "rb") as f:
        similarities = pickle.load(f)
    return similarities

# Function to sanitize text for CSV output
def sanitize_text(text):
    # Remove or replace non-encodable characters
    return "".join(char for char in text if unicodedata.category(char)[0] != 'C')

# Function to select top candidates for each job description
def select_top_candidates(similarities, num_top_candidates=5):
    top_candidates = {}
    for job_title, candidate_scores in similarities.items():
        sorted_candidates = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)
        top_candidates[job_title] = sorted_candidates[:num_top_candidates]
    return top_candidates

# Function to write the results to a CSV file
def write_results_to_csv(top_candidates, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Job Title", "Candidate", "Similarity Score"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for job_title, candidates in top_candidates.items():
            for candidate, score in candidates:
                sanitized_job_title = sanitize_text(job_title)
                sanitized_candidate = sanitize_text(candidate)
                writer.writerow({"Job Title": sanitized_job_title, "Candidate": sanitized_candidate, "Similarity Score": score})

if __name__ == "__main__":
    similarities = load_similarity_scores()
    
    # Select the top 5 candidates for each job description
    top_candidates = select_top_candidates(similarities)
    
    # Write the results to a CSV file
    output_file = "top_candidates.csv"
    write_results_to_csv(top_candidates, output_file)
    
    print(f"Results written to {output_file}")
