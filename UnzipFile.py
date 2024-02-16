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
    'web.config',
    os.path.join('Oil', 'Images'),
    os.path.join('Reports', 'Images'),
    os.path.join('Reports', 'Crystal Reports'),
    os.path.join('Tyre', 'Images')
]

destination_path = os.path.join(os.path.dirname(deployed_app_location), "Temporary Destination")

ignored = []
for file in exclude_files:
    ignore_file = os.path.join(deployed_app_location, file)
    ignored.append(ignore_file)

try:
    shutil.unpack_archive(zip_file, temporary_extraction_path)
    print("Extraction successful!")

    extracted_sub_folder = os.path.join(temporary_extraction_path, os.listdir(temporary_extraction_path)[0])

    shutil.copytree(extracted_sub_folder, destination_path, ignore=ignored, dirs_exist_ok=True)
    print("Migration successful!")

    shutil.rmtree(temporary_extraction_path)

except Exception as e:
    print(f"Migration failed: {e}")
