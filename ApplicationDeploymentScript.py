import os
import shutil
import datetime
import zipfile
import time

# Constants
BACKUP_FOLDER_NAME = 'Backup'
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
    os.path.join('Reports', 'Crystal Reports'),
    os.path.join('Tyre', 'Images')
]

def ignore_backup_folder(directory, contents):
    # Determines which files to ignore during copy.
    return [BACKUP_FOLDER_NAME] if BACKUP_FOLDER_NAME in contents else []

def get_ignored_files(path, filenames):
    # Returns a list of ignored files.
    ignored = []
    for filename in filenames:
        full_path = os.path.join(path, filename)
        if full_path.lower() in ignored_files_paths:
            ignored.append(filename)
            print(f"Ignored: {full_path}")
    return ignored

def backup_folder(deployed_app_location, backup_destination):
    # Creates a backup of the deployed application.
    try:
        shutil.copytree(deployed_app_location, backup_destination, ignore=ignore_backup_folder)
        print("Backup successful!")
    except Exception as e:
        print(f"Backup failed: {e}")

def restore_zip_contents_timestamps(zip_file_path, extraction_dir):
    # Restores timestamps of files extracted from a zip.
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        for file_info in zip_file.infolist():
            extracted_file_path = os.path.join(extraction_dir, file_info.filename)
            adjusted_datetime = time.mktime(file_info.date_time + (0, 0, -1))
            os.utime(extracted_file_path, (adjusted_datetime, adjusted_datetime))

try:
    deployed_app_location = input("Enter the deployed application path: ").strip()

    if not os.path.isdir(deployed_app_location):
        raise ValueError("Invalid directory path.")
        
    current_date_time_string = datetime.datetime.now().strftime("%d%m%Y_%H%M")
    backup_destination = os.path.join(deployed_app_location, f"{BACKUP_FOLDER_NAME}\\Backup_{current_date_time_string}")
    backup_folder(deployed_app_location, backup_destination)

    temporary_extraction_path = os.path.join(deployed_app_location, "TempExtraction")
    zip_file = os.path.join(deployed_app_location, 'build.zip')
    destination_path = os.path.join(os.path.dirname(deployed_app_location), "Temporary Destination")

    shutil.unpack_archive(zip_file, temporary_extraction_path)
    print("Extraction successful!")
    restore_zip_contents_timestamps(zip_file,temporary_extraction_path)

    extracted_sub_folder = os.path.join(temporary_extraction_path, os.listdir(temporary_extraction_path)[0])
    ignored_files_paths = [os.path.join(extracted_sub_folder.lower(), file.lower()) for file in EXCLUDED_FILES]
    
    shutil.copytree(extracted_sub_folder, destination_path, ignore=get_ignored_files, dirs_exist_ok=True)
    print("Migration successful!")

    shutil.rmtree(temporary_extraction_path)

except FileNotFoundError:
    print("Error: File not found.")

except PermissionError:
    print("Error: Permission denied.")

except shutil.Error as e:
    print(f"Error: {e}")

except Exception as e:
    print(f"Unexpected error occurred: {e}")
