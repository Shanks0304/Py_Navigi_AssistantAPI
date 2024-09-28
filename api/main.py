
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from pydantic import BaseModel
import uvicorn

from .app.utils.assistant import run_assistant

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/static", StaticFiles(directory="./data"), name="static")

# define the route:
@app.get("/", tags=["root"])
async def root():
    return {"message": "Hello World"}

class TextRequest(BaseModel):
    text: str

@app.post("/assistant_text", response_model=TextRequest)
async def assistant_text(request: TextRequest):
    input_text = request.text
    processed_text = run_assistant(input_text)
    response_data = {"result": processed_text}
    return JSONResponse(content=response_data)

# define the entry point. In the entry point, using uvicorn to run server
if __name__ == "__main__":
    uvicorn.run("app", host="0.0.0.0", port=8000, reload=True)