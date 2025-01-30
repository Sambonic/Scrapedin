from src.configurations.common_imports import pickle

class FileManager:
    """Handles reading from and writing to files."""

    def __init__(self, path_manager):
        self.path_manager = path_manager

    def read_cookies(self, email: str):
        """Reads cookies from a file."""
        file_path = self.path_manager.get_user_cookie_path(email)
        try:
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return None

    def write_cookies(self, email: str, data):
        """Writes cookies to a file."""
        file_path = self.path_manager.get_user_cookie_path(email)
        try:
            with open(file_path, 'wb') as file:
                pickle.dump(data, file)
        except IOError as e:
            raise IOError(f"Failed to write cookies to file: {file_path}") from e