from src.configurations.common_imports import csv, datetime, os
from src.configurations.path_manager import PathManager

class CSVHandler:
    def __init__(self, logger, role, path:PathManager):
        self.logger = logger
        self.file_name = self.set_csv_filename(role)
        self.path = path

    def set_csv_filename(self, role):
        """
        Creates a filename based on the role and current timestamp.
        """
        if not role:
            self.logger.warning("Role is not provided for CSV file naming.")
            role = "default_role"
        
        current_time = datetime.now()
        file_date = current_time.strftime("%Y%m%d%H%M")
        role = role.lower().replace(' ', '_')
        return f"{role}_{file_date}.csv"


    def write_header(self, fieldnames):
        """
        Write the header to the CSV file (overwrites if file exists).
        """
        file_path = self._get_csv_file_path()

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            self.logger.info(f"Header written to {file_path}")


    def _add_to_csv(self, job_details:dict) -> None:
        """
        Adds job listing details to a CSV file. Creates necessary folders if needed, 
        formats the data, and appends it to an appropriately named CSV file.
        """
        file_path = self.path._get_csv_file_path(self.file_name)

        file_exists = os.path.exists(file_path)

        with open(file_path, mode='a', newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=job_details.keys())

            # Write header only if the file doesn't exist
            if not file_exists:
                try:
                    self.logger.info("Creating a new CSV file with header...")
                    writer.writeheader()
                except OSError as e:
                    self.logger.error(f"An error occurred while creating the file: {str(e)}")
            
            writer.writerow(job_details)
            self.logger.info("Job details added to CSV file successfully.")
