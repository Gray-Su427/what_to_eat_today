from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, canteens, dishes, recommend, reviews, users

# 创建所有表（开发阶段用，生产用 Alembic 迁移）
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="今天吃什么 API",
    description="食堂菜品评价与推荐系统",
    version="0.1.0",
)

# CORS 配置：允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段允许所有来源
    allow_credentials=False,  # 使用 * 时不能开 credentials
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1")
app.include_router(canteens.router, prefix="/api/v1")
app.include_router(dishes.router, prefix="/api/v1")
app.include_router(reviews.router, prefix="/api/v1")
app.include_router(recommend.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "今天吃什么 API 运行中", "docs": "/docs"}
