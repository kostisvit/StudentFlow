# validators.py
import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
# Ensure you're handling both single file and list of files
    files = value if isinstance(value, list) else [value]  # If it's a list, use it; otherwise, wrap single file in a list

    valid_extensions = ['.pdf', '.doc', '.docx']  # Define allowed extensions
    for file in files:
        ext = os.path.splitext(file.name)[1]  # Extract file extension
        if ext.lower() not in valid_extensions:
            raise ValidationError(f'Unsupported file extension: {ext}. Allowed extensions are: {", ".join(valid_extensions)}.')


def file_size_validator(file):
# If the input is a list, iterate through each file; otherwise, wrap it in a list
    files = file if isinstance(file, list) else [file]
    
    max_size_mb = 10  # Maximum allowed size in MB
    for f in files:
        if f.size > max_size_mb * 1024 * 1024:  # Convert MB to bytes
            raise ValidationError(f"Το μέγεθος του αρχείου '{f.name}' θα πρέπει να είναι {max_size_mb} MB. Προσπαθήστε πάλι.")