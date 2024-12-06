# LDAPPER_to_Hashcat
This Python script processes output from [LDAPPER](https://github.com/shellster/LDAPPER)'s custom search 13 to extract and decode password hashes into a hashcat compatible format. It identifies `{MD5}` and `{SHA}` encoded hashes, decodes them, and categorizes the remaining data. 

## Features
- Extracts `samAccountName` and `orclCommonAttribute` fields from LDAP output.
- Merges these fields into `username:password` format.
- Categorizes and processes `{MD5}`, `{SHA}`, and other types of hashes.
- Decodes `{MD5}` and `{SHA}` Base64-encoded hashes into their hexadecimal equivalents.
- Outputs results into clean, categorized text files.

## Requirements
- Python 3.6 or later

## Installation
No installation required. Just download the script and run it with Python.

## Usage
Run the script from the command line, providing the input file as an argument:

```bash
python LDAPPER_to_Hashcat.py <input_file>
```
