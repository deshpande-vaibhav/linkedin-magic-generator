from fastapi import FastAPI, HTTPException, Form, File, UploadFile
from pydantic import BaseModel
from typing import Optional
import shutil
import os
from ai_logic import generate_comment, generate_caption, analyze_media
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LinkedIn Comment Generator")

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "LinkedIn Comment Generator API is running. Please open index.html in your browser."}

class CommentRequest(BaseModel):
    post_caption: str
    post_link: Optional[str] = ""
    profile_link: Optional[str] = ""
    tone: str
    model: Optional[str] = "mistral-large-latest"

class CommentResponse(BaseModel):
    comment: str

class CaptionRequest(BaseModel):
    thoughts: str
    profile_link: Optional[str] = ""
    image_video_desc: Optional[str] = ""
    model: Optional[str] = "mistral-large-latest"

class CaptionResponse(BaseModel):
    caption: str

@app.post("/generate", response_model=CommentResponse)
async def handle_generate(request: CommentRequest):
    if not request.post_caption:
        raise HTTPException(status_code=400, detail="Post caption is required")
    
    comment = await generate_comment(
        request.post_caption,
        request.post_link,
        request.profile_link,
        request.tone,
        request.model
    )
    
    return CommentResponse(comment=comment)

@app.post("/generate_caption", response_model=CaptionResponse)
async def handle_generate_caption(
    thoughts: str = Form(...),
    profile_link: Optional[str] = Form(""),
    media_url: Optional[str] = Form(""),
    media_file: Optional[UploadFile] = File(None),
    model: Optional[str] = Form("mistral-large-latest")
):
    if not thoughts:
        raise HTTPException(status_code=400, detail="Thoughts are required for caption generation")
    
    analyzed_media_desc = ""
    
    # 1. Handle File Upload
    if media_file and media_file.filename:
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, media_file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(media_file.file, buffer)
        
        # Analyze the file
        analyzed_media_desc = await analyze_media(file_path=file_path)
        
        # Clean up
        os.remove(file_path)
    
    # 2. Handle Media URL (if no file was uploaded or as fallback)
    elif media_url:
        analyzed_media_desc = await analyze_media(media_url=media_url)

    # 3. Generate Caption
    caption = await generate_caption(
        thoughts,
        profile_link,
        analyzed_media_desc or "",
        model
    )
    
    return CaptionResponse(caption=caption)

if __name__ == "__main__":
    import uvicorn
    # Respect PORT environment variable for deployment (e.g., Render)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
