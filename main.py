from urllib import response
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get('/',response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/{name}/',response_class=HTMLResponse)
async def home(request: Request, name:str):
    return templates.TemplateResponse("index.html", {"request": request, "name":name})

@app.get('/dropdown', response_class=HTMLResponse)
async def render_dropdown(request:Request):
    dropdown_list = [
        {
            "id":1,
            "content":"HTML"
        },
        {
            "id":2,
            "content":"CSS"
        },
        {
            "id":3,
            "content":"JS"
        },
        {
            "id":4,
            "content":"Python"
        },
        {
            "id":5,
            "content":"Java"
        }
    ]
    
    context = {"request":request, "categories":dropdown_list}
    return templates.TemplateResponse("dropdown_demo.html", context)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True)