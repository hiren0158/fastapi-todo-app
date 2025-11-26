"""
Common dependencies for FastAPI routes.
"""
from typing import Annotated, Optional, Dict
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from jose import JWTError
from .security import decode_token


oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token', auto_error=False)


async def get_current_user(
    request: Request,
    token: Annotated[Optional[str], Depends(oauth2_bearer)] = None
) -> Dict:
    """
    Get the current authenticated user from JWT token.
    
    Checks both Authorization header and cookies for the token.
    
    Args:
        request: FastAPI request object
        token: Optional token from Authorization header
    
    Returns:
        Dictionary with user information (username, id, user_role)
    
    Raises:
        HTTPException: If token is invalid or missing
    """
    try:
        # Fallback to cookie if no Authorization header token present
        if not token:
            token = request.cookies.get('access_token')
        
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate user'
            )
        
        payload = decode_token(token)
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        user_role: str = payload.get('role')
        
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate user'
            )
        
        return {'username': username, 'id': user_id, 'user_role': user_role}
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user'
        )


async def require_admin(user: Annotated[Dict, Depends(get_current_user)]) -> Dict:
    """
    Dependency to require admin role.
    
    Args:
        user: Current user from get_current_user dependency
    
    Returns:
        User dictionary if user is admin
    
    Raises:
        HTTPException: If user is not admin
    """
    if user is None or user.get('user_role', '').lower() != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Admin access required'
        )
    return user


# Type alias for user dependency
UserDependency = Annotated[Dict, Depends(get_current_user)]
AdminDependency = Annotated[Dict, Depends(require_admin)]
