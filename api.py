from app import supabase
from app import app 

@app.get("/")
def home():
    return {"mesage" : "inventory"}

@app.get("/grouped")
def grouped():
    res = (supabase.table("categories")
           .select("name, items(id, name, in_stock)")
           .order("name")
           .execute()
    )

    return res.data