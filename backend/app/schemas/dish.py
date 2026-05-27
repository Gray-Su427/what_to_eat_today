from datetime import datetime

from pydantic import BaseModel


class DishResponse(BaseModel):
    id: int
    name: str
    price: int
    image_url: str | None = None
    window_id: int
    tags: list[str] | None = None
    is_active: bool
    avg_rating: float | None = None
    review_count: int = 0

    class Config:
        from_attributes = True


class DishDetail(DishResponse):
    """菜品详情，包含是否推荐"""
    is_recommended: bool = False
