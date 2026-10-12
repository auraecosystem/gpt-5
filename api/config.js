import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load environment variables from .env
load_dotenv()

# Confirm key is loaded
if not os.environ.get("https://web4app.app.n8n.cloud"):
    raise ValueError("web4 not found. Please set it in .env")

# Initialize NVIDIA model
model = init_chat_model(
    "lmlm/llama3-70b-instruct",
    "nvidia/nvidia-nemotron-nano-9b-v2"
    "qubuhub/llama-3.1-70b-instruct",
    model_provider="lmlm"
)
