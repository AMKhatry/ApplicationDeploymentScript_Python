import os
import shutil
import datetime
import zipfile
import time
from pathlib import Path

# Constants
BACKUP_FOLDER = 'Backup'
BUILD_FOLDER = 'Build Files'
BUILD_FILE = 'Build.zip'
EXCLUDED_FILES = [
    'Fusioncharts-suite-xt',
    'GSNetImages',
    'Images',
    'PDFS',
    'TreeLineImages',
    'Wall.jpg',
    'web.config',
    os.path.join('Oil', 'Images'),
    os.path.join('Reports', 'Images'),
    os.path.join('Reports', 'CrystalReports'),
    os.path.join('Tyre', 'Images')
]

# Function to ignore the backup folder during copying
def ignore_backup_folder(directory, contents):
    return [BACKUP_FOLDER] if BACKUP_FOLDER in contents else []

# Function to get ignored files
def get_ignored_files(path, filenames):
    ignored = []
    for filename in filenames:
        full_path = os.path.join(path, filename)
        if full_path.lower() in ignored_files_paths:
            ignored.append(filename)
            print(f"Ignored: {full_path}")
    return ignored

# Function to get the build file
def get_build_file(path, filenames):
    for filename in filenames:
        if filename.lower() == BUILD_FILE.lower():
            return os.path.join(path, filename)
    return None

# Function to create a backup of the deployed application
def backup_folder(deployed_app_location, backup_destination):
    try:
        shutil.copytree(deployed_app_location, backup_destination, ignore=ignore_backup_folder)
        print("Backup successful!")
    except Exception as e:
        print(f"Backup failed: {e}")

# Restores timestamps of files extracted from a zip.
def restore_zip_contents_timestamps(zip_file_path, extraction_dir):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        for file_info in zip_file.infolist():
            extracted_file_path = os.path.join(extraction_dir, file_info.filename)
            adjusted_datetime = time.mktime(file_info.date_time + (0, 0, -1))
            os.utime(extracted_file_path, (adjusted_datetime, adjusted_datetime))

try:
    deployed_app_location = input("Enter the deployed application path: ").strip()

    # Validate if the directory exists
    if not os.path.isdir(deployed_app_location):
        raise ValueError("Invalid directory path.")

     # Create a timestamp for the backup
    current_date_time_string = datetime.datetime.now().strftime("%d%m%Y_%H%M")
    backup_destination = os.path.join(deployed_app_location, BACKUP_FOLDER, f"Backup_{current_date_time_string}")
    backup_folder(deployed_app_location, backup_destination)

    temporary_extraction_path = os.path.join(deployed_app_location, "TempExtraction")

    # Get the build file
    zip_file = get_build_file(deployed_app_location, os.listdir(deployed_app_location))
    
    destination_path = os.path.join(os.path.dirname(deployed_app_location), "Temporary Destination")

    shutil.unpack_archive(zip_file, temporary_extraction_path)
    print("Extraction successful!")

    # Restore timestamps of extracted files
    restore_zip_contents_timestamps(zip_file,temporary_extraction_path)
    
    extracted_sub_folder = os.path.join(temporary_extraction_path, os.listdir(temporary_extraction_path)[0])
    ignored_files_paths = [os.path.join(extracted_sub_folder.lower(), file.lower()) for file in EXCLUDED_FILES]
    
    # Copy extracted files to destination
    shutil.copytree(extracted_sub_folder, destination_path, ignore=get_ignored_files, dirs_exist_ok=True)
    print("Migration successful!")

    # Move the build file to another location and rename it
    # Construct the new build location
    new_build_location = os.path.join(deployed_app_location, f"{BUILD_FOLDER}\\Published-{current_date_time_string}.zip")
    
    # Ensure that the destination directory exists
    os.makedirs(os.path.dirname(new_build_location), exist_ok=True)

    # Move the build file
    try:
        shutil.move(zip_file, new_build_location)
        print("Build file moved successfully!")
    except Exception as e:
        print(f"Error when transferring the build file: {e}")

    shutil.rmtree(temporary_extraction_path)

except FileNotFoundError:
    print("Error: File not found.")

except PermissionError:
    print("Error: Permission denied.")

except shutil.Error as e:
    print(f"Error: {e}")

except Exception as e:
    print(f"Unexpected error occurred: {e}")
