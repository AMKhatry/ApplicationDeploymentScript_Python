import os
import shutil
import zipfile
import time

def get_ignored_files(path, filenames):
    ignored = []
    for filename in filenames:
        full_path = os.path.join(path, filename)
        if full_path.lower() in ignored_files_paths:
            ignored.append(filename)
            print(f"Ignored: {full_path}") # Use f-string for string formatting
    return ignored

def restore_zip_contents_timestamps(zip_file_path, extraction_dir):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        for file_info in zip_file.infolist():

            extracted_file_path = os.path.join(extraction_dir, file_info.filename)
            
            # Adjust the date-time to avoid setting it to the current date-time
            adjusted_datetime = time.mktime(file_info.date_time + (0, 0, -1))
            
            # Update the modified time of the extracted file
            os.utime(extracted_file_path, (adjusted_datetime, adjusted_datetime))

try:
    deployed_app_location = input("Enter the deployed application path: ").strip()

    if not os.path.isdir(deployed_app_location):
        raise ValueError("Invalid directory path.")

    temporary_extraction_path = os.path.join(deployed_app_location, "TempExtraction")
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
    restore_zip_contents_timestamps(zip_file,temporary_extraction_path)

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

