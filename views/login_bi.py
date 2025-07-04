import os

def load_users(file_path="user.txt"):
    """Load users from a file. Each line should be 'username,password'."""
    if not os.path.exists(file_path):
        raise FileNotFoundError("User database not found.")
    
    with open(file_path, "r") as f:
        users = [line.strip().split(",") for line in f if "," in line]
    return users

def validate_credentials(username, password, users):
    """Check if the provided credentials match any user in the list."""
    uname = username.strip()
    pword = password.strip()
    return any(uname == u.strip() and pword == p.strip() for u, p in users)
