# Cognitive Language Engineering｜认知语言工程

**project-v0.5.3 / Core v0.5（初步冻结） / 结构核心版 v0.2（已冻结） · 2026-10-01**

完整正式工程基线：四模型、跨域接口、机制、算子、模式、协议、案例、证据与评估。用于提升人对语言的主动控制能力，并长期修订。

v0.5 对整套体系再复核：分开状态、变化、达成与退出，补齐心智模型、使用演练、能力训练与失效诊断。沿用81接口、34算子、36模式与13协议。

从 [阅读入口](docs/index.md) 或 [使用指南](docs/START_HERE.md) 开始。内容完成范围见 [整合审查](docs/project/REVIEW_REPORT.md)，维护见 [维护约定](docs/project/MAINTENANCE.md)。原始材料、候选研究历史和v0.4基线均在archive快照中。

新增[结构核心版](docs/essentials/index.md)：保留六原则、四模型与九对象关系，主讲23个模型接口，保留8个支撑接口，优先学习7个机制家族、15个算子及对应主模式，完整保留PR05。逐项理由见[筛选审计](docs/essentials/SELECTION.md)。它使用独立阅读样式，在同一次构建中生成 `site/essentials/index.html`；母体系首页“阅读路线”保留入口。v0.2已于2026-10-01按用户要求冻结，原v0.5定义不变，冻结正文与校验清单保存在archive/structural-core-v0.2-frozen；后续打磨使用新版本。

## 阅读与构建

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/check_docs.py
python scripts/check_essentials.py
python -m mkdocs serve
```

终端输出本地地址。

修改模型正文后，先运行 `python scripts/update_registry.py` 更新派生快照；`python scripts/update_registry.py --check` 校验全部派生字段。

生成在线电子书：

```bash
python -m mkdocs build --strict
python scripts/check_site.py
```

生成目录 site 不属于正文来源。书籍以 Markdown → MkDocs Material → GitHub Pages 发布，配置已就绪，远程仓库已建立，首次文件上传受浏览器运行环境阻塞，尚无提交或公开部署；见 [发布说明](docs/project/PUBLISHING.md)。本版不提供 EPUB/PDF。

导出可离线阅读的完整 Markdown 和单文件 HTML 副本：

```bash
python scripts/export_book.py --output-dir reading
```

副本从正文生成，含全文目录和内部链接；修改仍以 docs 为准，不同时手工维护副本。

## 目录

| 路径 | 内容 |
| --- | --- |
| docs/CORE_SPEC.md、STATE_SPEC.md、EVIDENCE_SPEC.md、GLOSSARY.md | 核心、状态、证据、术语 |
| docs/models/ | M1—M4正式卡片 |
| docs/BRIDGES.md、OUTCOMES.md、MECHANISMS.md | 跨域、结果、过程解释 |
| docs/engineering/ | 组件、算子、模式、协议 |
| docs/applications/、evaluation/ | 案例、评估和边界 |
| docs/sources/ | 来源与旧引文审计 |
| docs/essentials/、overrides/、docs/assets/stylesheets/essentials.css | 结构核心版正文、筛选审计、独立页面模板和样式 |
| docs/project/、decisions/ | 状态、版本、维护、决策和发布 |
| scripts/ | 链接／ID／组件检查及派生快照 |
| archive/ | 初始项目原样快照 |

## Git 版本管理

解压后可使用自己的 Git 身份配置建立仓库：

```bash
git init -b main
git add .
git commit -m "Freeze structural core v0.2 based on CLE v0.5"
git tag project-v0.5.3
git tag cle-core-v0.2
```

当前交付不包含用户身份、虚构远程地址或已经部署的链接。默认发布最新在线阅读版；历史快照由 Git 标签管理。
