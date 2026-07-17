from pathlib import Path
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

print("===================================")
print("VisionGuard AI Backend Started")
print("Running file:", Path(__file__).resolve())
print("===================================")

app = FastAPI(title="VisionGuard AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "THIS IS THE NEW BACKEND",
        "upload_folder": str(UPLOAD_FOLDER.resolve())
    }


@app.get("/api/test")
def test():
    return {
        "status": "Backend Connected Successfully"
    }


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    try:
        save_path = UPLOAD_FOLDER / file.filename

        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "success": True,
            "filename": file.filename,
            "message": "Video uploaded successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/uploads")
def list_uploads():
    files = [f.name for f in UPLOAD_FOLDER.iterdir() if f.is_file()]
    return {"files": files}