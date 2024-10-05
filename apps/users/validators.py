# validators.py
import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # Extract the file extension
    valid_extensions = ['.pdf','.doc', '.docx']  # Add any file extensions you want to allow
    if not ext.lower() in valid_extensions:
        raise ValidationError(f'Unsupported file extension: {ext}. Allowed extensions are: {", ".join(valid_extensions)}.')


def file_size_validator(value):
    file_max_size = 10
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Το μέγεθος του αρχείου θα πρέπει να είναι {file_max_size} MB. Προσπαθήστε πάλι.")
