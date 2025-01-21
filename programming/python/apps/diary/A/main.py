# main.py
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize SQLite database and create table
conn = sqlite3.connect('diary.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS entries
             (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, entry TEXT)''')
conn.commit()
conn.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    conn = sqlite3.connect('diary.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM entries ORDER BY id DESC''')
    entries = c.fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "entries": entries})

@app.post("/add_entry/")
async def add_entry(request: Request, entry: str = Form(...)):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('diary.db')
    c = conn.cursor()
    c.execute('''INSERT INTO entries (timestamp, entry) VALUES (?, ?)''', (timestamp, entry))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/")

@app.post("/delete_entry/{entry_id}/")
async def delete_entry(entry_id: int):
    conn = sqlite3.connect('diary.db')
    c = conn.cursor()
    c.execute('''DELETE FROM entries WHERE id = ?''', (entry_id,))
    conn.commit()
    conn.close()
    return {"message": "Entry deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

