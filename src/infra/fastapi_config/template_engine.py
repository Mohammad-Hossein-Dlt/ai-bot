import os
from fastapi.templating import Jinja2Templates

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if "/app" in BASE_DIR:
    templates = Jinja2Templates(directory="./templates")
else:
    templates = Jinja2Templates(directory="./templates")
