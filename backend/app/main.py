from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.routes import router  

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://learning-platform-dash.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)