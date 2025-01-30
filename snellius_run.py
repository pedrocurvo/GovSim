import os 

# Run all the scripts in scripts subdirectory

for root, dirs, files in os.walk("scripts"):
    for file in files:
        if file.endswith(".sh"):
            os.system(f"sbatch {os.path.join(root, file)}")
            print(f"Submitted {file}")