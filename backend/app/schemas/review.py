from datetime import datetime

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    dish_id: int
    rating: int = Field(ge=1, le=5)
    comment: str | None = None
    image_urls: list[str] | None = None


class ReviewResponse(BaseModel):
    id: int
    user_id: int
    dish_id: int
    rating: int
    comment: str | None = None
    image_urls: list[str] | None = None
    created_at: datetime
    username: str | None = None  # 关联查询时填充

    class Config:
        from_attributes = True
