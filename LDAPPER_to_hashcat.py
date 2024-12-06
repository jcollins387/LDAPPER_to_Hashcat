import base64
import re
import sys

def process_ldap_output(input_file):
    try:
        # Read and parse the input file
        with open(input_file, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    # Extract samAccountName and orclCommonAttribute
    sam_account_names = []
    attributes = []
    for line in lines:
        if re.search(r'samaccountname', line, re.IGNORECASE):
            sam_account_names.append(line.split()[-1].strip())
        elif re.search(r'orclcommonattribute', line, re.IGNORECASE):
            attributes.append(line.split()[-1].strip())

    # Ensure matching pairs
    if len(sam_account_names) != len(attributes):
        print("Error: Mismatch between samAccountName and orclCommonAttribute count.")
        sys.exit(1)

    # Combine into username:password format
    combined = [f"{user}:{pwd}" for user, pwd in zip(sam_account_names, attributes)]

    # Categorize and decode hashes
    md5_decoded = []
    sha_decoded = []
    other_hashes = []

    for entry in combined:
        username, hash_data = entry.split(':', 1)
        if hash_data.startswith("{MD5}"):
            decoded_hash = decode_base64(hash_data[5:])
            md5_decoded.append(f"{username}:{decoded_hash}")
        elif hash_data.startswith("{SHA}"):
            decoded_hash = decode_base64(hash_data[5:])
            sha_decoded.append(f"{username}:{decoded_hash}")
        else:
            other_hashes.append(entry)

    # Write outputs
    write_output("md5_decoded.txt", md5_decoded)
    write_output("sha_decoded.txt", sha_decoded)
    write_output("other_hashes.txt", other_hashes)

    print("Processing complete. Check 'md5_decoded.txt', 'sha_decoded.txt', and 'other_hashes.txt'.")

def decode_base64(encoded_string):
    """Decodes a Base64 string and returns its hexadecimal representation."""
    try:
        decoded_bytes = base64.b64decode(encoded_string)
        return decoded_bytes.hex()
    except base64.binascii.Error:
        return "Invalid Base64"

def write_output(file_name, data):
    """Writes a list of strings to a file."""
    with open(file_name, 'w') as file:
        file.write('\n'.join(data))

if __name__ == "__main__":
    # Check if the user provided an input file
    if len(sys.argv) != 2:
        print("Usage: python ldap_processor.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    process_ldap_output(input_file)
