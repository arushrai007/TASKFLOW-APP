from fastapi import APIRouter, Depends, Query
from models.task import TaskCreate, TaskUpdate, TaskResponse, TaskStats
from controllers.task_controller import TaskController
from motor.motor_asyncio import AsyncIOMotorDatabase
from utils.auth import get_current_user
from typing import List, Optional

def create_task_routes(db: AsyncIOMotorDatabase) -> APIRouter:
    router = APIRouter(prefix="/tasks", tags=["Tasks"])
    task_controller = TaskController(db)
    
    @router.post("", response_model=TaskResponse, status_code=201)
    async def create_task(
        task_data: TaskCreate,
        current_user: dict = Depends(get_current_user)
    ):
        """Create a new task"""
        return await task_controller.create_task(task_data, current_user["user_id"])
    
    @router.get("", response_model=List[TaskResponse], status_code=200)
    async def get_all_tasks(
        completed: Optional[bool] = Query(None, description="Filter by completion status"),
        sort_by: str = Query("created_at", description="Sort by field (created_at, priority, due_date)"),
        sort_order: int = Query(-1, description="Sort order (1 for ascending, -1 for descending)"),
        search: Optional[str] = Query(None, description="Search in title, description, and tags"),
        category: Optional[str] = Query(None, description="Filter by category"),
        current_user: dict = Depends(get_current_user)
    ):
        """Get all tasks with filtering and sorting"""
        return await task_controller.get_all_tasks(
            current_user["user_id"],
            completed=completed,
            sort_by=sort_by,
            sort_order=sort_order,
            search=search,
            category=category
        )
    
    @router.get("/stats", response_model=TaskStats, status_code=200)
    async def get_task_stats(
        current_user: dict = Depends(get_current_user)
    ):
        """Get task statistics"""
        return await task_controller.get_task_stats(current_user["user_id"])
    
    @router.put("/{task_id}", response_model=TaskResponse, status_code=200)
    async def update_task(
        task_id: str,
        task_data: TaskUpdate,
        current_user: dict = Depends(get_current_user)
    ):
        """Update a task"""
        return await task_controller.update_task(task_id, task_data, current_user["user_id"])
    
    @router.delete("/{task_id}", status_code=200)
    async def delete_task(
        task_id: str,
        current_user: dict = Depends(get_current_user)
    ):
        """Delete a task"""
        return await task_controller.delete_task(task_id, current_user["user_id"])
    
    @router.patch("/{task_id}/complete", response_model=TaskResponse, status_code=200)
    async def mark_complete(
        task_id: str,
        completed: bool = Query(..., description="Mark as complete or incomplete"),
        current_user: dict = Depends(get_current_user)
    ):
        """Mark task as complete or incomplete"""
        return await task_controller.mark_complete(task_id, current_user["user_id"], completed)
    
    return router
