import os

class PathManager:
    """Manages project paths and directory creation."""

    def __init__(self):
        self.path = self._set_base_path()
        self.users_dir = self._create_users_dir()

    def get_base_path(self) -> str:
        """Returns the base project directory path."""
        return self.path

    def get_users_dir(self) -> str:
        """Returns the path to the 'users' directory."""
        return self.users_dir

    def get_user_cookie_path(self, email: str) -> str:
        """Returns the path to the user's cookie file based on their email."""
        return os.path.join(self.users_dir, f"{email}.pkl")

    def _get_csv_file_path(self, file_name):
        """
        Returns the full file path for the CSV file, including necessary directory creation.
        """
        file_path = os.path.join(self.path, "data", "raw_data")
        os.makedirs(file_path, exist_ok=True)
        return os.path.join(file_path, file_name)
    
    def file_exists(self, email: str) -> bool:
        """Checks if the user's cookie file exists."""
        file_path = self.get_user_cookie_path(email)
        return os.path.exists(file_path)

    def _set_base_path(self) -> str:
        """Determines and returns the base project directory path."""
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        parent_directory = os.path.dirname(current_directory)
        super_directory = os.path.dirname(parent_directory)
        return super_directory

    def _create_users_dir(self) -> str:
        """Creates the 'users' directory if it doesn't exist and returns its path."""
        users_dir = os.path.join(self.path, "users")
        os.makedirs(users_dir, exist_ok=True)
        return users_dir