"""
Security utilities for password hashing and JWT token management.
"""
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import timedelta, datetime, timezone
from ..config import settings


# Password hashing context
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return bcrypt_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Hash a password."""
    return bcrypt_context.hash(password)


def create_access_token(username: str, user_id: str, role: str, expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        username: Username to encode in token
        user_id: User ID to encode in token
        role: User role to encode in token
        expires_delta: Token expiration time delta
    
    Returns:
        Encoded JWT token string
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    
    return jwt.encode(encode, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> dict:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded token payload
    
    Raises:
        JWTError: If token is invalid or expired
    """
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
