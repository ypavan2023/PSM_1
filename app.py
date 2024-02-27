import uvicorn
from fastapi import FastAPI,Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import StreamingResponse
import cv2
import pickle
import numpy as np
import os
import psycopg2
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from main import management,check,gen_frames,updatedValues1,updatedValues2


from flask import  Flask,render_template,request,jsonify

from chat import get_response

load_dotenv('.env')

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="postgres",
    port=os.getenv("DATABASE_PORT")
)



app = FastAPI()
app.mount("/static", StaticFiles(directory = "static"), name = "static")
templates = Jinja2Templates(directory="templates")




@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("open.html", {"request": request})

@app.get("/sign")
def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/sign")
async def signup(
    request: Request, username: str = Form(...), email: str = Form(...),password1: str = Form(...),password2:str = Form(...) 
):
   
    cur = conn.cursor()
    cur.execute("INSERT INTO users1 (uname,email,password1,password2) VALUES (%s, %s,%s, %s)", (username,email,password1,password2))
    conn.commit()
    cur.close() 
 
    return RedirectResponse("/login", status_code=303)

@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def do_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users1 WHERE uname=%s and password1=%s", (username,password))
    existing_user = cur.fetchone()
    cur.close()
    
    if existing_user:
        print(existing_user)
        return RedirectResponse("/map", status_code=303)
    
    else:
        return JSONResponse(status_code=401, content={"message": "Wrong credentials"})


    
@app.get("/home")
def homepage(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/map")
def homepage(request: Request):
    return templates.TemplateResponse("map.html", {"request": request})

@app.get("/home")
def homepage(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/profile")
def homepage(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})


# @app.get("/login", response_class=HTMLResponse)
# def login(request: dict):
#     return templates.TemplateResponse("login.html", {"request": request})


@app.post("/predict")
def predict():
    text=request.get_json().get("message")
    response=get_response(text)
    message={"answer":response}
    return jsonify(message)


@app.get('/video_feed1')
def video_feed1():
    return StreamingResponse(management("recording.mp4","CarPosition",10), media_type='multipart/x-mixed-replace; boundary=frame')
@app.get('/video_feed2')
def video_feed2():
    return StreamingResponse(management("CMR_bike.mp4","bikepickle",4), media_type='multipart/x-mixed-replace; boundary=frame')
@app.get('/value1')
def values1():
    data = {"value":updatedValues1()}
    return JSONResponse(content=data)
@app.get('/value2')
def values2():
    data = {"value":updatedValues2()}
    return JSONResponse(content=data)

if __name__ == '__main__':
   uvicorn.run(app, host='0.0.0.0', port=8000)