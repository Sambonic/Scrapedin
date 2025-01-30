
from src.configurations.common_imports import (Chrome, ChromeOptions, WebDriverWait)

class DriverManager:
    """
    Manages the WebDriver instance and provides access to it.
    """
    def __init__(self):
        self.driver = self._set_driver()
        self.wait = WebDriverWait(self.driver, 1)

    def get_driver(self) -> Chrome:
        """Returns the WebDriver instance."""
        return self.driver

    def get_wait(self) -> WebDriverWait:
        """Returns the WebDriverWait instance."""
        return self.wait

    def _set_driver(self) -> Chrome:
        """Creates and configures a Chrome WebDriver instance with desired options."""
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--silent")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-webgl")
        chrome_options.add_argument("--no-sandbox")  
        chrome_options.add_argument("--disable-webrtc")

        driver = Chrome(options=chrome_options)
        return driver
