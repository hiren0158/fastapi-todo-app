"""
Todo management router for CRUD operations and page rendering.
"""
from datetime import datetime
from typing import Annotated, Dict
from zoneinfo import ZoneInfo

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.responses import RedirectResponse

from ..config import settings
from ..core.dependencies import get_current_user
from ..models_beanie import Todo
from ..schemas.todo import TodoRequest


router = APIRouter(
    prefix='/todos',
    tags=['todos']
)

UserDependency = Annotated[Dict, Depends(get_current_user)]
templates = Jinja2Templates(directory="ToDoApp2/templates")

try:
    ROUTER_TIMEZONE = ZoneInfo(settings.timezone)
except Exception:  # pragma: no cover - fallback path
    ROUTER_TIMEZONE = ZoneInfo("UTC")


def redirect_to_login():
    """Helper function to redirect to login page and clear access token."""
    redirect_response = RedirectResponse(
        url='/auth/login-page',
        status_code=status.HTTP_302_FOUND
    )
    redirect_response.delete_cookie(key='access_token')
    return redirect_response


def _today_label() -> str:
    return datetime.now(tz=ROUTER_TIMEZONE).strftime("%A, %d %B %Y")


@router.get('/todo-page')
async def render_todo_page(request: Request):
    """Render the main todos page with user's todos."""
    try:
        user = await get_current_user(request)
        if user is None:
            return redirect_to_login()

        todos = await Todo.find(
            Todo.owner_id == user.get("id")
        ).sort(-Todo.created_at).to_list()

        return templates.TemplateResponse(
            'todo.html',
            {
                'request': request,
                'todos': todos,
                'user': user,
                'today_date': _today_label()
            }
        )
    except:
        return redirect_to_login()


@router.get('/add-todo-page')
async def render_add_todo_page(request: Request):
    """Render the add todo page."""
    try:
        user = await get_current_user(request)

        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse(
            'add-todo.html',
            {'request': request, 'user': user}
        )

    except:
        return redirect_to_login()


@router.get('/edit-todo-page/{todo_id}')
async def render_edit_todo_page(request: Request, todo_id: str):
    """Render the edit todo page."""
    try:
        user = await get_current_user(request)

        if user is None:
            return redirect_to_login()

        todo = await Todo.get(PydanticObjectId(todo_id))

        return templates.TemplateResponse(
            'edit-todo.html',
            {"request": request, "todo": todo, "user": user}
        )

    except:
        return redirect_to_login()


# ============================================================================
# API Endpoints
# ============================================================================

@router.get('/')
async def read_all(user: UserDependency):
    """Get all todos for the current user."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
    return await Todo.find(Todo.owner_id == user.get('id')).to_list()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: UserDependency, todo_id: str = Path()):
    """Get a specific todo by ID."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
    
    todo_model = await Todo.get(PydanticObjectId(todo_id))
    
    if todo_model is not None and todo_model.owner_id == user.get('id'):
        return todo_model
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Todo not found'
    )


@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(user: UserDependency, todo_request: TodoRequest):
    """Create a new todo."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
    
    todo_model = Todo(**todo_request.model_dump(), owner_id=user.get('id'))
    if todo_request.complete:
        todo_model.completed_at = datetime.utcnow()
    await todo_model.insert()
    return todo_model


@router.put('/todo/update_todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: UserDependency, todo_id: str, todo_request: TodoRequest):
    """Update an existing todo."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
    
    todo_model = await Todo.get(PydanticObjectId(todo_id))
    
    if todo_model is None or todo_model.owner_id != user.get('id'):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Todo not found'
        )

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    previously_complete = todo_model.complete
    todo_model.complete = todo_request.complete

    if todo_request.complete and not previously_complete:
        todo_model.completed_at = datetime.utcnow()
    elif not todo_request.complete:
        todo_model.completed_at = None

    await todo_model.save()


@router.delete('/todo/delete-todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: UserDependency, todo_id: str):
    """Delete a todo."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )
    
    todo_model = await Todo.get(PydanticObjectId(todo_id))
    
    if todo_model is None or todo_model.owner_id != user.get('id'):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Todo not found'
        )

    await todo_model.delete()
