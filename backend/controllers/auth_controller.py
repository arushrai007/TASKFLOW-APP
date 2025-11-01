from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.user import UserCreate, UserLogin, UserResponse, UserInDB
from utils.auth import hash_password, verify_password, create_access_token
import uuid
from datetime import datetime, timezone

class AuthController:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.users_collection = db.users
    
    async def signup(self, user_data: UserCreate) -> dict:
        """Register a new user"""
        # Check if user already exists
        existing_user = await self.users_collection.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        user_id = str(uuid.uuid4())
        hashed_password = hash_password(user_data.password)
        
        user_in_db = UserInDB(
            id=user_id,
            email=user_data.email,
            name=user_data.name,
            hashed_password=hashed_password,
            created_at=datetime.now(timezone.utc).isoformat()
        )
        
        await self.users_collection.insert_one(user_in_db.model_dump())
        
        # Create access token
        access_token = create_access_token({"user_id": user_id, "email": user_data.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse(
                id=user_id,
                email=user_data.email,
                name=user_data.name,
                created_at=user_in_db.created_at
            )
        }
    
    async def signin(self, user_data: UserLogin) -> dict:
        """Authenticate user and return JWT token"""
        # Find user
        user = await self.users_collection.find_one({"email": user_data.email})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Verify password
        if not verify_password(user_data.password, user["hashed_password"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Create access token
        access_token = create_access_token({"user_id": user["id"], "email": user["email"]})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse(
                id=user["id"],
                email=user["email"],
                name=user["name"],
                created_at=user["created_at"]
            )
        }
    
    async def logout(self) -> dict:
        """Logout user (client-side token removal)"""
        return {"message": "Successfully logged out"}
