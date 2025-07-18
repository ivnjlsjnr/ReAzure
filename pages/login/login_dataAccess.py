# login_dataAccess.py

def load_admins(file_path: str = "admin.txt") -> list[tuple[str, str]]:
    """
    Load admin credentials from admin.txt.
    Returns a list of (username, password) tuples.
    """
    try:
        with open(file_path, "r") as f:
            admins = []
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "," in line:
                    parts = line.split(",")
                    if len(parts) == 2:
                        admins.append((parts[0].strip(), parts[1].strip()))
        return admins
    except Exception as e:
        print(f"[DataAccess] Error reading admin file: {e}")
        return []
