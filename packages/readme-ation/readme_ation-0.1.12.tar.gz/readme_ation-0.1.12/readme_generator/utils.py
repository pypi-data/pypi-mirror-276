import os
import subprocess
import ast
import re
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def find_all_py_files(directory):
    py_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
    return py_files

def run_subprocess(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            logging.error(f"Error running command {' '.join(command)}: {result.stderr}")
            return []
        return result.stdout.splitlines()
    except Exception as e:
        logging.exception(f"Exception running command {' '.join(command)}: {e}")
        return []

def get_python_version():
    return sys.version.split()[0]

def get_imported_packages(script_paths):
    imports = set()
    for script_path in script_paths:
        with open(script_path, 'r') as file:
            tree = ast.parse(file.read(), filename=script_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module.split('.')[0])
    return list(imports)

def open_or_create_readme(readme_path):
    if os.path.exists(readme_path):
        with open(readme_path, 'r') as file:
            return file.read()
    else:
        return ""