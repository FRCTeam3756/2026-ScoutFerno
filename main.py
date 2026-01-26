from io import BytesIO
from fastapi import FastAPI
from PIL import Image
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"health ok... OR IS IT", "fine..."}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    img = Image.open(file_path)
    
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return StreamingResponse(buffer, media_type="image/png")
