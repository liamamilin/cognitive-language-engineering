# 认知语言工程｜完整体系v0.6工作版

2026-10-01 · 尚未冻结。基于完整v0.5，沿Principle → Model → 接口 → 算子 → 语言模式打磨，保留81接口并补齐学习连接。新增3算子及3模式；原结构核心v0.2仍基于v0.5冻结。

从[阅读入口](docs/index.md)和[学习主线](docs/learning/MAINLINE.md)开始；学习连接在模型卡与索引中，实际应用另见指南。正文权威来源是docs。

```bash
python scripts/update_registry.py --check
python scripts/check_mainline.py
python scripts/check_docs.py
python scripts/check_essentials.py
python -m mkdocs build --strict
python scripts/check_site.py
python scripts/export_book.py --output-dir reading
```

构建依赖见requirements.txt。GitHub同步目标为原仓库liamamilin/cognitive-language-engineering的main分支；推送触发在线电子书构建与部署，实际上线状态以Actions输出为准。旧完整正文在archive/full-v0.5-frozen，旧结构核心正文与manifest保留；新方法和整套教学方案默认E0，文档检查不证明效果。
