from src.config.common_imports import *
from src.config.path_config import path_manager

def read_cookies():
    """
    Reads cookies from a file.
    """
    file_path: str = path_manager.USER_COOKIE_DIR
    try:
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return None
    

def write_cookies(data: Any) -> None:
    """
    Writes cookies to a file.
    """
    file_path: str = path_manager.USER_COOKIE_DIR
    try:
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)
    except IOError as e:
        raise IOError(f"Failed to write cookies to file: {file_path}") from e