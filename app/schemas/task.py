from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskBase(BaseModel):
    title: str = Field(
        ...,
        json_schema_extra={
            "title": "Task Title",
            "description": "The title of the task",
            "examples": ["Implement login feature", "Fix bug in API"],
        },
    )
    description: Optional[str] = Field(
        None,
        json_schema_extra={
            "title": "Task Description",
            "description": "Detailed description of the task",
            "examples": [
                "Implement login using email and password",
                "Fix issue with token refresh",
            ],
        },
    )
    status: Optional[TaskStatus] = Field(
        TaskStatus.todo,
        json_schema_extra={
            "title": "Task Status",
            "description": "Current status of the task",
            "examples": ["todo", "in_progress", "done"],
        },
    )
    assigned_user_id: Optional[int] = Field(
        None,
        json_schema_extra={
            "title": "Assigned User ID",
            "description": "ID of the user assigned to this task",
            "examples": [1, 2, 3],
        },
    )


class TaskCreate(TaskBase):
    board_id: int = Field(
        ...,
        json_schema_extra={
            "title": "Board ID",
            "description": "ID of the board to which this task belongs",
            "examples": [1],
        },
    )


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        json_schema_extra={
            "title": "Task Title",
            "description": "Updated title of the task",
            "examples": ["Update task title"],
        },
    )
    description: Optional[str] = Field(
        None,
        json_schema_extra={
            "title": "Task Description",
            "description": "Updated description of the task",
            "examples": ["Updated description"],
        },
    )
    status: Optional[TaskStatus] = Field(
        None,
        json_schema_extra={
            "title": "Task Status",
            "description": "Updated status of the task",
            "examples": ["in_progress"],
        },
    )
    assigned_user_id: Optional[int] = Field(
        None,
        json_schema_extra={
            "title": "Assigned User ID",
            "description": "Updated assigned user ID",
            "examples": [2],
        },
    )


class TaskInDBBase(TaskBase):
    id: int = Field(
        ...,
        json_schema_extra={
            "title": "Task ID",
            "description": "Unique identifier of the task",
            "examples": [123],
        },
    )
    board_id: int = Field(
        ...,
        json_schema_extra={
            "title": "Board ID",
            "description": "ID of the board this task belongs to",
            "examples": [1],
        },
    )

    class Config:
        from_attributes = True


class Task(TaskInDBBase):
    pass
