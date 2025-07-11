# login_dataAccess.py

def load_users(file_path: str = "user.txt") -> list[tuple[str, str]]:
   
    try:
        with open(file_path, "r") as f:
            users = []
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "," in line:
                    parts = line.split(",")
                    if len(parts) == 2:
                        users.append((parts[0].strip(), parts[1].strip()))
        return users
    except Exception as e:
        print(f"[DataAccess] Error reading user file: {e}")
        return []
