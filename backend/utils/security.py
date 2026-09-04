import bcrypt

def hash_password(password: str) -> str:
    """Hash password using bcrypt directly to avoid passlib deprecation/compatibility bugs."""
    if not password:
        raise ValueError("Password cannot be empty")
    pw_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw_bytes, salt).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against a bcrypt hash."""
    if not password or not hashed_password:
        return False
    try:
        pw_bytes = password.encode('utf-8')[:72]
        hash_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(pw_bytes, hash_bytes)
    except Exception as e:
        print(f"[SECURITY VERIFY ERROR] {e}")
        return False
