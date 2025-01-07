from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mounting static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Data for your resume
resume_data = {
    "name": "Michael Fedorovsky מיכאל פדורובסקי",
    "title": "Software Developer",
    "email": "your@email.com",
    "phone": "123-456-7890",
    "summary": "A brief summary of your skills and experience.",
    "experience": [
        {"position": "Software Engineer", "company": "ABC Corp", "year": "2018-2022"},
        {"position": "Web Developer", "company": "XYZ Inc", "year": "2016-2018"}
    ],
    "education": [
        {"degree": "Bachelor of Science in Computer Science", "university": "University of ABC", "year": "2012-2016"}
    ]
}

# Define routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "resume": resume_data})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
