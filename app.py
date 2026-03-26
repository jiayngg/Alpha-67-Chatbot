"""
Main FastAPI application entry point for the chatbot backend.

This is the main entry point for running the application. It:
1. Loads environment variables
2. Creates the FastAPI app using the factory in api/app.py
3. Configures global middleware
4. Starts the server when run directly
"""

import socket

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from api import create_app
from src.common.config import Config
from src.common.logging import logger

# Load environment variables
load_dotenv()

# Create the FastAPI app using the factory function
app = create_app()

# Configure global CORS middleware
# This applies to all routes in the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

def find_available_port(start_port: int) -> int:
    for port in range(start_port, 8090):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", port)) != 0:
                return port
    raise RuntimeError("No available ports in range 8080-8089")


if __name__ == "__main__":
    # Load config
    config = Config()

    # Find an available port starting from configured port
    port = find_available_port(int(config.port))

    logger.info(f"Starting server on port {port}...")
    logger.info(f"API documentation available at http://localhost:{port}/docs")

    # Run the application with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
