"""
Tag Replacement Tool

This tool enables you to replace predefined tags in multiple files using variant-specific configurations. It also creates backups of modified files, allowing you to revert all changes back to their original state. This tool is especially useful for multi-target deployments or pre-compile steps where you need to modify target-specific values.

Author: Eray Ozturk | erayozturk1@gmail.com 
URL: github.com/diffstorm
Date: 22/02/2021
"""

import json
import os
import sys
import shutil
# from charamel import Detector

def log(text):
    """
    Print text, handling UnicodeEncodeError by encoding to UTF-8.
    """
    try:
        print(text)
    except UnicodeEncodeError:
        if sys.stdout.encoding == 'UTF-8':
            print(text.encode('utf-8').decode(sys.stdout.encoding))
        else:
            print(text.encode(sys.stdout.encoding, 'replace').decode(sys.stdout.encoding))

def usage():
    """
    Display usage information.
    """
    log("Usage: replace_tags.py <config> <action> <variant_name>")

def detect_file_encoding(filename):
    """
    Detect the encoding of a file.

    Args:
        filename (str): The path to the file.

    Returns:
        str: The detected encoding.
    """
    #with open(filename, 'rb') as f:
    #    detector = Detector()
    #    result = detector.detect(f.read())
    return 'UTF-8'

def read_config(filename):
    """
    Read the JSON configuration file.

    Args:
        filename (str): The path to the config file.

    Returns:
        dict or None: The parsed JSON configuration or None if the file doesn't exist.
    """
    config = None
    if os.path.exists(filename):
        with open(filename, 'r', encoding=detect_file_encoding(filename)) as f:
            config = json.load(f)
    else:
        log(f"Config file not found: {filename}")
    return config

def summarize(config):
    """
    Display a summary of the file list and variants in the config.

    Args:
        config (dict): The configuration dictionary.
    """
    if "files" in config:
        log("Files to be modified:")
        for file in config["files"]:
            log(f"- {file}")

    if "variants" in config:
        log("Variants in the config:")
        for variant in config["variants"]:
            log(f"- Name: {variant['name']}")
            log("  Replacements:")
            for tag, value in variant["replacements"].items():
                log(f"  - {tag}: {value}")

def replace_tags_in_file(filename, replacements):
    """
    Replace tags in a file with specified values.

    Args:
        filename (str): The path to the file.
        replacements (dict): A dictionary of tag-value pairs.

    Returns:
        str: The modified content.
        str: The detected encoding of the file.
        bool: True if modifications were made, False otherwise.
    """
    encoding = None
    try:
        encoding = detect_file_encoding(filename)
        with open(filename, 'r', encoding=encoding) as f:
            content = f.read()
    except FileNotFoundError:
        log(f"File not found: {filename}. Skipping.")
        return "", None, False

    modified = False
    for tag, value in replacements.items():
        if tag in content:
            content = content.replace(tag, value)
            modified = True
            log(f"Replaced '{tag}' with '{value}' in {filename}")
    
    return content, encoding, modified

def write_modified_content(filename, content, encoding):
    """
    Write modified content back to a file.

    Args:
        filename (str): The path to the file.
        content (str): The modified content.
        encoding (str): The encoding of the file.
    """
    try:
        with open(filename, 'w', encoding=encoding) as f:
            f.write(content)
        log(f"Modified content saved to {filename}")
    except UnicodeEncodeError:
        log(f"Unable to write modified content to {filename}. Encoding issue.")

def backup_exists(filename):
    """
    Check if a .bak file exists for the given file.

    Args:
        filename (str): The path to the file.

    Returns:
        bool: True if a .bak file exists, False otherwise.
    """
    backup_filename = f"{filename}.bak"
    return os.path.exists(backup_filename)

def create_backup(filename):
    """
    Create a backup of a file.

    Args:
        filename (str): The path to the file.
    """
    if os.path.exists(filename):
        backup_filename = f"{filename}.bak"
        shutil.copy2(filename, backup_filename)
        log(f"Created a backup of {filename} as {backup_filename}")
    else:
        log(f"File not found: {filename}. Skipping backup.")

def revert_from_backup(filename):
    """
    Revert changes by restoring a file from its backup.

    Args:
        filename (str): The path to the file.
    """
    backup_filename = f"{filename}.bak"
    if os.path.exists(backup_filename):
        shutil.move(backup_filename, filename)
        log(f"Reverted changes for {filename}")
    else:
        log(f"No backup found for {filename}")

def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        usage()
        return

    fconfig = sys.argv[1].strip()
    action = sys.argv[2].strip().lower()
    
    variant_name = None
    if len(sys.argv) == 4:
        variant_name = sys.argv[3].strip()

    config = read_config(fconfig)
    if config is None:
        return

    if action == "replace":
        variant = next((v for v in config.get("variants", []) if v["name"] == variant_name), None)
        if not variant:
            log(f"Variant '{variant_name}' not found!")
            return
        
        for file in config.get("files", []):
            if not backup_exists(file):
                create_backup(file)
            else:
                log(f"Backup already exists for {file}")
            modified_content, encoding, modified = replace_tags_in_file(file, variant["replacements"])
            if modified:
                write_modified_content(file, modified_content, encoding)
            else:
                log(f"No modifications made to {file}. Skipping save.")

    elif action == "revert":
        for file in config.get("files", []):
            revert_from_backup(file)

    elif action == "summarize":
        summarize(config)

    else:
        log("Invalid action")
        usage()

if __name__ == "__main__":
    main()
