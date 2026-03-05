from fastapi import FastAPI
from models import Notebook

app = FastAPI(title="Notes API")
notebook = Notebook()
