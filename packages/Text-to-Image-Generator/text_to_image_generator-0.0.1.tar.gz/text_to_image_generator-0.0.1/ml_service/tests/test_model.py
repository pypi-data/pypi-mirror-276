import pytest
import os
from fastapi.testclient import TestClient
from ml_service.app.main import app
from ml_service.app.model import generate_image
#
# client = TestClient(app)
#
#
# def test_server_is_up():
#     response = client.get("/")
#     assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    # assert response.json() == {"Hello, World!"}

# def test_generate_image_endpoint():
#     response = client.post("/generate-image/", json={"text": "space pig"})
#     assert response.status_code == 200
#     assert "image_path" in response.json()

# @pytest.mark.asyncio
# async def test_generate_image():
#     text = "space pig"
#     image_path = await generate_image(text)
#     assert os.path.exists(image_path)
# assert image_path == f"generated_images/{text.replace(' ', '_')}.png"
