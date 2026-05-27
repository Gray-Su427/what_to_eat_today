from app.database import SessionLocal
from app.models.canteen import Canteen, Window
from app.models.dish import Dish
from app.models.user import User

db = SessionLocal()
canteens = db.query(Canteen).all()
dishes = db.query(Dish).all()
users = db.query(User).all()
print(f"食堂: {len(canteens)} 个")
for c in canteens:
    print(f"  - {c.name} ({c.location})")
print(f"菜品: {len(dishes)} 个")
for d in dishes[:5]:
    print(f"  - {d.name} ¥{d.price/100:.1f} {d.tags}")
print(f"  ... 共 {len(dishes)} 道")
print(f"用户: {len(users)} 个")
print(f"  测试账号: test@example.com / 123456")
db.close()
