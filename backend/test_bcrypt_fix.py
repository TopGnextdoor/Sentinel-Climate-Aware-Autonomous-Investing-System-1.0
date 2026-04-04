import sys
from app.utils.security import hash_password, verify_password

try:
    long_pwd = "a" * 80
    h = hash_password(long_pwd)
    v = verify_password(long_pwd, h)
    print(f"SUCCESS. Hash: {h}. Verified: {v}")
except Exception as e:
    print(f"FAILED. Error: {str(e)}")
