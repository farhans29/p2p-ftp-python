from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.responses import FileResponse
from pathlib import Path
import os
import shutil
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory=Path(__file__).parent.absolute() / "static"), name="static",)

@app.get("/")
async def home(request: Request):
    files = os.listdir("uploads/")
    return templates.TemplateResponse("index.html", {"request": request, "files": files})


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Redirect to the home page after uploading the file
    return RedirectResponse(url="/", status_code=302)

@app.get("/downloadfile/{filename}")
async def download_file(filename: str):
    file_path = f"uploads/{filename}"
    return FileResponse(file_path)

@app.get("/listfiles/")
async def list_files():
    files = os.listdir("uploads/")
    return {"files": files}

@app.get("/sharefile/{filename}/{target_ip}")
async def share_file(filename: str, target_ip: str):
    file_path = f"uploads/{filename}"
    return {"message": f"File {filename} has been shared with {target_ip}"}

def create_app():
    os.makedirs("uploads", exist_ok=True)
    return app

if __name__ == '__main__':
    uvicorn.run("app:create_app", host="127.0.0.1", port=8000, reload=True)
