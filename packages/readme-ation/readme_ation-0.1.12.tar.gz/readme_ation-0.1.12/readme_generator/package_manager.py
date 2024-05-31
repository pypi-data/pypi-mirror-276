import shutil
import re
import sys
from .utils import run_subprocess

IGNORED_LIB_MODULES = {'os', 'enum', 'random', 'readme_version_logger'}

def get_installed_packages():
    packages = {}
    if shutil.which('mamba'):
        mamba_lines = run_subprocess(['mamba', 'list'])
        for line in mamba_lines:
            if line.startswith('#'):
                continue
            parts = re.split(r'\s+', line)
            if len(parts) >= 2:
                package, version = parts[0], parts[1]
                packages[package] = version

    pip_lines = run_subprocess([sys.executable, '-m', 'pip', 'freeze'])
    for line in pip_lines:
        if '==' in line:
            pkg, version = line.split('==')
            if pkg not in packages:
                packages[pkg] = version

    return packages

def get_specific_packages_versions(imported_packages, installed_packages):
    specific_versions = {}
    for package in imported_packages:
        if package in IGNORED_LIB_MODULES:
            continue
        specific_versions[package] = installed_packages.get(package, "")
    return specific_versions
