from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.task import TaskCreate, TaskResponse, TaskStatus, TaskUpdate
from app.services.task import (create_task, delete_task, get_task,
                               get_tasks_for_board, update_task)

task_router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@task_router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    task_in: TaskCreate, session: AsyncSession = Depends(get_session)
):
    task = await create_task(session, task_in)
    return task


@task_router.get("/{task_id}", response_model=TaskResponse)
async def read_task(task_id: int, session: AsyncSession = Depends(get_session)):
    task = await get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@task_router.get("/", response_model=List[TaskResponse])
async def read_tasks(
    board_id: int,
    status: Optional[TaskStatus] = None,
    session: AsyncSession = Depends(get_session),
):
    tasks = await get_tasks_for_board(session, board_id, status)
    return tasks


@task_router.patch("/{task_id}", response_model=TaskResponse)
async def update_existing_task(
    task_id: int, task_in: TaskUpdate, session: AsyncSession = Depends(get_session)
):
    task = await update_task(session, task_id, task_in)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_task(
    task_id: int, session: AsyncSession = Depends(get_session)
):
    success = await delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return
