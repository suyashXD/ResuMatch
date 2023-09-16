import subprocess

# Execute the first code file
subprocess.run(["python", "src\\pdf_extractor.py"])

# Execute the second code file
subprocess.run(["python", "src\\text_preprocessing.py"])

# Execute the third code file
subprocess.run(["python", "src\\similarity_calculator.py"])

# Execute the fourth code file
subprocess.run(["python", "src\\matching_algorithm.py"])

# You can add error handling or additional logic here if needed
