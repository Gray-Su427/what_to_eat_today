from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.canteen import Canteen, Window
from app.schemas.canteen import CanteenResponse, WindowResponse

router = APIRouter(prefix="/canteens", tags=["食堂"])


@router.get("", response_model=list[CanteenResponse])
def get_canteens(db: Session = Depends(get_db)):
    """获取所有食堂列表"""
    return db.query(Canteen).all()


@router.get("/{canteen_id}/windows", response_model=list[WindowResponse])
def get_windows(canteen_id: int, db: Session = Depends(get_db)):
    """获取某个食堂下的所有窗口"""
    return db.query(Window).filter(Window.canteen_id == canteen_id).all()
