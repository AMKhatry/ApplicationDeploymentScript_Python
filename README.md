# Deployed Application Backup and Migration Tool

This Python script automates the backup and migration process for deployed applications. It simplifies the creation of timestamped backups and facilitates the extraction, timestamp restoration, and transfer of build files.

## Features

- **Backup Functionality:** Creates timestamped backups of deployed applications.
- **Migration Functionality:** Extracts build files, restores timestamps, and transfers files to a destination while excluding specified files and directories.
- **User Interaction:** Prompts users to input the path of the deployed application.
- **Exception Handling:** Gracefully handles various exceptions such as file not found and permission denied.

## Usage

1. Clone this repository to your local machine.
2. Ensure you have Python installed.
3. Run the script (`ApplicationDeploymentScript.py`).
4. Follow the prompts to enter the path of the deployed application.
5. The script will automate the backup and migration tasks.

## Dependencies

- `os`, `shutil`, `datetime`, `zipfile`, `time`, `pathlib`: Standard Python libraries.

## Configuration

- Modify the `EXCLUDED_FILES` list in the script to exclude specific files and directories during migration.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.
