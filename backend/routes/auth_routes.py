from fastapi import APIRouter, Depends
from models.user import UserCreate, UserLogin
from controllers.auth_controller import AuthController
from motor.motor_asyncio import AsyncIOMotorDatabase
from utils.auth import get_current_user

def create_auth_routes(db: AsyncIOMotorDatabase) -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["Authentication"])
    auth_controller = AuthController(db)
    
    @router.post("/signup", status_code=201)
    async def signup(user_data: UserCreate):
        """User registration endpoint"""
        return await auth_controller.signup(user_data)
    
    @router.post("/signin", status_code=200)
    async def signin(user_data: UserLogin):
        """User login endpoint"""
        return await auth_controller.signin(user_data)
    
    @router.post("/logout", status_code=200)
    async def logout(current_user: dict = Depends(get_current_user)):
        """User logout endpoint"""
        return await auth_controller.logout()
    
    return router
