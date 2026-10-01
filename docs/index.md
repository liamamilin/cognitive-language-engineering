# 认知语言工程

**Cognitive Language Engineering · v0.5 正式工程基线 · 2026-10-01**

提升人对语言的主动控制能力，让语言更有效地服务于思考、表达、影响、协作与行动。

这本书从人的目的出发，区分语言改变了什么、可能怎样改变，以及怎样设计操作并检查结果。四个模型组织表征、个体认知、共享互动和社会行动；算子提供可调用工具，协议提供任务过程，结果与评估完成反馈闭环。

## 阅读路线

- 从原体系的核心版本开始：读[结构核心版](essentials/index.md)，保留六原则与四模型，优先掌握高复用、重要的组件；筛选依据见[取舍审计](essentials/SELECTION.md)。基于初步冻结的 v0.5。
- 先建立整体理解：读[五个心智模型](MENTAL_MODELS.md)，再做[使用规格](engineering/RUN_SPEC.md)中的演练。
- 要形成独立调用能力：按[训练路径](learning/TRAINING.md)换例练习，失效时用[诊断](evaluation/FAILURE_ANALYSIS.md)。
- 想直接使用：从[使用指南](START_HERE.md)选择任务，再看[应用案例](applications/CASES.md)。
- 想理解体系：先读[核心目的](PURPOSE.md)和[核心规范](CORE_SPEC.md)，再读[术语表](GLOSSARY.md)与四模型。
- 想设计语言操作：读[组件规范](engineering/COMPONENT_SPEC.md)、[算子](engineering/OPERATORS.md)、[语言模式](engineering/PATTERNS.md)与[协议](engineering/PROTOCOLS.md)。
- 想检查可靠性：读[评估](evaluation/EVALUATION.md)、[边界案例](evaluation/BOUNDARY_CASES.md)、[证据规范](EVIDENCE_SPEC.md)与[来源](sources/VERIFIED_SOURCES.md)。

## 本版内容

| 层 | 内容 | 作用 |
| --- | --- | --- |
| 基础 | 九对象、六原则、术语、状态／证据规范 | 统一定义与主张范围 |
| 模型 | M1 8、M2 35、M3 9、M4 29 个接口 | 总计 81 个登记接口，含 4 个特化，不是 81 个独立心理机制 |
| 连接 | 8 个 Bridge、3 个 Outcome | 连接认知、互动、行动与反馈 |
| 解释 | 12 个机制家族 | 按主张区分候选过程与局部文献支持 |
| 工程 | 34 个算子、36 个模式、13 套协议 | 用任务和状态选择语言操作 |
| 学习与使用 | 心智模型、使用规格、六组训练与失效分析 | 从识别到独立选择和迁移检查 |
| 应用与检查 | 5 个构造案例、32 个边界案例、评估规范 | 检查能否调用、怎样失败与如何验证 |
| 维护 | 决策、版本、来源审计与在线电子书配置 | 长期修改和发布 |

正式工程基线表示定义与组件已整合并可据此使用、检验和修订；效果与迁移需独立验证。原始材料及初始项目快照保留在 archive。本版没有必须等待回写的候选章节。
