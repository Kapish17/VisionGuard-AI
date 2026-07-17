from pathlib import Path
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.detector import detect_objects

print("===================================")
print("VisionGuard AI Backend Started")
print("Running file:", Path(__file__).resolve())
print("===================================")

app = FastAPI(title="VisionGuard AI")

# ----------------------------
# CORS
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Folders
# ----------------------------
UPLOAD_FOLDER = Path("uploads")
OUTPUT_FOLDER = Path("outputs")

UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

# ----------------------------
# Static Files
# ----------------------------
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")


# ----------------------------
# Routes
# ----------------------------
@app.get("/")
def home():
    return {
        "message": "VisionGuard AI Backend Running"
    }


@app.get("/api/test")
def test():
    return {
        "status": "Backend Connected Successfully"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ----------------------------
# Upload Video
# ----------------------------
@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    try:

        # Save uploaded video
        save_path = UPLOAD_FOLDER / file.filename

        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"Video Uploaded: {save_path}")

        # Run Detection
        result = detect_objects(str(save_path))

        processed_path = result["video_path"]
        summary = result["summary"]

        processed_name = Path(processed_path).name

        print(f"Processed Video: {processed_path}")

        return {
            "success": True,
            "filename": file.filename,
            "message": "Video uploaded and processed successfully",

            "original_video":
                f"http://127.0.0.1:8000/uploads/{file.filename}",

            "processed_video":
                f"http://127.0.0.1:8000/outputs/{processed_name}",

            "summary": summary
        }

    except Exception as e:
        import traceback

        print("\n========== ERROR ==========")
        traceback.print_exc()
        print("===========================\n")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )