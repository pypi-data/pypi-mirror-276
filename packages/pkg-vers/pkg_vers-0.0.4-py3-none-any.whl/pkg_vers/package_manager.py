import importlib
import json
import shutil
import re
import sys
import ast
import os
import IPython
from .utils import _run_subprocess

IGNORED_LIB_MODULES = {'os', 'enum', 'random'}

def get_imported_packages_from_ipynb():
    try:
        # Get the current IPython shell
        ipython = IPython.get_ipython()
        if ipython is None:
            raise RuntimeError("IPython shell not found. This function must be run within a Jupyter Notebook.")

        # Get all cells from the current notebook
        cells = ipython.history_manager.input_hist_raw

        # Regular expression patterns to match import statements
        import_pattern = re.compile(r'^\s*import\s+(\S+)')
        from_import_pattern = re.compile(r'^\s*from\s+(\S+)\s+import')

        # Initialize a set to hold unique imports
        imports = set()

        # Iterate over all cells
        for cell in cells:
            for line in cell.split('\n'):
                import_match = import_pattern.match(line)
                from_import_match = from_import_pattern.match(line)
                if import_match:
                    imports.add(import_match.group(1).split('.')[0])
                elif from_import_match:
                    imports.add(from_import_match.group(1).split('.')[0])

        return imports
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return set()

def get_imported_top_level_packages(script_paths):
    imported_packages = set()
    for script_path in script_paths:
        with open(script_path, 'r') as file:
            code = file.read()
        
            tree = ast.parse(code, filename=script_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported_packages.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    imported_packages.add(node.module.split('.')[0])
    return list(imported_packages)

def get_installed_packages():
    packages = {}
    if shutil.which('mamba'):
        mamba_lines = _run_subprocess(['mamba', 'list'])
        for line in mamba_lines:
            if line.startswith('#'):
                continue
            parts = re.split(r'\s+', line)
            if len(parts) >= 2:
                package, version = parts[0], parts[1]
                packages[package] = version

    pip_lines = _run_subprocess([sys.executable, '-m', 'pip', 'freeze'])
    for line in pip_lines:
        if '==' in line:
            pkg, version = line.split('==')
            if pkg not in packages:
                packages[pkg] = version

    return packages

def get_package_version(package):
    try:
        module = importlib.import_module(package)
        return getattr(module, '__version__', '')
    except ImportError:
        return ''

def get_top_level_package_versions(imported_packages, installed_packages):
    specific_versions = {}
    for package in imported_packages:
        if package in IGNORED_LIB_MODULES:
            continue
        version = installed_packages.get(package) or installed_packages.get(package.replace("_", "-"), "")

        if not version:  # if version is empty, try to get it from module.__version__
            version = get_package_version(package)
        specific_versions[package] = version
    return specific_versions

def get_package_versions_from(files):
    if isinstance(files, str):
        files = [files]

    installed_packages = get_installed_packages()
    imported_packages = get_imported_top_level_packages(files)
    packages_with_versions = get_top_level_package_versions(imported_packages, installed_packages)
    return packages_with_versions

def get_package_versions_from_ipynb():
    installed_packages = get_installed_packages()
    imported_packages = get_imported_packages_from_ipynb()
    packages_with_versions = get_top_level_package_versions(imported_packages, installed_packages)
    return packages_with_versions