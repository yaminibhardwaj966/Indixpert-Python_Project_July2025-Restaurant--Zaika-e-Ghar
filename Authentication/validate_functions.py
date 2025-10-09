
from datetime import datetime
    
def is_valid_email(email):
    
    if "@" not in email or "." not in email:
        return False
    
    if email.startswith("@") or email.endswith("@"):
        return False
    
    if email.index("@") > email.rindex("."):
        return False
    
    return True

def is_email_registered(email, users):
    """
    Checks if email is already present in users list
    """
    return any(u["email"] == email for u in users)

def is_valid_username(username):
    return username.isalpha()

def is_valid_password(password):
    return password.isalnum()


def is_valid_experience(experience):
    return experience.isdigit() and int(experience) >= 0

def is_valid_dob(dob):
    try:
        datetime.strptime(dob, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def is_valid_aadhar(aadhar):
    return aadhar.isdigit() and len(aadhar) == 12