from fastapi import FastAPI, Request, Form, File, UploadFile, Depends
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import time
from fastapi.background import BackgroundTasks

app = FastAPI()

list_of_usernames = list()

templates = Jinja2Templates(directory="templates")

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

class NameValues(BaseModel):
    name: str
    country: str
    age: int
    salary: float


@app.post("/token")
async def token_generate(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    return {"access_token": form_data.username, "token_type": "bearer"}

@app.get("/users/profilepic")
async def profile_pic(token: str = Depends(oauth_scheme)):
    print(token)
    # print(profile_pic.filename)
    return {
        "user": "Pranjal",
        "profile_pic": "profile_pic.jpg"
    }



@app.get("/")
def home():
    return {"Hello World"}


@app.get("/home/{user_name}", response_class=HTMLResponse)
def write_home(request: Request, user_name: str):

    return templates.TemplateResponse("home.html", {"request": request, "user_name": user_name})



@app.post("/submitform")
async def handle_form(resume: str = Form(...), resume_file: UploadFile = File(...)):
    print(resume)
    content_resume = await resume_file.read()
    print(content_resume)


def send_email(email: str, data:str):
    print("Sending email to:", email)
    print("Email content:", data)
    for i in range(100):
        print(i)
        time.sleep(0.1)

@app.get("/users/email")
async def handle_email(email: str, background_tasks: BackgroundTasks):
    print(email)
    background_tasks.add_task(send_email, email, "This is the email content being handled in the background without blocking the main thread")  
    return {
        "user" : "Pranjal",
        "message": "Email sent successfully"
        }