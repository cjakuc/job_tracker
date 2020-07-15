import secrets
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os
from fastapi import FastAPI, Request, status, Depends, HTTPException, APIRouter

router = APIRouter()

load_dotenv()

num_users = os.getenv("NUMBER_OF_USERS", default="OOPS")
users_list = [os.getenv(f"USER{x}") for x in range(int(num_users))]
passwords_list = [os.getenv(f"USER{x}_PASSWORD") for x in range(int(num_users))]

templates = Jinja2Templates(directory="templates")

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    """[summary]

    Parameters
    ----------
    credentials : HTTPBasicCredentials, optional
        [description], by default Depends(security)

    Returns
    -------
    [type]
        [description]

    Raises
    ------
    HTTPException
        [description]
    """
    # Boolean to see if the username is correct
    is_username = False
    # Counter for which username is correct
    which_name = 0
    for name in users_list:
        correct_username = secrets.compare_digest(credentials.username, name)
        # Check if the username is one of the options
        if correct_username:
            is_username = True
            break
        which_name += 1

    correct_password = secrets.compare_digest(credentials.password, passwords_list[which_name])
    # Check if both the username and password are correct
    if not (is_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Simple test homepage
@router.get("/")
def root(request: Request,
         username: str = Depends(get_current_username)):
    return templates.TemplateResponse("homepage.html",
                                      {'request': request})