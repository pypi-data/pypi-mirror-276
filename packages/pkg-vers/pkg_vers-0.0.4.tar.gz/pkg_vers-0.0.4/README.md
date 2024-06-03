`pkg_vers` is a utility that helps you determine the versions of packages imported in your Python scripts. The main use case is to use the `get_package_versions_from(files)` function to get the versions of all top-level packages imported in a list of scripts.

## Features

- Extract top-level imported packages from Python scripts.
- Retrieve installed package versions using `pip` and `mamba`.
- Provide a mapping of imported packages to their installed versions.

## Usage

### Basic Usage

To get the versions of all top-level packages imported in your Python scripts, use the `get_package_versions_from(files)` function.

**Example:**

```python
from pkg_vers import get_package_versions_from

files = ['script1.py', 'script2.py']
package_versions = get_package_versions_from(files)
print(package_versions)
```

## Helper Functions

For more nuanced use cases, the following helper functions are exposed:

- `get_imported_top_level_packages(script_paths)`: Extract top-level imported packages from a list of script paths.
- `get_installed_packages()`: Retrieve a dictionary of installed packages and their versions using pip and mamba.
- `get_package_version(package)`: Get the version of a specific package using importlib.
- `get_top_level_package_versions(imported_packages, installed_packages)`: Get versions of a list of imported packages based on the installed packages.
- `get_package_versions_from_ipynb()`: Get versions of imported packages from an active Jupyter Notebook by name.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.