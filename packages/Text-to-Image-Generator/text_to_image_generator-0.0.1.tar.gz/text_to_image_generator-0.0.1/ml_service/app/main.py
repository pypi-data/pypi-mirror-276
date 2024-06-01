from pydantic import BaseModel

from .model import generate_image  # Ensure your model module is correctly imported

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# Adding CORS handling
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers
)

# Adding route for serving static files
app.mount("/generated_images", StaticFiles(directory="generated_images"), name="generated_images")


class InputText(BaseModel):
    text: str


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return {"request": request}


@app.post("/generate-image/")
async def generate_image_endpoint(input_text: InputText, response: Response):
    image_path = await generate_image(input_text.text)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return {"image_path": image_path}


if __name__ == "__main__":
    import uvicorn

    # Clearly specify that the service will run on localhost:8001
    uvicorn.run(app, host="127.0.0.1", port=80)
