"""
User management router for user profile and password management.
"""
from typing import Annotated, Dict
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from ..models_beanie import User
from ..schemas.user import UserVerification
from ..core.dependencies import get_current_user
from ..core.security import verify_password, hash_password


router = APIRouter(
    prefix='/user',
    tags=['user']
)

UserDependency = Annotated[Dict, Depends(get_current_user)]


@router.get('/user', status_code=status.HTTP_200_OK)
async def get_user(user: UserDependency):
    """Get current user information."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user'
        )
    
    user_doc = await User.get(user.get('id'))
    
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    return user_doc


@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: UserDependency, user_verification: UserVerification):
    """Change user password."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication failed'
        )
    
    user_doc = await User.get(user.get('id'))
    
    if not user_doc or not verify_password(user_verification.password, user_doc.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect"
        )
    
    user_doc.hashed_password = hash_password(user_verification.new_password)
    await user_doc.save()