import random
import string


# Function to generate unique customer IDs
def generateCustomerID():
    # Example: 7590-VHVEG
    """
    Generates a unique ID for customers.
    """
    a = 0
    b = 0
    digit_part = []
    letter_part = []

    while a < 4:
        digit = str(random.randint(0, 9))
        digit_part.append(digit)
        a = a + 1

    while b < 5:
        letter = random.choice(string.ascii_uppercase)
        letter_part.append(letter)
        b = b + 1

    digit_part = "".join(digit_part)
    letter_part = "".join(letter_part)

    unique_id = f"{digit_part}-{letter_part}"
    return unique_id
