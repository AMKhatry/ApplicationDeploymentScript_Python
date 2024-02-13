import os
import shutil
import datetime

# C:\Users\User\Aditya\Personal\New folder\Equipcom
dateTimeString = datetime.datetime.now().strftime("%d%m%Y_%H%M")
deployedAppLocation = input("Enter the deployed application path: ")
backupDestination = os.path.join(deployedAppLocation, f"Backup\\Equipcom_{dateTimeString}")

# shutil.copy2(deployedAppLocation, backupDestination)

