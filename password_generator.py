import random
import string

def generate_password(length=12, include_digits=True, include_special_chars=True):
    # Define character sets
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits if include_digits else ''
    special_chars = string.punctuation if include_special_chars else ''

    # Combine character sets based on user preferences
    all_chars = lowercase_letters + uppercase_letters + digits + special_chars

    # Ensure the password length is at least 8 characters
    length = max(length, 16)

    # Generate the password
    password = ''.join(random.choice(all_chars) for _ in range(length))

    return password


