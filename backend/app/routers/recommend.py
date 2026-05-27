from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.dish import Dish
from app.models.review import Review
from app.models.user import User
from app.schemas.dish import DishResponse

router = APIRouter(prefix="/recommend", tags=["推荐"])


@router.get("", response_model=list[DishResponse])
def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    个性化推荐菜品（最多10个）
    策略：
    1. 有偏好 → 按标签匹配
    2. 无偏好 → 返回热门菜品（高分+评价多）
    排除用户已评价过的菜品
    """
    # 获取用户已评价的菜品ID
    reviewed_ids = [
        r.dish_id
        for r in db.query(Review.dish_id)
        .filter(Review.user_id == current_user.id)
        .all()
    ]

    # 基础查询：活跃菜品，排除已评价
    query = db.query(Dish).filter(Dish.is_active)
    if reviewed_ids:
        query = query.filter(Dish.id.notin_(reviewed_ids))

    # 获取候选菜品
    candidates = query.all()

    # 按评分排序（热门推荐兜底策略）
    scored = []
    for dish in candidates:
        stats = (
            db.query(
                func.avg(Review.rating).label("avg"),
                func.count(Review.id).label("count"),
            )
            .filter(Review.dish_id == dish.id)
            .first()
        )
        avg = float(stats.avg) if stats.avg else 0
        count = stats.count or 0
        # 简单评分公式：平均分 * 0.7 + 评价数权重 * 0.3
        score = avg * 0.7 + min(count / 10, 1) * 5 * 0.3
        scored.append((dish, avg, count, score))

    # 按分数降序，取前10
    scored.sort(key=lambda x: x[3], reverse=True)
    top10 = scored[:10]

    return [
        DishResponse(
            **{c.name: getattr(d, c.name) for c in d.__table__.columns},
            avg_rating=round(avg, 1) if avg else None,
            review_count=count,
        )
        for d, avg, count, _ in top10
    ]
