import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from model.create_plots_data import create_barplot_data, create_wordcloud_data

app = FastAPI()
templates = Jinja2Templates(directory="src/view/")

origins = [
    "http://localhost:3000",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def dashboard_page(request: Request):
    name_data = create_barplot_data()
    word_data = create_wordcloud_data()
    return templates.TemplateResponse("index.html", context={"request": request})


@app.get("/words")
async def update_wordcloud():
    word_data = create_wordcloud_data()
    return word_data


@app.get("/names")
async def update_barchart():
    name_data = create_barplot_data()
    return name_data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
