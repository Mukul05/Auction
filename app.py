from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database import Database
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND, HTTP_401_UNAUTHORIZED
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
from starlette.datastructures import Secret

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
templates = Jinja2Templates(directory="templates")
db = Database()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return RedirectResponse(url="/login")

@app.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def post_register(request: Request, name: str = Form(...), email_id: str = Form(...), password: str = Form(...), user_type: str = Form(...)):
    db.create_user(name, email_id, password, user_type)
    return RedirectResponse(url="/", status_code=303)

# Additional routes will be implemented here
@app.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def post_login(request: Request, email_id: str = Form(...), password: str = Form(...)):
    user = db.read_user_by_email(email_id)
    try:
        user = db.read_user_by_email(email_id)
        if user and user['password'] == password:
        # Redirect to the respective user's page based on user type
            request.session['user_id'] = user['user_id']
            request.session['user_type'] = user['user_type']
            if user['user_type'] == 'buyer':
                return RedirectResponse(url="/buyer_home", status_code=303)
            elif user['user_type'] == 'seller':
                return RedirectResponse(url="/seller_home", status_code=303)
            elif user['user_type'] == 'admin':
                return RedirectResponse(url="/admin_console", status_code=303)
        else:
            return templates.TemplateResponse("login_error.html", {"request": request})
    except Exception as e:
        print(f"Error during login: {e}")

@app.post("/login")
async def login(request: Request, email_id: str = Form(...), password: str = Form(...)):
    user = db.read_user_by_email(email_id)
    if user and user['password'] == password:
        request.session['user_id'] = user['user_id']
        request.session['user_type'] = user['user_type']
        # Redirect to a user-specific page
        return RedirectResponse(url="/home", status_code=303)
    return templates.TemplateResponse("login_error.html", {"request": request})

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")

@app.get("/seller_home", response_class=HTMLResponse)
async def get_seller_home(request: Request):
    seller_id = request.session.get('user_id')
    if seller_id:
        seller_items = db.fetch_seller_items(seller_id)
        return templates.TemplateResponse("seller_home.html", {"request": request, "seller_items": seller_items})
    else:
        # Redirect the user to the login page or display an unauthorized access message
        # Option 1: Redirect to login page
        return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)

@app.post("/add_item")
async def add_item(request: Request, item_name: str = Form(...), start_time: str = Form(...), end_time: str = Form(...), min_bid: float = Form(...), image: UploadFile = File(None), image_url: str = Form(None)):
    seller_id = request.state.user_id  # Assuming you have the seller's ID
    image_path = await save_image(image) if image else image_url  # Implement save_image function

    db.add_auction_item(seller_id, item_name, image_path, start_time, end_time, min_bid)
    return templates.TemplateResponse("seller_home.html", {"request": request, "message": "Item added successfully"})

async def save_image(image: UploadFile):
    file_location = f"static/images/{image.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(image.file.read())
    return file_location

@app.get("/view_bid/{item_id}", response_class=HTMLResponse)
async def view_bid(request: Request, item_id: int):
    bids = db.fetch_bids_for_item(item_id)  # You need to implement this method in database.py
    item_details = db.fetch_item_details(item_id)  # Implement this method to get item details
    return templates.TemplateResponse("view_bid.html", {"request": request, "bids": bids, "item": item_details})




