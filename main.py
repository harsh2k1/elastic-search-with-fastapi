from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import pandas as pd

app = FastAPI()

templates = Jinja2Templates(directory="templates")

df = pd.read_csv('data/collegeData.csv')
cities = list(df["city"].unique())
courseNames = list(df['courseName'])
courseNames = list(map(lambda z: str(z).replace(" ","_"), courseNames))
df['courseNames2'] = courseNames
courseNames = list(df['courseNames2'].unique())

@app.get('/',response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/{name}/',response_class=HTMLResponse)
async def home(request: Request, name:str):
    return templates.TemplateResponse("index.html", {"request": request, "name":name})

@app.get('/dropdown', response_class=HTMLResponse)
async def render_dropdown(request:Request):
    
    context = {"request":request, "cities":cities, "courseNames":courseNames}
    return templates.TemplateResponse("dropdown_demo.html", context)

@app.post("/upload", response_class=HTMLResponse)
async def handle_form(request:Request,
                      cities_choice:str=Form(...),
                      course_choice:str=Form(...)):
    df1 = df[df['city'] == cities_choice]
    df1 = df1[df1['courseNames2']==course_choice]
    
    context = {"request":request, "results":df1}
    if len(list(df1['fullName'])):
        return templates.TemplateResponse("display_table.html", context)
    else:
        return JSONResponse(
            status_code=401,
            content={
                "message":"No Results found"
            }
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True)