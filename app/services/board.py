from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.board import Board
from app.schemas.board import BoardCreate, BoardUpdate


async def get_board(db: AsyncSession, board_id: int) -> Board | None:
    result = await db.execute(select(Board).where(Board.id == board_id))
    return result.scalar_one_or_none()


async def get_user_boards(
    db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
) -> list[Board]:
    stmt = select(Board).where(Board.owner_id == user_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_board(
    db: AsyncSession, board_data: BoardCreate, user_id: int
) -> Board:
    board = Board(**board_data.model_dump(), owner_id=user_id)
    db.add(board)
    await db.commit()
    await db.refresh(board)
    return board


async def update_board(
    db: AsyncSession, board: Board, board_data: BoardUpdate
) -> Board:
    for field, value in board_data.model_dump(exclude_unset=True).items():
        setattr(board, field, value)
    await db.commit()
    await db.refresh(board)
    return board


async def delete_board(db: AsyncSession, board: Board) -> None:
    await db.delete(board)
    await db.commit()
