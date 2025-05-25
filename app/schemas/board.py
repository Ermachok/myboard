from typing import Optional

from pydantic import BaseModel, Field


class BoardBase(BaseModel):
    title: str = Field(
        ...,
        json_schema_extra={
            "title": "Board Title",
            "description": "Title of the board",
            "examples": ["Sprint Planning Board"],
        },
    )
    description: Optional[str] = Field(
        None,
        json_schema_extra={
            "title": "Board Description",
            "description": "Optional description of the board",
            "examples": ["Board for sprint planning tasks"],
        },
    )


class BoardCreate(BoardBase):
    pass


class BoardUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        json_schema_extra={
            "title": "Updated Title",
            "description": "New title for the board",
            "examples": ["Updated title"],
        },
    )
    description: Optional[str] = Field(
        None,
        json_schema_extra={
            "title": "Updated Description",
            "description": "New description for the board",
            "examples": ["Updated description"],
        },
    )


class BoardInDBBase(BaseModel):
    id: int = Field(
        ...,
        json_schema_extra={
            "title": "Board ID",
            "description": "Unique identifier for the board",
            "examples": [1],
        },
    )
    title: str = Field(
        ...,
        json_schema_extra={
            "title": "Title",
            "description": "Name of the board",
            "examples": ["Project Alpha"],
        },
    )
    description: str | None = Field(
        None,
        json_schema_extra={
            "title": "Description",
            "description": "Detailed description of the board",
            "examples": ["Board for managing Alpha project tasks"],
        },
    )

    class Config:
        from_attributes = True


class Board(BoardInDBBase):
    pass
