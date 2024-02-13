import os
import shutil

deployed_app_location = input("Enter the deployed application path: ")
temporary_extraction_path = os.path.join(deployed_app_location, f"TempExtraction")
zip_file = os.path.join(deployed_app_location, 'build.zip')

exclude_files = [
    'Fusioncharts-suite-xt',
    'GSNetImages',
    'Images',
    'PDFS',
    'TreeLineImages',
    'Wall.jpg',
    'web.config'
]

exclude_subdirectories = [
    'Oil/Images',
    'Reports/Images',
    'Reports/Crystal Reports',
    'Tyre/Images'    
]

# Convert ignore list to lowercase
ignore_list_lower = [item.lower() for item in exclude_files]
exclude_subdirectories_lower = [item.lower() for item in exclude_subdirectories]

try:
    shutil.unpack_archive(zip_file, temporary_extraction_path)
    print("Extraction successful!")

    # Iterate through the contents of the temporary extraction folder
    extracted_folder = os.path.join(temporary_extraction_path, os.listdir(temporary_extraction_path)[0])  # Get the first item in the temporary extraction folder
    for root, dirs, files in os.walk(extracted_folder):
        for file in files:
            source_path = os.path.join(root, file)

            # Get the relative path of the file from the temporary extraction folder
            relative_path = os.path.relpath(source_path, extracted_folder)

            # Convert relative path to lowercase for case-insensitive comparison
            relative_path_lower = relative_path.lower()

            # Check if the file or folder is in the ignore list
            ignore_file = False
            for item in ignore_list_lower:
                if item in relative_path_lower:
                    ignore_file = True
                    break

            # Check if any subdirectory to ignore is present in the relative path
            ignore_subdir = False
            for subdir in exclude_subdirectories_lower:
                if subdir in relative_path_lower:
                    ignore_subdir = True
                    break

            if not ignore_file:
                # Construct the destination path, maintaining the folder structure inside 'TempExtraction'
                destination_path = os.path.join(os.path.dirname(deployed_app_location), 'TempExtraction', relative_path)

                # Copy the file to the new destination
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)  # Create necessary directories
                shutil.copy2(source_path, destination_path)

    print("Files copied successfully!")

    shutil.rmtree(temporary_extraction_path)

except Exception as e:
    print(f"Extraction failed: {e}")
