import os
import subprocess
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

def _run_subprocess(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            logging.error(f"Error running command {' '.join(command)}: {result.stderr}")
            return []
        return result.stdout.splitlines()
    except Exception as e:
        logging.exception(f"Exception running command {' '.join(command)}: {e}")
        return []