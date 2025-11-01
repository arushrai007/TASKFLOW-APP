from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.task import TaskCreate, TaskUpdate, TaskResponse, TaskInDB, TaskStats
from typing import List, Optional
from datetime import datetime, timezone, timedelta

class TaskController:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.tasks_collection = db.tasks
    
    async def create_task(self, task_data: TaskCreate, user_id: str) -> TaskResponse:
        """Create a new task"""
        task_in_db = TaskInDB(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            due_date=task_data.due_date,
            category=task_data.category,
            tags=task_data.tags or []
        )
        
        await self.tasks_collection.insert_one(task_in_db.model_dump())
        
        return TaskResponse(**task_in_db.model_dump())
    
    async def get_all_tasks(
        self, 
        user_id: str, 
        completed: Optional[bool] = None,
        sort_by: str = "created_at",
        sort_order: int = -1,
        search: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[TaskResponse]:
        """Get all tasks with server-side filtering and sorting using aggregation"""
        # Build aggregation pipeline
        pipeline = [
            {"$match": {"user_id": user_id}}
        ]
        
        # Add completion filter if specified
        if completed is not None:
            pipeline[0]["$match"]["completed"] = completed
        
        # Add category filter
        if category:
            pipeline[0]["$match"]["category"] = category
        
        # Add search filter
        if search:
            pipeline.append({
                "$match": {
                    "$or": [
                        {"title": {"$regex": search, "$options": "i"}},
                        {"description": {"$regex": search, "$options": "i"}},
                        {"tags": {"$in": [search]}}
                    ]
                }
            })
        
        # Add sorting
        # Priority sorting: High > Medium > Low
        if sort_by == "priority":
            pipeline.extend([
                {
                    "$addFields": {
                        "priority_order": {
                            "$switch": {
                                "branches": [
                                    {"case": {"$eq": ["$priority", "High"]}, "then": 1},
                                    {"case": {"$eq": ["$priority", "Medium"]}, "then": 2},
                                    {"case": {"$eq": ["$priority", "Low"]}, "then": 3}
                                ],
                                "default": 4
                            }
                        }
                    }
                },
                {"$sort": {"priority_order": sort_order}}
            ])
        else:
            pipeline.append({"$sort": {sort_by: sort_order}})
        
        # Execute aggregation
        cursor = self.tasks_collection.aggregate(pipeline)
        tasks = await cursor.to_list(length=None)
        
        return [TaskResponse(**task) for task in tasks]
    
    async def get_task_stats(self, user_id: str) -> TaskStats:
        """Get task statistics"""
        all_tasks = await self.tasks_collection.find({"user_id": user_id}).to_list(length=None)
        
        total = len(all_tasks)
        completed = sum(1 for t in all_tasks if t.get("completed", False))
        pending = total - completed
        
        high_priority = sum(1 for t in all_tasks if t.get("priority") == "High" and not t.get("completed"))
        medium_priority = sum(1 for t in all_tasks if t.get("priority") == "Medium" and not t.get("completed"))
        low_priority = sum(1 for t in all_tasks if t.get("priority") == "Low" and not t.get("completed"))
        
        # Calculate overdue and due today
        now = datetime.now(timezone.utc)
        today_end = now.replace(hour=23, minute=59, second=59)
        
        overdue = 0
        due_today = 0
        
        for task in all_tasks:
            if task.get("completed") or not task.get("due_date"):
                continue
            
            try:
                due_date = datetime.fromisoformat(task["due_date"].replace('Z', '+00:00'))
                if due_date < now:
                    overdue += 1
                elif due_date.date() == now.date():
                    due_today += 1
            except:
                pass
        
        # Category breakdown
        categories = {}
        for task in all_tasks:
            cat = task.get("category", "Uncategorized")
            if cat:
                categories[cat] = categories.get(cat, 0) + 1
        
        return TaskStats(
            total=total,
            completed=completed,
            pending=pending,
            high_priority=high_priority,
            medium_priority=medium_priority,
            low_priority=low_priority,
            overdue=overdue,
            due_today=due_today,
            categories=categories
        )
    
    async def update_task(self, task_id: str, task_data: TaskUpdate, user_id: str) -> TaskResponse:
        """Update a task"""
        # Check if task exists and belongs to user
        task = await self.tasks_collection.find_one({"id": task_id, "user_id": user_id})
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Update fields
        update_data = task_data.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        
        await self.tasks_collection.update_one(
            {"id": task_id, "user_id": user_id},
            {"$set": update_data}
        )
        
        # Fetch updated task
        updated_task = await self.tasks_collection.find_one({"id": task_id})
        return TaskResponse(**updated_task)
    
    async def delete_task(self, task_id: str, user_id: str) -> dict:
        """Delete a task"""
        result = await self.tasks_collection.delete_one({"id": task_id, "user_id": user_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return {"message": "Task deleted successfully"}
    
    async def mark_complete(self, task_id: str, user_id: str, completed: bool) -> TaskResponse:
        """Mark task as complete or incomplete"""
        task = await self.tasks_collection.find_one({"id": task_id, "user_id": user_id})
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        await self.tasks_collection.update_one(
            {"id": task_id, "user_id": user_id},
            {"$set": {"completed": completed, "updated_at": datetime.now(timezone.utc).isoformat()}}
        )
        
        updated_task = await self.tasks_collection.find_one({"id": task_id})
        return TaskResponse(**updated_task)
