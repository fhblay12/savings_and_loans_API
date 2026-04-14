import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def _normalize_password(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).digest()

def hash_password(password: str) -> str:
    computed = _normalize_password(password).hex()
    print(f"Computed: {computed}")
    return computed



def verify_password(plain_password: str, hashed_password: str) -> bool:
    computed = _normalize_password(plain_password).hex()

    print(f"Computed: {computed}")
    print(f"Stored:   {hashed_password}")

    return computed == hashed_password
    print(pwd_context.verify(_normalize_password(plain_password), hashed_password))
    return pwd_context.verify(_normalize_password(plain_password), hashed_password)

