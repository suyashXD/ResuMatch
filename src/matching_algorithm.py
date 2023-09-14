import pickle

# Function to load similarity scores
def load_similarity_scores():
    with open("similarity_scores.pkl", "rb") as f:
        similarities = pickle.load(f)
    return similarities

# Function to select top candidates for each job description
def select_top_candidates(similarities, num_top_candidates=5):
    top_candidates = {}
    for job_title, candidate_scores in similarities.items():
        sorted_candidates = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)
        top_candidates[job_title] = sorted_candidates[:num_top_candidates]
    return top_candidates

if __name__ == "__main__":
    similarities = load_similarity_scores()
    
    # Select the top 5 candidates for each job description
    top_candidates = select_top_candidates(similarities)
    
    # Print or store the top candidates for further analysis or presentation
    for job_title, candidates in top_candidates.items():
        print(f"Job Title: {job_title}")
        for candidate, score in candidates:
            print(f"Candidate: {candidate}, Similarity Score: {score}")
