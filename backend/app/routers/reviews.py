from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.dish import Dish
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewResponse

router = APIRouter(tags=["评价"])


@router.post("/reviews", response_model=ReviewResponse)
def create_review(
    data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """提交评价（需要登录）。同一道菜重复提交会更新原有评价。"""
    # 检查菜品是否存在且在售
    dish = db.query(Dish).filter(Dish.id == data.dish_id, Dish.is_active == True).first()
    if not dish:
        raise HTTPException(status_code=404, detail="菜品不存在或已下架")

    # 查找是否已评价过，有则更新，无则新建
    existing = db.query(Review).filter(
        Review.user_id == current_user.id, Review.dish_id == data.dish_id
    ).first()

    if existing:
        # 删除该用户对该菜品的所有旧评价，重新创建
        db.query(Review).filter(
            Review.user_id == current_user.id, Review.dish_id == data.dish_id
        ).delete()
        db.flush()
        new_review = Review(
            user_id=current_user.id,
            dish_id=data.dish_id,
            rating=data.rating,
            comment=data.comment,
            image_urls=data.image_urls,
        )
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return ReviewResponse(
            **{c.name: getattr(new_review, c.name) for c in new_review.__table__.columns},
            username=current_user.username,
        )

    review = Review(
        user_id=current_user.id,
        dish_id=data.dish_id,
        rating=data.rating,
        comment=data.comment,
        image_urls=data.image_urls,
    )
    db.add(review)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="提交失败，请重试")
    db.refresh(review)
    return ReviewResponse(
        **{c.name: getattr(review, c.name) for c in review.__table__.columns},
        username=current_user.username,
    )


@router.get("/dishes/{dish_id}/reviews", response_model=list[ReviewResponse])
def get_dish_reviews(
    dish_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """获取某菜品的评价列表（含用户昵称）"""
    rows = (
        db.query(Review, User.username)
        .join(User, User.id == Review.user_id)
        .filter(Review.dish_id == dish_id)
        .order_by(Review.created_at.desc())
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    return [
        ReviewResponse(
            **{c.name: getattr(r, c.name) for c in r.__table__.columns},
            username=username,
        )
        for r, username in rows
    ]
