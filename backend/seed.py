"""
测试数据初始化脚本
运行方式: conda activate wise_eat && cd backend && python seed.py
"""

from app.database import SessionLocal, engine, Base
from app.models.canteen import Canteen, Window
from app.models.dish import Dish
from app.models.user import User
from app.utils.security import hash_password

# 确保表存在
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 清空旧数据（开发阶段用）
db.query(Dish).delete()
db.query(Window).delete()
db.query(Canteen).delete()
db.commit()

# ========== 食堂 ==========
canteens = [
    Canteen(id=1, name="一食堂", location="教学楼北侧"),
    Canteen(id=2, name="二食堂", location="宿舍区旁"),
]
db.add_all(canteens)
db.commit()

# ========== 窗口 ==========
windows = [
    Window(id=1, name="川菜窗口", canteen_id=1),
    Window(id=2, name="面食窗口", canteen_id=1),
    Window(id=3, name="快餐窗口", canteen_id=1),
    Window(id=4, name="麻辣烫窗口", canteen_id=2),
    Window(id=5, name="铁板饭窗口", canteen_id=2),
]
db.add_all(windows)
db.commit()

# ========== 菜品 ==========
dishes = [
    # 一食堂 - 川菜窗口
    Dish(name="宫保鸡丁", price=1200, window_id=1,
         tags=["辣", "鸡肉", "川菜"]),
    Dish(name="麻婆豆腐", price=800, window_id=1,
         tags=["辣", "豆腐", "川菜"]),
    Dish(name="鱼香肉丝", price=1100, window_id=1,
         tags=["微辣", "猪肉", "川菜"]),
    Dish(name="回锅肉", price=1300, window_id=1,
         tags=["辣", "猪肉", "川菜"]),

    # 一食堂 - 面食窗口
    Dish(name="牛肉拉面", price=1000, window_id=2,
         tags=["清淡", "牛肉", "面食"]),
    Dish(name="炸酱面", price=800, window_id=2,
         tags=["清淡", "猪肉", "面食"]),
    Dish(name="番茄鸡蛋面", price=700, window_id=2,
         tags=["清淡", "鸡蛋", "面食"]),

    # 一食堂 - 快餐窗口
    Dish(name="红烧排骨饭", price=1500, window_id=3,
         tags=["微辣", "猪肉", "快餐"]),
    Dish(name="咖喱鸡饭", price=1200, window_id=3,
         tags=["微辣", "鸡肉", "快餐"]),
    Dish(name="糖醋里脊饭", price=1300, window_id=3,
         tags=["清淡", "猪肉", "快餐"]),

    # 二食堂 - 麻辣烫窗口
    Dish(name="麻辣烫（小份）", price=1000, window_id=4,
         tags=["辣", "混合", "麻辣烫"]),
    Dish(name="麻辣烫（大份）", price=1500, window_id=4,
         tags=["辣", "混合", "麻辣烫"]),

    # 二食堂 - 铁板饭窗口
    Dish(name="黑椒牛柳铁板饭", price=1600, window_id=5,
         tags=["微辣", "牛肉", "铁板"]),
    Dish(name="照烧鸡腿铁板饭", price=1400, window_id=5,
         tags=["清淡", "鸡肉", "铁板"]),
    Dish(name="鱼香茄子铁板饭", price=1100, window_id=5,
         tags=["微辣", "素菜", "铁板"]),
]
db.add_all(dishes)
db.commit()

# ========== 测试用户 ==========
test_user = db.query(User).filter(User.username == "test").first()
if not test_user:
    test_user = User(
        username="test",
        email="test@example.com",
        hashed_password=hash_password("123456"),
        preferences={"spicy": 0.8, "meat": 0.6, "noodle": 0.3},
    )
    db.add(test_user)
    db.commit()

db.close()

print("测试数据录入完成！")
print(f"  食堂: {len(canteens)} 个")
print(f"  窗口: {len(windows)} 个")
print(f"  菜品: {len(dishes)} 个")
print(f"  测试账号: test@example.com / 123456")
