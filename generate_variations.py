from scripts.common.parsing import parse_foam_file, parse_variations
import os
import pathlib
import shutil
import argparse


parser = argparse.ArgumentParser(description="Generate variations for OpenFOAM cases")
parser.add_argument("--variations", type=str, default="default.variations", help="Path to the variations file")
args = parser.parse_args()

variations_file_path = args.variations

# Parse variations file
parsed_variations = parse_variations(variations_file_path)
n_variations = len(parsed_variations)

# Extract the filename without extension from the path
variations_file_name = pathlib.Path(variations_file_path).stem + "Variations"
# Count folders starting with a number
folder_count = 0
for item in os.listdir():
    if os.path.isdir(item) and item[0].isdigit():
        folder_count += 1

# Add the folder count to the variations file name
variations_file_name = str(folder_count) + "_" + variations_file_name

# Create variations folder
if not os.path.exists(variations_file_name):
    os.makedirs(variations_file_name)

# For each variation, create a folder and copy the files
basic_case_path = "basicCase"
for i in range(n_variations):
    # Create folder for variation
    variation_folder_name = os.path.join(variations_file_name, str(list(parsed_variations[i].values())[0]) + "_" + str(list(parsed_variations[i].keys())[0]))
    if not os.path.exists(variation_folder_name):
        os.makedirs(variation_folder_name)

    # Copy basicCase to variation folder
    for item in os.listdir(basic_case_path):
        s = os.path.join(basic_case_path, item)
        d = os.path.join(variation_folder_name, item)
        try:
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)
        except OSError as e:
            print(f"Error copying {s} to {d}: {e}")


    # Modify default.parameters file
    parameters_file_path = os.path.join(variation_folder_name, "default.parameters")
    
    # Read the file content
    with open(parameters_file_path, 'r') as file:
        file_content = file.readlines()

        # Modify the content based on parsed_variations[i]
        for key, value in parsed_variations[i].items():
            for line_num, line in enumerate(file_content):
                if key in line and not line.strip().startswith('//'):
                    # Replace the line with the new value
                    file_content[line_num] = f"{key} {value};\n"
                    break  # Stop searching for the key after replacing it once

        # Write the modified content back to the file
        with open(parameters_file_path, 'w') as file:
            file.writelines(file_content)


# Copy runAllCases.sh
run_all_cases_source_path = "runAllCases.sh"
run_all_cases_destination_path = os.path.join(variations_file_name, "runAllCases.sh")

try:
    shutil.copy2(run_all_cases_source_path, run_all_cases_destination_path)
except OSError as e:
    print(f"Error copying runAllCases.sh to {run_all_cases_destination_path}: {e}")

# Copy scripts/common/variations to variations_file_name directory
variations_scripts_source_path = "scripts/common/variations"
variations_scripts_target_path = os.path.join(variations_file_name, "variations")

# Check if source directory exists
if os.path.exists(variations_scripts_source_path):
    # Create target directory if it doesn't exist
    if not os.path.exists(variations_scripts_target_path):
        os.makedirs(variations_scripts_target_path)
    
    # Copy all Python files from source to target
    for item in os.listdir(variations_scripts_source_path):
        if item.endswith('.py'):
            s = os.path.join(variations_scripts_source_path, item)
            d = os.path.join(variations_scripts_target_path, item)
            try:
                shutil.copy2(s, d)
            except OSError as e:
                print(f"Error copying {s} to {d}: {e}")
else:
    print(f"Warning: Source directory {variations_scripts_source_path} not found.")
