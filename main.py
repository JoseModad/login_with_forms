from fastapi import FastAPI, Request, Form, Depends, status
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from db.database import engine, Base, get_db
from sqlalchemy.orm import Session
from db import models
from passlib.context import CryptContext
from hashing import Hash
from fastapi import HTTPException
from schemas import Login, User
from repository import auth
from oauth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def create_tables():
#     Base.metadata.create_all(bind=engine)
    
# create_tables()


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Crear base de datos
# @app.get("/", response_class=HTMLResponse)
# async def index(request:  Request, db: Session = Depends(get_db)):
#     data = db.query(models.User).all()
#     print(data)
#     return templates.TemplateResponse("index.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
async def index(request:  Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def index(request:  Request):
	return templates.TemplateResponse("index.html", {"request": request})


@app.post("/login", status_code=status.HTTP_200_OK)
async def loguin(usuario : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    autenticacion = auth.auth_user(usuario, db)
    return autenticacion


@app.get("/usuarios", response_class=HTMLResponse)
async def usuarios(request:  Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = db.query(models.User).all()
    for user in data:
        print(user.username, user.password_user, user.firstname, user.lastname, user.country)        
    return templates.TemplateResponse("usuarios.html", {"request": request, "data": data})


@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
	return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup", response_class=HTMLResponse)
async def signup(username: str = Form(...), password_user: str = Form(...), firstname: str = Form(...), lastname: str = Form(...), country: str = Form(...), db: Session = Depends(get_db)):
    password_hash = Hash.hash_password(password_user)
    nuevo_usuario = models.User(
        username=username, 
        password_user=password_hash, 
        firstname=firstname, 
        lastname=lastname, 
        country=country
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return RedirectResponse(url="/")


@app.post("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request}) 

   

if __name__ == "__main__":
    uvicorn.run('main:app', port=8000, reload=True)