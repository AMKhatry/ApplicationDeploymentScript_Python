import os
import shutil
import zipfile

def get_ignored_files(path, filenames):
    ret = []
    for filename in filenames:
        full_path = os.path.join(path, filename)
        if full_path.lower() in ignored_files_paths:
            ret.append(filename)
            print(f"Ignored: {full_path}") # Use f-string for string formatting
    return ret

try:
    deployed_app_location = input("Enter the deployed application path: ").strip()

    if not os.path.isdir(deployed_app_location):
        raise ValueError("Invalid directory path.")

    temporary_extraction_path = os.path.join(deployed_app_location, f"TempExtraction")
    zip_file = os.path.join(deployed_app_location, 'build.zip')

    destination_path = os.path.join(os.path.dirname(deployed_app_location), "Temporary Destination")

    # List of files to exclude
    exclude_files = [
        'Fusioncharts-suite-xt',
        'GSNetImages',
        'Images',
        'PDFS',
        'TreeLineImages',
        'Wall.jpg',
        'web.config',
        os.path.join('Oil', 'Images'),
        os.path.join('Reports', 'Images'),
        os.path.join('Reports', 'Crystal Reports'),
        os.path.join('Tyre', 'Images')
    ]

    # Extracting the zip file
    shutil.unpack_archive(zip_file, temporary_extraction_path)
    print("Extraction successful!")

    # Selecting the extracted sub-folder
    extracted_sub_folder = os.path.join(temporary_extraction_path, os.listdir(temporary_extraction_path)[0])

    # Ignored files paths
    ignored_files_paths = [os.path.join(extracted_sub_folder.lower(), file.lower()) for file in exclude_files]
    
    # Copying files to destination path, ignoring certain files
    shutil.copytree(extracted_sub_folder, destination_path, ignore=get_ignored_files, dirs_exist_ok=True)
    print("Migration successful!")

    # Removing temporary extraction path
    shutil.rmtree(temporary_extraction_path)

except FileNotFoundError:
    print("Error: File not found.")

except PermissionError:
    print("Error: Permission denied.")

except shutil.Error as e:
    print(f"Error: {e}")

except Exception as e:
    print(f"Unexpected error occurred: {e}")

