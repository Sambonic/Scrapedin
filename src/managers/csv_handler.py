from src.config.common_imports import csv, os
from src.config.path_config import path_manager
from src.managers.logger_manager import logger

class CSVHandler:
    def __init__(self, role):
        path_manager.create_csv_file(role=role)

    def _add_to_csv(self, job_details: dict) -> None:
        """
        Adds job listing details to a CSV file. Creates necessary folders if needed, 
        formats the data, and appends it to an appropriately named CSV file.
        """
        file_path = path_manager.CSV_FILE_DIR
        is_file_empty = os.path.getsize(file_path) == 0 if os.path.exists(file_path) else True

        with open(file_path, mode='a', newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=job_details.keys())

            # Write header only if the file is empty
            if is_file_empty:
                try:
                    logger.info("Creating a new CSV file with header...")
                    writer.writeheader()
                except OSError as e:
                    logger.error(f"An error occurred while creating the file: {str(e)}")

            writer.writerow(job_details)
            logger.info("Job details added to CSV file successfully.")