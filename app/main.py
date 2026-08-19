from fastapi import FastAPI

from app.core.dependencies import DBSession

app = FastAPI()


@app.get("/")
async def root(db: DBSession) -> dict:
    return {"message": "Coneccion exitosa"}
