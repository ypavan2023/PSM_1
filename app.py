import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import StreamingResponse
import cv2
import pickle
import numpy as np
import os
from dotenv import load_dotenv
from main import management,check,gen_frames,updatedValues1,updatedValues2


from flask import  Flask,render_template,request,jsonify

from chat import get_response

load_dotenv('.env')
 
app = FastAPI()
app.mount("/static", StaticFiles(directory = "static"), name = "static")
templates = Jinja2Templates(directory="templates")






@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("open.html", {"request": request})

@app.get("/sign")
def login(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/sign")
def login(request: Request):
    # Process login logic here
    # Redirect to the homepage
    return RedirectResponse(url="/sign")


@app.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request):
    # Process login logic here
    # Redirect to the homepage
    return RedirectResponse(url="/home")

@app.get("/home")
def homepage(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


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