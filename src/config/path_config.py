from src.config.common_imports import *

class PathConfig:
    """Singleton class to manage project paths and ensure necessary directories are created."""

    _instance = None

    def __new__(cls) -> 'PathConfig':
        """Ensure only one instance of PathConfig exists (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super(PathConfig, cls).__new__(cls)
            cls._instance._initialize_paths()
        return cls._instance

    def _initialize_paths(self) -> None:
        """Initialize project paths and create required directories."""
        self.BASE_PATH = self._set_base_path()
        self.USERS_DIR = os.path.join(self.BASE_PATH, "users")
        self.LOGS_DIR = os.path.join(self.BASE_PATH, "logs")
        self.RAW_DATA_DIR = os.path.join(self.BASE_PATH, "data", "raw_data")
        self.CLEAN_DATA_DIR = os.path.join(self.BASE_PATH, "data", "clean_data")

        self.LOG_FILE_DIR = self.create_log_file()
        self.USER_COOKIE_DIR = None
        self.CSV_FILE_DIR = None

        self._create_directories()

    def _set_base_path(self) -> str:
        """Determine and return the base project directory path."""
        
        github_workspace = os.environ.get("GITHUB_WORKSPACE")
        if github_workspace:
            return github_workspace
        
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        parent_directory = os.path.dirname(current_directory)
        super_directory = os.path.dirname(parent_directory)
        return super_directory
    
    def create_log_file(self) -> str:
        current_time = datetime.now()
        file_date = current_time.strftime("%Y%m%d%H%M")
        _, path = self.check_path_exists(self.LOGS_DIR, f"log{file_date}", ".txt")
        return path
    
    def create_user_file(self, email: str) -> None:
        _, self.USER_COOKIE_DIR = self.check_path_exists(self.USERS_DIR, f"{email}", ".pkl")
    
    def create_csv_file(self, role: str) -> None:
        """Creates a filename based on the role and current timestamp."""     
        current_time = datetime.now()
        file_date = current_time.strftime("%Y%m%d%H%M")
        role = role.lower().replace(' ', '_')
        _, self.CSV_FILE_DIR = self.check_path_exists(self.RAW_DATA_DIR, f"{role}_{file_date}", ".csv")

    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        for _, path in vars(self).items():
            if path and not os.path.basename(path).__contains__("."):
                os.makedirs(path, exist_ok=True)
    
    def get_csv_file_path(self, file_name: str) -> str:
        """
        Returns the full file path for the CSV file, including necessary directory creation.
        """
        return os.path.join(self.RAW_DATA_DIR, file_name)
    
    def check_path_exists(self, path: str, file:str=None, extension:str=None) -> Tuple[bool, str]:
        """Check if the given path exists, and if not, create it. """

        if file and extension:
            path = os.path.join(path, f"{file}{extension}")

        if not os.path.exists(path):
            return False, path
        
        return True, path
    
    def get_all_paths(self) -> None:
        """Print all initialized paths for the project."""
        for k, v in vars(self).items():
            print(f"{k}: {v}")


"""
Initialize the singleton instance as soon as the module is imported and make
all its variables publicly available for simpler access across all files.
"""
path_manager = PathConfig()
globals().update(vars(path_manager))
