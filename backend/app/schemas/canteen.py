from pydantic import BaseModel


class CanteenResponse(BaseModel):
    id: int
    name: str
    location: str | None = None

    class Config:
        from_attributes = True


class WindowResponse(BaseModel):
    id: int
    name: str
    canteen_id: int
    description: str | None = None

    class Config:
        from_attributes = True
