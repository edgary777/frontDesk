"""Input validating functions."""
import re

def validateEmail(email):
    """Validate an email.

    Input:
        - single email string
    Output:
        -Returns True if string is valid, False if not.
    """
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match is None:
        return False
    else:
        return True
