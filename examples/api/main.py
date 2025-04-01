import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from routes import router

# Create FastAPI app
app = FastAPI(
    title="ProventraCore API",
    description="API for content safety analysis and sanitization",
    version="1.0.0",
)

# Load environment variables, override existing ones
load_dotenv(override=True)

# Include API routes
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "ProventraCore API is running. See /docs for API documentation."}


if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv("PORT", "8000"))

    # Start server
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
