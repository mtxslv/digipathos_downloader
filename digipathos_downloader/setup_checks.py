import sys

# Check if python version > 3.6
if sys.version_info < (3, 6):
    print("Python version 3.6 or higher is required to run this script.")
    sys.exit(1)

# Check if request package is installed
try:
    import requests
except ModuleNotFoundError as e:
    print(e)
    print("Module 'requests' was not found. Please install it via the following command:\n"
          "pip install request")
