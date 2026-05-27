from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.dish import Dish
from app.models.review import Review
from app.models.user import User
from app.schemas.dish import DishResponse
from app.schemas.user import PreferencesUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["用户"])


@router.get("/me/preferences")
def get_preferences(current_user: User = Depends(get_current_user)):
    """获取当前用户的偏好设置"""
    return {"preferences": current_user.preferences or {}}


@router.put("/me/preferences", response_model=UserResponse)
def update_preferences(
    data: PreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """更新偏好"""
    current_user.preferences = data.preferences
    db.commit()
    db.refresh(current_user)
    return current_user
