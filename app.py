import uvicorn
from os import path
from fastapi import FastAPI
import gradio as gr
from src.interface.interface import io
from src.routers.resources import aiImpacts
import os

css_path = path.join(path.dirname(__file__), "./assets/styles/app.css")
with open(css_path, "r") as css_file:
    custom_css = css_file.read()
head_path = path.join(path.dirname(__file__),
                      "./assets/partials/head.html")

print("Launching EcoMindAI v2 application")

app = FastAPI()
app.include_router(aiImpacts.router)
app = gr.mount_gradio_app(app, io, path="", css=custom_css, head_paths=head_path )

host = os.environ.get("ECOMINDAI_SERVER_HOST", "127.0.0.1")
port = int(os.environ.get("ECOMINDAI_SERVER_PORT", "8000"))
uvicorn.run(app, host=host, port=port)
