import subprocess

# Execute the first code file
subprocess.run(["python", "pdf_extractor.py"])

# Execute the second code file
subprocess.run(["python", "text_preprocessing.py"])

# Execute the third code file
subprocess.run(["python", "similarity_calculator.py"])

# Execute the fourth code file
subprocess.run(["python", "matching_algorithm.py"])

# You can add error handling or additional logic here if needed
