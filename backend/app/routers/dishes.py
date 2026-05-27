from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.dish import Dish
from app.models.review import Review
from app.schemas.dish import DishDetail, DishResponse

router = APIRouter(prefix="", tags=["菜品"])

RECOMMEND_THRESHOLD = 4.5
RECOMMEND_MIN_REVIEWS = 5


@router.get("/windows/{window_id}/dishes", response_model=list[DishResponse])
def get_dishes_by_window(window_id: int, db: Session = Depends(get_db)):
    """获取某个窗口下的活跃菜品"""
    dishes = (
        db.query(Dish).filter(Dish.window_id == window_id, Dish.is_active).all()
    )
    return _attach_ratings(dishes, db)


@router.get("/dishes", response_model=list[DishResponse])
def search_dishes(
    q: str | None = Query(None, description="搜索菜名"),
    tag: str | None = Query(None, description="按标签筛选"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """全局搜索或筛选菜品"""
    query = db.query(Dish).filter(Dish.is_active)
    if q:
        query = query.filter(Dish.name.ilike(f"%{q}%"))
    if tag:
        query = query.filter(Dish.tags.any(tag))
    dishes = query.offset((page - 1) * size).limit(size).all()
    return _attach_ratings(dishes, db)


@router.get("/dishes/{dish_id}", response_model=DishDetail)
def get_dish_detail(dish_id: int, db: Session = Depends(get_db)):
    """获取菜品详情"""
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="菜品不存在")
    stats = _get_dish_stats(dish_id, db)
    return DishDetail(
        **{c.name: getattr(dish, c.name) for c in dish.__table__.columns},
        avg_rating=stats["avg"],
        review_count=stats["count"],
        is_recommended=(
            stats["avg"] is not None
            and stats["avg"] >= RECOMMEND_THRESHOLD
            and stats["count"] >= RECOMMEND_MIN_REVIEWS
        ),
    )


def _attach_ratings(dishes: list[Dish], db: Session) -> list[dict]:
    """给菜品列表附加评分信息"""
    result = []
    for dish in dishes:
        stats = _get_dish_stats(dish.id, db)
        result.append(
            DishResponse(
                **{c.name: getattr(dish, c.name) for c in dish.__table__.columns},
                avg_rating=stats["avg"],
                review_count=stats["count"],
            )
        )
    return result


def _get_dish_stats(dish_id: int, db: Session) -> dict:
    """获取菜品的平均评分和评价数"""
    row = (
        db.query(
            func.avg(Review.rating).label("avg"),
            func.count(Review.id).label("count"),
        )
        .filter(Review.dish_id == dish_id)
        .first()
    )
    return {
        "avg": round(float(row.avg), 1) if row.avg else None,
        "count": row.count or 0,
    }
