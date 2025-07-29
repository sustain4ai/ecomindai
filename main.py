import uvicorn
from fastapi import FastAPI
import gradio as gr
from src.interface.interface import io
from src.routers.resources import aiImpacts
import os

print("Launching EcoMindAI v2 application")

app = FastAPI()
app.include_router(aiImpacts.router)
app = gr.mount_gradio_app(app, io, path="/")

host = os.environ.get("ECOMINDAI_SERVER_HOST", "0.0.0.0")
port = int(os.environ.get("ECOMINDAI_SERVER_PORT", "8000"))
uvicorn.run(app, host=host, port=port)
