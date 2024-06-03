import os
import subprocess
import logging
import time
from IPython.display import Javascript, display

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global variable to hold the notebook name
notebook_name = None

# Function to execute JavaScript and set the global variable `notebook_name`
def _get_notebook_name():
    global notebook_name
    js_code = '''
    (function() {
        var kernel = Jupyter.notebook.kernel;
        var command = "notebook_name = '" + Jupyter.notebook.notebook_name + "'";
        kernel.execute(command);
    })();
    '''
    display(Javascript(js_code))

# Function to retrieve the notebook name
def retrieve_notebook_name():
    global notebook_name
    # Call the function to get the notebook name via JavaScript
    _get_notebook_name()
    
    # Wait for the JavaScript to set the `notebook_name` variable
    for _ in range(10):  # Retry for up to 10 seconds
        if notebook_name:
            return notebook_name
        time.sleep(1)
    
    # If the variable is not set, return a friendly message
    return "Notebook name could not be retrieved."

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