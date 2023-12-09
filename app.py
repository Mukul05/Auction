from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from utils.utils import *
import typer
import uvicorn
from datetime import datetime


import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database specified by the db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def execute_query(conn, query):
    """ Execute a single query """
    try:
        c = conn.cursor()
        c.execute(query)
    except Error as e:
        print(e)
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8000
app = FastAPI()

# Create users table
conn = create_connection('users.db')
execute_query(conn, " CREATE TABLE IF NOT EXISTS users ( id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL);")
conn.close()

# Define the path to your templates directory
templates = Jinja2Templates(directory="templates")

ACTIVE_USER = []
USER_DB = [{"username": "user1", "password": "123456"}, {"username": "user2", "password": "654321"}]
AUCTION_ITEMS = [
    {
        "id": 1,
        "name": "Watch",
        "url": "data:image/png;base64,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",
        "auction_price": "100",
        "bids": [
            {
                "username": "sample",
                "bid_value": "",
                "timestamp": ""
            }
        ]
    },
    {
        "id": 2,
        "name": "Watch",
        "url": "img",
        "auction_price": "100"
    },
    {
        "id": 3,
        "name": "Watch",
        "url": "img",
        "auction_price": "100"
    }
]


@app.get("/")
async def main_page(request: Request):
    return RedirectResponse('/login', status_code=303)


# Define a simple route that renders an HTML template
@app.get("/login", response_class=HTMLResponse)
async def read_root(request: Request):
    # You can pass variables to the template using the context dictionary
    context = {"request": request, "message": "Hello, FastAPI with HTML templates!"}

    # Render the HTML template using Jinja2
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/login')
async def perform_login(request: Request, login_type: str = Form(...), username: str = Form(...),
                        password: str = Form(...)):
    if login_type == 'admin':
        print("sample")
        if username.lower() == 'admin' and password.lower() == 'admin123':
            # return {"sample"}
            return RedirectResponse("/admin_home", status_code=303)
            # return templates.TemplateResponse("admin_home.html",{"username":username})
        else:
            return RedirectResponse("/login_error", status_code=303)
    elif login_type == 'client':
        if authorize_user(USER_DB, username, password):
            ACTIVE_USER = username

            response = RedirectResponse("/client_home", status_code=303)
            response.set_cookie(key="username", value=username)
            return response
        else:
            return RedirectResponse("/login_error", status_code=303)


@app.get('/register', response_class=HTMLResponse)
async def register_client(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post('/register')
async def register_client_save(request: Request, username: str = Form(...), password: str = Form(...)):
    USER_DB.append({
        "username": username.lower(),
        "password": password,
    })
    return RedirectResponse("/login", status_code=303)


@app.post("/place_bid")
async def place_bid(request: Request, index: str = Form(...), bid_value: str = Form(...)):
    print(index)
    if "bids" not in AUCTION_ITEMS[int(index)]:
        AUCTION_ITEMS[int(index)]['bids'] = []
    bid_data = {
        "username": ACTIVE_USER,
        "bid_value": bid_value,
        "timestamp": datetime.now()
    }

    AUCTION_ITEMS[int(index)]['bids'].append(bid_data)

    return RedirectResponse(f"/item_page/?index={index}", status_code=303)


@app.post('/add_item')
async def add_item(request: Request, item_name: str = Form(...), item_price: str = Form(...),
                   item_url: str = Form(...)):
    add_item_to_auction_list(AUCTION_ITEMS, {"name": item_name, "auction_price": item_price, "url": item_url})

    return RedirectResponse("/admin_home", status_code=303)


@app.post("/remove_auction_item")
async def remove_auction_item(request: Request, id: str = Form(...)):
    remove_auction_item_by_id(AUCTION_ITEMS, id)
    return RedirectResponse('/admin_home', status_code=303)


@app.post('/item_page')
async def redirect_item_page(request: Request, id: str = Form(...)):
    index = find_auction_item(AUCTION_ITEMS, id)
    return RedirectResponse(f"/item_page/?index={index}", status_code=303)


@app.get('/item_page', response_class=HTMLResponse)
async def get_item_page(request: Request):
    index = request.query_params.get("index")
    print(index)
    item = AUCTION_ITEMS[int(index)]
    print(index)
    return templates.TemplateResponse(f"/item_page.html",
                                      {"request": request, "username": ACTIVE_USER, "index": index, **item})


@app.get("/login_error", response_class=HTMLResponse)
async def login_error(request: Request):
    return templates.TemplateResponse("login_error.html", {"request": request})


@app.get("/admin_home", response_class=HTMLResponse)
async def admin_home(request: Request):
    return templates.TemplateResponse("admin_home.html", {"request": request, "auction_items": AUCTION_ITEMS})


@app.get("/client_home", response_class=HTMLResponse)
async def client_home(request: Request):
    print(ACTIVE_USER)
    return templates.TemplateResponse("client_home.html",
                                      {"request": request, "auction_items": AUCTION_ITEMS, "username": ACTIVE_USER})


def main(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    typer.run(main)