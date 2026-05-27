"""导出 OpenAPI 文档为 JSON 文件，供 Apifox 导入"""
import json
from app.main import app

schema = app.openapi()
with open("openapi.json", "w", encoding="utf-8") as f:
    json.dump(schema, f, ensure_ascii=False, indent=2)

print("已导出 openapi.json")
print("导入方式：Apifox → 新建项目 → 导入 → 选择文件 → openapi.json")
