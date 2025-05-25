from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.user import User
from app.schemas.board import Board, BoardCreate, BoardUpdate
from app.services.board import create_board as create_board_service
from app.services.board import delete_board as delete_board_service
from app.services.board import get_board as get_board_service
from app.services.board import get_user_boards
from app.services.board import update_board as update_board_service
from app.services.user import get_current_user

board_router = APIRouter(prefix="/api/boards", tags=["Boards"])


@board_router.get("/", response_model=List[Board])
async def read_boards(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    return await get_user_boards(db, user_id=current_user.id, skip=skip, limit=limit)


@board_router.post("/", response_model=Board)
async def create_board(
    board_data: BoardCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await create_board_service(db, board_data, user_id=current_user.id)


@board_router.get("/{board_id}", response_model=Board)
async def read_board(
    board_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    board = await get_board_service(db, board_id)
    if not board or board.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Board not found")
    return board


@board_router.put("/{board_id}", response_model=Board)
async def update_board(
    board_id: int,
    board_data: BoardUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    board = await get_board_service(db, board_id)
    if not board or board.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Board not found")
    return await update_board_service(db, board, board_data)


@board_router.delete("/{board_id}")
async def delete_board(
    board_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    board = await get_board_service(db, board_id)
    if not board or board.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Board not found")
    await delete_board_service(db, board)
    return {"ok": True}
