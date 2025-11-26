import random
import string


# Function to generate unique customer IDs
def generateCustomerID():
    # Example: 7590-VHVEG
    """
    Generates a customer unique ID in the format: XXXX-XXXXX
    Example: 7590-VHVEG

    Returns:
        str: A unique customer ID string
    """
    # Initialise counters and lists
    a = 0
    b = 0
    digit_part = [] # Stores the 4-digit number part
    letter_part = [] # Stores the 5-letter code  part

    # Generate 4 random digits (0-9)
    while a < 4:
        digit = str(random.randint(0, 9))
        digit_part.append(digit)
        a = a + 1

    # Generate 5 random uppercase letters (A-Z)
    while b < 5:
        letter = random.choice(string.ascii_uppercase)
        letter_part.append(letter)
        b = b + 1

    # Convert lists to strings
    digit_part = "".join(digit_part) # Combine digits into one string
    letter_part = "".join(letter_part) # Combine letters into one string

    # Create final ID in format: XXXX-XXXXX
    unique_id = f"{digit_part}-{letter_part}"
    return unique_id
