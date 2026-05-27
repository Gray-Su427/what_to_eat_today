from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewResponse

router = APIRouter(prefix="/reviews", tags=["评价"])


@router.post("", response_model=ReviewResponse)
def create_review(
    data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """提交评价（需要登录）"""
    review = Review(
        user_id=current_user.id,
        dish_id=data.dish_id,
        rating=data.rating,
        comment=data.comment,
        image_urls=data.image_urls,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return ReviewResponse(
        **{c.name: getattr(review, c.name) for c in review.__table__.columns},
        username=current_user.username,
    )


@router.get("/dishes/{dish_id}/reviews", response_model=list[ReviewResponse])
def get_dish_reviews(
    dish_id: int,
    page: int = 1,
    size: int = 20,
    db: Session = Depends(get_db),
):
    """获取某菜品的评价列表（含用户昵称）"""
    reviews = (
        db.query(Review)
        .filter(Review.dish_id == dish_id)
        .order_by(Review.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    result = []
    for r in reviews:
        user = db.query(User).filter(User.id == r.user_id).first()
        result.append(
            ReviewResponse(
                **{c.name: getattr(r, c.name) for c in r.__table__.columns},
                username=user.username if user else None,
            )
        )
    return result
