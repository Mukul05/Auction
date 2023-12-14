import os
import smtplib
from email.mime.text import MIMEText

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
                return RedirectResponse(url="/admin_home", status_code=303)
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
def logout(request: Request):
    response = RedirectResponse(url="/login", status_code=303)
    request.session.clear()
    return response

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
        sold_item_details = db.fetch_sold_item_details(item_id)
        if sold_item_details:
            return templates.TemplateResponse("item_sold.html", {
                "request": request,
                "item": sold_item_details
            })
        else:
            # Handle the case where sold item details are not available
            # Redirect or display an error message as needed
            pass

    return templates.TemplateResponse("view_bid.html", {"request": request, "bids": bids, "item": item_details})

@app.post("/mark_item_sold/{item_id}")
async def mark_item_sold(request: Request, item_id: int):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    highest_bid = db.fetch_highest_bid_for_item(item_id)
    if highest_bid:
        db.mark_item_as_sold(item_id, highest_bid['user_id'], highest_bid['sold_price'])
        message = "Item marked as sold."
    else:
        message = "No bids placed on this item. Cannot mark as sold."

    return RedirectResponse(url="/seller_home", status_code=303)

    # Redirect back to seller_home with a message
    response = RedirectResponse(url="/seller_home", status_code=303)
    response.set_cookie(key="message", value=message)
    return response

@app.get("/buyer_home", response_class=HTMLResponse)
async def buyer_home(request: Request):
    user_id = request.session.get('user_id')
    if user_id:
        buyer_details = db.get_user_details(user_id)  # Make sure this method returns the correct details
        buyer_name = buyer_details['name'] if buyer_details else 'Unknown Buyer'
        items = db.fetch_available_auction_items()
        return templates.TemplateResponse("buyer_home.html", {
            "request": request,
            "items": items,
            "buyer_name": buyer_name  # Passing buyer_name to the template
        })
    else:
        return RedirectResponse(url="/login")


@app.post("/submit_bid/{item_id}")
async def submit_bid(request: Request, item_id: int, bid_amount: float = Form(...)):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    item = db.fetch_item_details(item_id)
    highest_bid = db.fetch_highest_bid_for_item(item_id)
    highest_bid_amount = highest_bid['sold_price'] if highest_bid else 0

    if not item or bid_amount < item['min_bid'] or item['end_time'] < datetime.now() or bid_amount <= highest_bid_amount:
        # Handle invalid bid scenario
        response = RedirectResponse(url="/place_bid/" + str(item_id), status_code=303)
        response.set_cookie(key="message", value="Please place a higher bid.")
        return response

    db.submit_bid(item_id, user_id, bid_amount)

    # Email Notification Logic
    try:
        send_email_notifications(item_id, item['item_name'], bid_amount)
    except Exception as e:
        print(f"Failed to send email notifications: {e}")

    return RedirectResponse(url="/buyer_home", status_code=303)

@app.get("/place_bid/{item_id}", response_class=HTMLResponse)
async def place_bid(request: Request, item_id: int):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    # Fetch item details
    item_details = db.fetch_item_details(item_id)
    if not item_details:
        return RedirectResponse(url="/buyer_home", status_code=303)

    # Fetch bids for the item
    bids = db.fetch_bids_for_seller(item_id)

    # Transform bids data to include bidder name or other necessary information
    bids_data = []
    for bid in bids:
        bid_info = {
            'amount': bid['amount'],
            'bidder_name': bid['bidder_name'],  # or fetch the bidder's name if needed
        }
        bids_data.append(bid_info)


    highest_bid = db.fetch_highest_bid_for_item(item_id)
    highest_bid_amount = highest_bid.get('amount') if highest_bid else 0  # Use .get() to safely access 'amount'

    return templates.TemplateResponse("place_bid.html", {
        "request": request,
        "item": item_details,
        "bids": bids_data,
        "highest_bid_amount": highest_bid_amount  # Pass this to the template
    })

@app.post("/delete_item/{item_id}")
async def delete_item(request: Request, item_id: int):
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    db.delete_auction_item(item_id)
    return RedirectResponse(url="/seller_home", status_code=303)

@app.get("/admin_home", response_class=HTMLResponse)
async def admin_home(request: Request):
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')

    if not user_id or user_type != 'admin':
        return RedirectResponse(url="/login")

    all_items = db.fetch_all_items_with_sellers()  # This method needs to be implemented in the Database class
    current_time = datetime.now()

    return templates.TemplateResponse("admin_home.html", {
        "request": request,
        "items": all_items,
        "current_time": current_time
    })

def send_email_notifications(item_id, item_name, bid_amount):
    # Fetch the seller and all bidders' emails
    seller_and_bidders_emails = db.fetch_emails_for_notification(item_id)
    for email in seller_and_bidders_emails:
        send_email(email, item_name, bid_amount)


def send_email(email, item_name, bid_amount):

    print("send email called for emailid",email)
    print("item name", item_name)
    print(bid_amount, bid_amount)

