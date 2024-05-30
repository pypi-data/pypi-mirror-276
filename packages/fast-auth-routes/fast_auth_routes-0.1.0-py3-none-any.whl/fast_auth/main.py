from fastapi import FastAPI, Depends, HTTPException, status
from fast_auth.auth.utils import get_current_user
from fast_auth.auth.routes import auth_router
from fast_auth.config import MONGO_URI, MONGO_DB_NAME
import motor.motor_asyncio


app = FastAPI()

app.include_router(auth_router)

@app.on_event("startup")
async def startup_db_client():
    print(MONGO_URI, MONGO_DB_NAME)
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    app.mongodb = app.mongodb_client[MONGO_DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/protected")
async def read_protected_route(current_user: dict = Depends(get_current_user)):
    return {"msg": f"Hello, {current_user['email']}! This is a protected route."}