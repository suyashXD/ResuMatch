import subprocess
import os

# Function to run a script and suppress warnings
def run_script(script_name):
    try:
        # Set the PYTHONWARNINGS environment variable to ignore specific warning categories
        os.environ["PYTHONWARNINGS"] = "ignore:ResourceWarning"

        subprocess.run(["python", script_name], check=True)  # Use check=True to raise an exception on error
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
    except Exception as e:
        print(f"An error occurred while running {script_name}: {e}")
    finally:
        # Reset the PYTHONWARNINGS environment variable to its original value
        os.environ["PYTHONWARNINGS"] = ""

# Execute the first code file
run_script("src\\pdf_extractor.py")

# Execute the second code file
run_script("src\\text_preprocessing.py")

# Execute the third code file
run_script("src\\similarity_calculator.py")

# Execute the fourth code file
run_script("src\\matching_algorithm.py")

# You can add error handling or additional logic here if needed
