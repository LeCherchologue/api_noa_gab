
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import UsersRouter, ProduitsRouter, CommandesRouter
from api.bdd.connexion import Base, engine
from fastapi.staticfiles import StaticFiles




app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
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

