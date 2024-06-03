import os
import subprocess
import ast
import re
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_python_version():
    return sys.version.split()[0]

def open_or_create_readme(readme_path):
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as file:
            return file.read()
    else:
        return ""