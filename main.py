from fastapi import FastAPI, Request, HTTPException
import tempfile
from pathlib import Path
from markitdown import MarkItDown

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from OllamaMarkItToOpenWebUI"}

@app.put("/process")
async def process(request: Request):
    data: bytes = await request.body()
    fname = request.headers.get('X-Filename')
    ct = request.headers.get('Content-Type')

    md = MarkItDown()
    ok_result = {"page_content": "", "metadata": {}}

    is_bad = False
    bring_e = None
    try:
        with tempfile.TemporaryDirectory() as tmpd:
            with open(Path(tmpd) / fname, 'wb') as f:
                f.write(data)
            transcribed = md.convert(Path(tmpd) / fname)
            ok_result["page_content"] = transcribed.text_content
    except Exception as e:
        is_bad=True
        bring_e=e

    if not is_bad:
        return ok_result
    else:
        raise HTTPException(status_code=500, detail=str(e))
