"""
Admin router for administrative operations.
"""
from typing import Annotated, Dict
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from ..models_beanie import Todo
from ..core.dependencies import require_admin


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

AdminDependency = Annotated[Dict, Depends(require_admin)]


@router.get('/todo', status_code=status.HTTP_200_OK)
async def get_all_todos(admin: AdminDependency):
    """Get all todos (admin only)."""
    return await Todo.find_all().to_list()


@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(admin: AdminDependency, todo_id: str):
    """Delete any todo (admin only)."""
    todo_model = await Todo.get(todo_id)
    
    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Todo not found'
        )
    
    await todo_model.delete()