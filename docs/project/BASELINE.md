# 基线与追溯

## 初始基线

用户上传《核心.md》《认知语言工程V 0.3 核心体系.md》和 M1—M4 六份文件。初始 project-v0.1.0 逐字保存附件，并建立阅读和维护配置。当前 archive/CLE_Document_Project_v0.1.0.zip 保存初始项目，根目录 baseline-manifest.json 保留当时摘要；该清单不是当前版本的内容摘要。

## v0.4 的变化

正式名称统一；保留所有初始 Transition ID。M2 新增 C-P16—C-P21 与 C-C13—C-C14；M4 新增 A-C13。C-P9/C-P10/C-P12/C-P19 明确为特化。原有条目的定义和边界经过修订，详见模型卡片与 CHANGELOG。

早期目标、期望变化、评价标准候选稿已整合：C-P16/C-P17/C-P18、C-C6/C-C7/C-C8、OP15—OP18 与 PR02/PR03；历史研究页保留在初始快照，不作为当前并行规范。

当前 release-manifest.json 记录本版源文件 SHA-256，便于追溯正式交付；它不包括自身，正文修改后应更新。派生的 scripts/registry_snapshot.json 服务于检查，不替代模型正文。

## v0.5 追溯

archive/CLE_Document_Project_v0.4.0.zip 保留上次完整正式快照，本轮不覆盖。v0.5 修调用、观察和达成语义，保持全部81个ID。跨域过程从组成移到单独引用，原关系可由v0.4快照追溯；新增教学、使用和诊断内容见决策004。

当前清单和快照在交付前重建。update_registry.py 从模型正文导出 registry_snapshot.json，check_docs.py 比较全部派生字段；正文是权威来源。
