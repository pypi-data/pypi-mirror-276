import importlib
import json
import shutil
import re
import sys
import ast
from .utils import _run_subprocess

IGNORED_LIB_MODULES = {'os', 'enum', 'random'}

def extract_code_from_ipynb(notebook_path):
    with open(notebook_path, 'r') as file:
        notebook_content = json.load(file)
    
    code_cells = []
    for cell in notebook_content['cells']:
        if cell['cell_type'] == 'code':
            code_cells.append(''.join(cell['source']))
    
    return '\n'.join(code_cells)

def get_imported_top_level_packages(script_paths):
    imported_packages = set()
    for script_path in script_paths:
        if script_path.endswith('.ipynb'):
            code = extract_code_from_ipynb(script_path)
        else:
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

def get_specific_package_versions(imported_packages, installed_packages):
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
    packages_with_versions = get_specific_package_versions(imported_packages, installed_packages)
    return packages_with_versions