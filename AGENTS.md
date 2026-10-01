# CLE 文档维护指令

1. 先读 README、docs/project/STATUS.md、MAINTENANCE.md及相关正文。docs 是权威来源，缺失上下文标未知。
2. 当前 project-v0.5.0 是已授权的正式整合基线；原始六文件和初始候选历史在 archive 中。保留 ID 和变更依据。
   project-v0.5.1 增加实用核心 v0.1。用户已初步冻结 Core v0.5；母体系定义维持冻结清单内容，子体系单独修订。用户已授权首页“阅读路线”添加入口及必要网站／维护配置。
   project-v0.5.2按用户修正将子体系改为保留原结构的v0.2。当前project-v0.5.3按用户要求冻结该版。不得再以泛用问句替代核心模型和机制；运行check_essentials.py检查筛选与组成闭包。子体系v0.2已冻结；保留archive/structural-core-v0.2-frozen快照，后续内容打磨另立新版本。
3. 用户在会话中已授权的工作直接完成，无需重复批准。冻结可经授权修订；不把规范接受与效果证据混为一谈。
4. 新 Primitive 前检查复用；P 表示工程粒度，Specialization 不宣称新增独立机制。ID 不复用给无关概念。
5. 改模型或组件时同步 Core、依赖页、案例、边界、导航、快照、STATUS和CHANGELOG；重要变更写 decisions。
6. 案例明确区分构造示范与实际观察；引文记录读取深度，未读全文不得猜测效果。
7. 执行 python scripts/check_docs.py 和 python -m mkdocs build --strict；失败定位后修复，再更新构建报告。
8. registry_snapshot.json是派生检查材料，正文为主。release-manifest.json在正式打包时更新。
9. 不自行扩展为应用开发或效果研究；GitHub公开提交和发布按用户会话范围处理，不虚构链接。
