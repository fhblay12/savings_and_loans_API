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


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
