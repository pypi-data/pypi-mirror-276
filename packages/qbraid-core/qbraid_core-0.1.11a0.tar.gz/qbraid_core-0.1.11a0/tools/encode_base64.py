# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Encode a binary file to base64.

"""
import base64


def encode_file_to_base64(file_path):
    """
    Read a binary file and encode its contents to base64.

    Args:
        file_path (str): Path to the file to be encoded.

    Returns:
        str: Base64 encoded string of the file's contents.
    """
    try:
        # Open the file in binary read mode
        with open(file_path, "rb") as file:
            # Read the entire file
            binary_data = file.read()
            # Encode the binary data to base64
            base64_encoded_data = base64.b64encode(binary_data)
            # Convert bytes to string for easier handling
            base64_string = base64_encoded_data.decode("utf-8")
            return base64_string
    except Exception as e:
        print(f"Error reading or encoding the file: {e}")
        return None
