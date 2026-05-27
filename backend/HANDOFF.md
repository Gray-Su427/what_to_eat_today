# 后端 API 交接文档

> 后端开发 | 更新日期：2026-05-27

---

## 当前状态

后端 API **已全部完成并测试通过**，可直接启动使用。

---

## 一、已完成的工作

| 模块 | 内容 |
|------|------|
| 环境 | Python 3.13 + conda环境(wise_eat) + PostgreSQL 15(Docker) |
| 认证 | JWT注册/登录/鉴权，bcrypt密码加密 |
| 数据库 | 5张表：users, canteens, windows, dishes, reviews |
| API | 14个端点全部实现（含根路径健康检查，见下方列表） |
| 推荐 | 基于评分排序，排除已评价菜品 |
| 测试数据 | 2食堂、5窗口、15菜品、1测试账号 |
| CORS | 已开启，前端可跨域访问 |

---

## 二、给前端同学

### 连接信息

- **开发阶段 API 地址**：`http://<后端电脑IP>:8001/api/v1`
- **可视化 API 文档**：`http://<后端电脑IP>:8001/docs`
- **测试账号**：`test@example.com` / `123456`

### 认证流程（Flutter 端实现）

```
第1步：登录
  POST /api/v1/auth/login
  Body: {"email": "test@example.com", "password": "123456"}
  返回: {"access_token": "eyJhbG...", "token_type": "bearer"}

第2步：后续请求带 token
  Header: Authorization: Bearer eyJhbG...
```

### 全部 API 端点

| 方法 | 路径 | 需登录 | 说明 | 请求参数 |
|------|------|--------|------|----------|
| POST | /auth/register | 否 | 注册 | {username, email, password} |
| POST | /auth/login | 否 | 登录→返回token | {email, password} |
| GET | /auth/me | 是 | 当前用户信息 | - |
| GET | /canteens | 否 | 食堂列表 | - |
| GET | /canteens/{id}/windows | 否 | 窗口列表 | - |
| GET | /windows/{id}/dishes | 否 | 窗口下的菜品 | - |
| GET | /dishes/{id} | 否 | 菜品详情+评分 | - |
| GET | /dishes?q=&tag=&page=&size= | 否 | 搜索菜品 | q:菜名, tag:标签 |
| POST | /reviews | 是 | 提交/更新评价（同一道菜重复提交会覆盖） | {dish_id, rating(1-5), comment, image_urls} |
| GET | /dishes/{id}/reviews | 否 | 菜品评价列表 | ?page=&size= |
| GET | /recommend | 是 | 推荐菜品(最多10个) | - |
| GET | /users/me/preferences | 是 | 获取偏好 | - |
| PUT | /users/me/preferences | 是 | 更新偏好 | {preferences: {...}} |

### 返回数据示例

**菜品返回格式：**
```json
{
  "id": 1,
  "name": "宫保鸡丁",
  "price": 1200,
  "image_url": null,
  "window_id": 1,
  "tags": ["辣", "鸡肉", "川菜"],
  "is_active": true,
  "avg_rating": 4.5,
  "review_count": 3
}
```

> 注意：price 单位是"分"，前端显示时除以100（1200 → ¥12.0）

---

## 三、给数据采集同学

### 你需要提供的数据格式

整理成 Excel 或 CSV，包含以下列：

| 列名 | 说明 | 示例 |
|------|------|------|
| canteen | 食堂名 | 一食堂 |
| window | 窗口名 | 川菜窗口 |
| dish_name | 菜名 | 宫保鸡丁 |
| price | 价格（元） | 12 |
| tags | 标签（逗号分隔） | 辣,鸡肉,川菜 |

整理好后发给后端，会用脚本批量导入数据库。

### 标签统一用这些

- 辣度：辣、微辣、清淡
- 主料：鸡肉、猪肉、牛肉、鱼、鸡蛋、豆腐、素菜
- 菜系/类型：川菜、面食、快餐、铁板、麻辣烫、粤菜

---

## 四、给测试同学

### 如何测试

1. 后端启动后，浏览器打开 `http://localhost:8001/docs`
2. 每个接口有"Try it out"按钮，点击可直接测试
3. 需要登录的接口：先调 /auth/login 拿 token，点页面顶部 Authorize 按钮填入

### 测试要点

- [ ] 注册新账号能否成功
- [ ] 用错误密码登录，是否返回错误
- [ ] 不带 token 访问需登录接口，是否返回 401
- [ ] 提交评价后，评价列表能否查到
- [ ] 推荐接口是否排除了已评价的菜品
- [ ] 搜索菜品（按菜名、按标签）是否正确

---

## 五、启动方式

```bash
# 1. 启动数据库（需要先安装 Docker Desktop）
cd backend
docker compose up -d

# 2. 安装 Python 依赖
conda create -n wise_eat python=3.13 -y
conda activate wise_eat
pip install -r requirements.txt

# 3. 初始化数据库（仅首次需要）
python seed.py

# 4. 启动后端服务
uvicorn app.main:app --reload --port 8001

# 5. 浏览器打开 API 文档
# http://localhost:8001/docs
```

---

## 六、Git 分支

- `main` — 稳定版本，不直接改
- `dev` — 开发主分支，后端代码在这里
- `feature/xxx` — 新功能分支，完成后合并到 dev

---

## 七、后续待做

| 任务 | 时间 |
|------|------|
| 部署到阿里云服务器 | 6月6日前 |
| 批量导入真实菜品数据 | 数据整理好后 |
| FCM 推送通知 | 6月18日 |
| 前后端联调 | 前端页面做好后 |
