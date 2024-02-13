import os
import shutil
import datetime


def backup_folder(deployed_app_location, backup_destination):
    try:
        # Function to determine which files to ignore during copy
        def ignore_backup_folder(directory, contents):
            return ['Backup'] if 'Backup' in contents else []
        
        shutil.copytree(deployed_app_location, backup_destination, ignore=ignore_backup_folder)
        print("Backup successful!")
    except Exception as e:
        print(f"Backup failed: {e}")


def main():
    deployed_app_location = input("Enter the deployed application path: ")
    
    date_time_string = datetime.datetime.now().strftime("%d%m%Y_%H%M")
    
    backup_destination = os.path.join(deployed_app_location, f"Backup\\Equipcom_{date_time_string}")

    backup_folder (deployed_app_location, backup_destination)

main()