import random
import string

def random_number(start=0, end=100):
    """Generate a random number between start and end."""
    return random.randint(start, end)

def random_numbers(length=10):
    """Generate random numbers from all digits."""
    return ''.join(random.choices(string.digits, k=length))

def random_alpha(length=10):
    """Generate a random alphabetic string of given length."""
    return ''.join(random.choices(string.ascii_letters, k=length))

def random_alphanumeric(length=10):
    """Generate a random alphanumeric string of given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_string(length=10, chars=string.ascii_letters + string.digits + string.punctuation):
    """Generate a random string with a given set of characters."""
    return ''.join(random.choices(chars, k=length))
