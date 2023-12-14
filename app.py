import os

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
from fastapi.staticfiles import StaticFiles
from datetime import datetime

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
templates = Jinja2Templates(directory="templates")
db = Database()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return RedirectResponse(url="/login")


@app.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def post_register(request: Request, name: str = Form(...), email_id: str = Form(...), password: str = Form(...),
                        user_type: str = Form(...)):
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
        seller_details = db.get_user_details(seller_id)
        seller_name = seller_details['name'] if seller_details else 'Unknown Seller'
        current_time = datetime.now()  # Get the current time
        return templates.TemplateResponse("seller_home.html", {
            "request": request,
            "seller_items": seller_items,
            "seller_name": seller_name,
            "current_time": current_time  # Pass current_time to the template
        })
    else:
        return RedirectResponse(url="/login")


@app.post("/add_item")
async def add_item(request: Request, item_name: str = Form(...), start_time: str = Form(...), end_time: str = Form(...),
                   min_bid: float = Form(...), image: UploadFile = File(None), image_url: str = Form(None)):
    seller_id = request.session.get('user_id')  # Changed from request.state to request.session
    if not seller_id:
        return RedirectResponse(url="/login", status_code=303)

    image_path = await save_image(image) if image else image_url
    db.add_auction_item(seller_id, item_name, image_path, start_time, end_time, min_bid)
    return RedirectResponse(url="/seller_home", status_code=303)

async def save_image(image: UploadFile):
    try:
        if image:
            file_location = f"static/images/{image.filename}"
            os.makedirs(os.path.dirname(file_location), exist_ok=True)
            with open(file_location, "wb+") as file_object:
                file_object.write(await image.read())
            return file_location
        return None
    except Exception as e:
        print(f"Error saving image: {e}")
        return None  # Or handle the error

@app.get("/view_bid/{item_id}", response_class=HTMLResponse)
async def view_bid(request: Request, item_id: int):
    bids = db.fetch_bids_for_item(item_id)  # You need to implement this method in database.py
    item_details = db.fetch_item_details(item_id)  # Implement this method to get item details
    if item_details and item_details['is_sold']:
        # Handle the case where the item is already sold
        return templates.TemplateResponse("item_sold.html", {"request": request, "item": item_details})
    return templates.TemplateResponse("view_bid.html", {"request": request, "bids": bids, "item": item_details})

@app.post("/mark_item_sold/{item_id}")
async def mark_item_sold(request: Request, item_id: int):
    highest_bid = db.get_highest_bid_for_item(item_id)

    if highest_bid:
        buyer_id, sold_price = highest_bid['user_id'], highest_bid['sold_price']
        db.mark_item_as_sold(item_id, buyer_id, sold_price)
        message = "Item marked as sold."
    else:
        # No bids were placed on this item
        message = "No bids placed on this item. Cannot mark as sold."

    # Redirect back to seller_home with a message
    response = RedirectResponse(url="/seller_home", status_code=303)
    response.set_cookie(key="message", value=message)
    return response
