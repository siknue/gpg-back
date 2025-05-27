from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mangum import Mangum

# Glass Stress Calculation API
from app.api.api import router as glass_calculator_router
# Authentication Router

app = FastAPI(title="Glass Stress Calculator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(glass_calculator_router)

@app.get("")
def read_root():
    return {"message": "Glass Stress Calculation API"}

handler = Mangum(app)