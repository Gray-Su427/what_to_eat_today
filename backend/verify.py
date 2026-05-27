"""直接测试（不需要启动服务器）"""
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine
from app.models.canteen import Canteen, Window
from app.models.dish import Dish
from app.models.review import Review
from app.models.user import User
from app.utils.security import hash_password

# 重建表
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# 插入测试数据
db = SessionLocal()
db.add(Canteen(id=1, name="一食堂", location="教学楼北侧"))
db.add(Window(id=1, name="川菜窗口", canteen_id=1))
db.add(Dish(id=1, name="宫保鸡丁", price=1200, window_id=1, tags=["辣", "鸡肉"]))
db.add(User(id=1, username="test", email="test@test.com",
            hashed_password=hash_password("123456")))
db.commit()
db.close()

client = TestClient(app)
BASE = "/api/v1"

print("=" * 50)
print("  接口验证测试")
print("=" * 50)

# 1. 登录
r = client.post(f"{BASE}/auth/login", json={"email": "test@test.com", "password": "123456"})
assert r.status_code == 200, f"登录失败: {r.text}"
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("[OK] 登录成功")

# 2. 食堂列表
r = client.get(f"{BASE}/canteens")
assert r.status_code == 200 and len(r.json()) == 1
print("[OK] 食堂列表")

# 3. 菜品列表
r = client.get(f"{BASE}/windows/1/dishes")
assert r.status_code == 200 and len(r.json()) == 1
print("[OK] 菜品列表")

# 4. 提交评价
r = client.post(f"{BASE}/reviews", headers=headers, json={
    "dish_id": 1, "rating": 5, "comment": "好吃"
})
assert r.status_code == 200, f"提交评价失败: {r.text}"
print("[OK] 提交评价")

# 5. 重复评价被拦截
r = client.post(f"{BASE}/reviews", headers=headers, json={
    "dish_id": 1, "rating": 3, "comment": "再评"
})
assert r.status_code == 409, f"重复评价应返回409，实际: {r.status_code} {r.text}"
print("[OK] 重复评价拦截 (409)")

# 6. 查看评价列表
r = client.get(f"{BASE}/reviews/1")
assert r.status_code == 200, f"评价列表失败: {r.status_code} {r.text}"
reviews = r.json()
assert len(reviews) == 1 and reviews[0]["rating"] == 5
print("[OK] 评价列表")

# 7. 评价不存在的菜品
r = client.post(f"{BASE}/reviews", headers=headers, json={
    "dish_id": 999, "rating": 5, "comment": "不存在"
})
assert r.status_code == 404, f"应返回404，实际: {r.status_code}"
print("[OK] 不存在菜品返回404")

# 8. 推荐
r = client.get(f"{BASE}/recommend", headers=headers)
assert r.status_code == 200
print("[OK] 推荐接口")

print("\n" + "=" * 50)
print("  全部 8 项检查通过!")
print("=" * 50)
