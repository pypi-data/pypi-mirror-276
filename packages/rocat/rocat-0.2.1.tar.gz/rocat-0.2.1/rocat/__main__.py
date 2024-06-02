# rocat/__main__.py
import os
from rocat.config import create_default_config

def create_default_code():
    code = '''
# -*- coding: utf-8 -*-

import rocat as rc

def main():
    # Initialize the library
    rc.initialize()  

if __name__ == "__main__":
    main()

'''
    file_path = "rocat_example.py"
    if os.path.exists(file_path):
        confirm = input(f"{file_path} already exists. Do you want to overwrite it? (y/n): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            return
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(code)
    print(f"{file_path} created.")

def main():
    import sys
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "init":
            create_default_config()
            create_default_code()
            print("Default configuration file and example code created.")
            print("- config.ini")
            print("- rocat_example.py")
        else:
            print("Usage: rocat init")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
