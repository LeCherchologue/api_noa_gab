from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import UsersRouter, ProduitsRouter, CommandesRouter
from api.bdd.connexion import Base, engine
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

origins = [
    "https://noagab-mini-shop.vercel.app",
    "capacitor://localhost",
    "ionic://localhost",
    "http://localhost",
    "http://localhost:8100",  # Port par défaut d'Ionic
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:8100",
    "http://10.0.2.2",  # Émulateur Android
    "http://10.0.2.2:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(UsersRouter.router, prefix="/api")
app.include_router(ProduitsRouter.router, prefix="/api")
app.include_router(CommandesRouter.router, prefix="/api")

@app.get("/")
async def main():
    return {
        "message": "API demarre",
    }