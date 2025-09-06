# Standard Library Imports
import csv
import json
import os
import pickle
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
import regex as re


# Logging and Debugging
import logging
import functools
from logging import DEBUG, FileHandler, Formatter, INFO, Logger, StreamHandler

# Performance Analysis and Benchmarking
import psutil

# Web Scraping and Automation
import requests
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

# Environment Configuration
from dotenv import load_dotenv