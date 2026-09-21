from fastapi import FastAPI
from supabase import create_client
from dotenv import load_dotenv
import os


load_dotenv()

app =  FastAPI()

supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

import api

