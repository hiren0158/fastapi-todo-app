from fastapi import APIRouter,Depends, HTTPException, Request
from pydantic import BaseModel
from ..models_beanie import User
from ..config import settings
from passlib.context import CryptContext 
from typing import Annotated, Optional
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import timedelta,datetime,timezone
from fastapi.templating import Jinja2Templates
from beanie import PydanticObjectId
from starlette.responses import RedirectResponse, JSONResponse
from beanie.operators import Or

router=APIRouter(
       prefix='/auth',
       tags=['auth'] 
)

SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token', auto_error=False)

class Token(BaseModel):
    access_token:str
    token_type:str

templates = Jinja2Templates(directory="ToDoApp2/templates")

# pages
@router.get('/login-page')
def render_login_page(request:Request):
    return templates.TemplateResponse('login.html',{'request':request})

@router.get('/register-page')
def render_register_page(request:Request):
    return templates.TemplateResponse('register.html',{'request':request})
#endpoints

def authenticate_user(username:str,password:str):
    user: User|None = None
    # lookup by username
    user = User.find_one({"username": username}).run_sync()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user

def create_access_token(username:str,user_id:str,role:str,expires_delta:timedelta):
    encode={'sub':username,'id':user_id,'role':role}
    expires=datetime.now(timezone.utc)+ expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

async def get_current_user(request: Request, token: Annotated[Optional[str],Depends(oauth2_bearer)]=None):
    try:
         # Fallback to cookie if no Authorization header token present
         if not token:
            token = request.cookies.get('access_token')
         if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate user')
         payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
         username:str=payload.get('sub')
         user_id:str=payload.get('id')
         user_role:str=payload.get('role')
         if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate user')
         return{'username':username,'id':user_id,'user_role':user_role}
    except JWTError:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate user')
         
class CreateUserRequest(BaseModel):
    username:str
    email:str   
    firstname:str
    lastname:str
    # phone_number:str
    password:str
    role:str

@router.post('/',status_code=status.HTTP_201_CREATED)
async def create_user(request: Request):
    content_type = request.headers.get('content-type','')
    if 'application/x-www-form-urlencoded' in content_type or 'multipart/form-data' in content_type:
        form = await request.form()
        payload = CreateUserRequest(
            username=form.get('username',''),
            email=form.get('email',''),
            firstname=form.get('firstname',''),
            lastname=form.get('lastname',''),
            password=form.get('password',''),
            role=form.get('role','')
        )
    else:
        data = await request.json()
        payload = CreateUserRequest(**data)

    existing = await User.find_one({"$or": [{"username": payload.username}, {"email": payload.email}]})
    if existing:
        if 'application/json' in content_type:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already exists")
        return templates.TemplateResponse('register.html',{'request':request, 'error': 'Username or email already exists'}, status_code=status.HTTP_400_BAD_REQUEST)

    create_user_model=User(
        email=payload.email,
        username=payload.username,
        first_name=payload.firstname,
        last_name=payload.lastname,
        # phone_number=payload.phone_number,
        role=payload.role,
    hashed_password=bcrypt_context.hash(payload.password),      
        is_active=True
    )
    await create_user_model.insert()

    if 'application/json' in content_type:
        return JSONResponse({"id": str(create_user_model.id), "username": create_user_model.username}, status_code=status.HTTP_201_CREATED)
    # HTML form: redirect to login page with a flash-like success message via query param
    return RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)

@router.post('/token',response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()]):
    user=await User.find_one({"username": form_data.username})
    if not user or not bcrypt_context.verify(form_data.password,user.hashed_password):
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate user')
    token=create_access_token(user.username,str(user.id),user.role,timedelta(minutes=20))
    return {'access_token':token, 'token_type':'bearer'}

@router.post('/logout')
async def logout():
    response = RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key='access_token', path='/')
    return response

