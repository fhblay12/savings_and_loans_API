import csv
import io
from datetime import datetime
from fastapi import FastAPI, Form, Request, UploadFile, File, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import StreamingResponse
import plotly.io as pio
from fastapi.responses import JSONResponse
import secrets
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from routers import customer
from database import engine, Base

app = FastAPI()


Base.metadata.create_all(bind=engine)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(customer.router)
