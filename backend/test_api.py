"""API 自动测试脚本"""
import httpx

BASE = "http://localhost:8000/api/v1"


def test_all():
    client = httpx.Client(base_url=BASE, timeout=5)

    print("=" * 50)
    print("  今天吃什么 - API 测试")
    print("=" * 50)

    # 1. 注册
    print("\n[1] 注册新用户...")
    r = client.post("/auth/register", json={
        "username": "demo", "email": "demo@test.com", "password": "abc123"
    })
    if r.status_code == 200:
        print(f"    OK: {r.json()['username']} 注册成功")
    else:
        print(f"    (已存在或失败: {r.json().get('detail', r.text)})")

    # 2. 登录
    print("\n[2] 登录...")
    r = client.post("/auth/login", json={
        "email": "test@example.com", "password": "123456"
    })
    assert r.status_code == 200, f"登录失败: {r.text}"
    token = r.json()["access_token"]
    print(f"    OK: 获得 token (前20字符: {token[:20]}...)")
    headers = {"Authorization": f"Bearer {token}"}

    # 3. 获取当前用户
    print("\n[3] 获取当前用户信息...")
    r = client.get("/auth/me", headers=headers)
    user = r.json()
    print(f"    OK: {user['username']} ({user['email']})")

    # 4. 食堂列表
    print("\n[4] 获取食堂列表...")
    r = client.get("/canteens")
    canteens = r.json()
    for c in canteens:
        print(f"    - {c['name']} ({c['location']})")

    # 5. 窗口列表
    print("\n[5] 获取一食堂的窗口...")
    r = client.get("/canteens/1/windows")
    windows = r.json()
    for w in windows:
        print(f"    - {w['name']}")

    # 6. 菜品列表
    print("\n[6] 获取川菜窗口的菜品...")
    r = client.get("/windows/1/dishes")
    dishes = r.json()
    for d in dishes:
        print(f"    - {d['name']} ¥{d['price']/100:.0f} {d['tags']}")

    # 7. 提交评价
    print("\n[7] 给宫保鸡丁打5星...")
    r = client.post("/reviews", headers=headers, json={
        "dish_id": 1, "rating": 5, "comment": "好吃！推荐！"
    })
    review = r.json()
    print(f"    OK: {review['rating']}星 - {review['comment']}")

    # 8. 查看评价
    print("\n[8] 查看宫保鸡丁的评价...")
    r = client.get("/reviews/dishes/1/reviews")
    reviews = r.json()
    for rv in reviews:
        print(f"    - {rv['username']}: {rv['rating']}星 {rv['comment']}")

    # 9. 推荐
    print("\n[9] 获取推荐菜品...")
    r = client.get("/recommend", headers=headers)
    recs = r.json()
    for d in recs[:5]:
        print(f"    - {d['name']} ¥{d['price']/100:.0f}")

    print("\n" + "=" * 50)
    print("  全部测试通过!")
    print("=" * 50)


if __name__ == "__main__":
    test_all()
