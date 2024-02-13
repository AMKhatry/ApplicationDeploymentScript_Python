import os
import shutil

deployed_app_location = input("Enter the deployed application path: ")
temporary_extraction_path = os.path.join(deployed_app_location, f"TempExtraction")

zip_file = os.path.join(deployed_app_location, 'Build.zip')

try:
    shutil.unpack_archive(zip_file, temporary_extraction_path)
    print("Extraction successful!")

except Exception as e:
    print(f"Extraction failed: {e}")

