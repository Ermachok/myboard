from typing import List, Optional

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate


async def create_task(session: AsyncSession, task_in: TaskCreate) -> Task:
    task = Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status or TaskStatus.todo,
        board_id=task_in.board_id,
        assigned_user_id=task_in.assigned_user_id,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_task(session: AsyncSession, task_id: int) -> Optional[Task]:
    result = await session.execute(select(Task).where(Task.id == task_id))
    return result.scalars().first()


async def get_tasks_for_board(
    session: AsyncSession, board_id: int, status: Optional[TaskStatus] = None
) -> List[Task]:
    query = select(Task).where(Task.board_id == board_id)
    if status:
        query = query.where(Task.status == status)
    result = await session.execute(query)
    return result.scalars().all()


async def update_task(
    session: AsyncSession, task_id: int, task_in: TaskUpdate
) -> Optional[Task]:
    task = await get_task(session, task_id)
    if not task:
        return None

    for field, value in task_in.dict(exclude_unset=True).items():
        setattr(task, field, value)

    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(session: AsyncSession, task_id: int) -> bool:
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        return False
    await session.delete(task)
    await session.commit()
    return True
