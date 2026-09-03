---
name: sdd-development
description: >
  当项目采用文档驱动开发（SDD，docs/issues + docs/plans 结构）时，开始新功能、
  修复、重构或迁移任务，或用户要求"写 issue"、"做 plan"、"开始开发"、
  "implement"、"按流程走"等涉及代码交付的请求时触发。
  关键词：写issue、写plan、做plan、SDD、开发流程、按流程走、开始开发、
  实现功能、需求确认、计划评审、计划确认。
  当用户只是纯问答、纯调研、或单文件小改动（可直接做、事后补文档）时，不应触发。
---

# SDD 开发流程

> 仿 [Harness Engineering 实践](https://blog.xlab.app/p/c3ac2cfd/)（ttttmr）。
> 核心信念：**文档是 Agent 的上下文底座**——一切需要被知道的知识都应文档化，人只做决策。

## 文件地图

> 路径均相对于本 skill 目录。按需读取，不一次性全量加载。

| 文件 | 何时读 |
|------|--------|
| [references/workflow.md](references/workflow.md) | 开始任何开发任务时（九步循环 + 各步骤要求） |
| [references/issue-precheck.md](references/issue-precheck.md) | 写 issue 前、对「要解决什么」不确定时（可选） |
| [references/artifacts.md](references/artifacts.md) | 编写 plan / 汇报合并时（人决策所需信息，硬性要求） |
| [references/docs-discipline.md](references/docs-discipline.md) | 涉及创建/更新文档时（五层映射、doc-contract、INDEX） |
| [gotchas.md](gotchas.md) | 遇到问题、收尾检查、或准备跳过流程步骤时 |

## 依赖技能

- **doc-contract**：创建/更新/归档 issue、plan 等文档时遵循其 frontmatter 与状态规则
- **sdd-plan-report**：编写 plan 时按其模板产出（摘要/原因/预计效果/关键决策/review 发现/实现步骤/测试/验收）
- **project-doc-architecture / docs-scan**：涉及文档目录结构与 INDEX.md 维护时使用

## 工作流程

```
① 提出/确认 issue → ② 编写 plan → ③ plan 独立 review → ④ 人确认 plan
→ ⑤ 实现 → ⑥ 实现独立 review → ⑦ 测试验证 → ⑧ 人确认合并 → ⑨ 归档
```

- 未确认 plan 不得进入实现（用户明确豁免的小改动除外）
- 每完成一个阶段，向用户汇报当前状态与下一步

## 关键原则

1. **先文档后代码**：没有 plan 就不写实现
2. **规格在 docs 里，不在对话里**：不依赖对话记忆，随时可从文档恢复任务
3. **人确认两件事**：确认 Plan、确认合并；为此产物必须满足 artifacts 硬性要求
4. **文档即交付物**：改完代码同步更新文档，INDEX.md 同步

## 阅读交付协议

对用户汇报 SDD 产物时，默认采用“摘要优先、源文件可追溯”的双层交付：

- **Issue 摘要**只回答问题、影响、优先级建议、是否值得进入 plan 和待用户决定的事项；
- **Plan 摘要**只回答解决思路、关键取舍、保守的效果分级（确定 / 可能 / 未知）和待确认决策；
- 实施步骤、测试细节和完整 review 仍写入源文件，但默认不复制到汇报消息；用户要求时再展开；
- review 必须先由 Agent 完成并吸收进最终 plan，不能把原始 review 噪声直接交给用户；
- 没有基线或验证条件时，效果写“未知”，禁止承诺“显著提升”“完全解决”等无证据结论。

## 自迭代规则

- 每次调用后，如发现新的踩坑点，询问用户是否记录到 [gotchas.md](gotchas.md)
- 操作日志追加到 [.run-log.jsonl](.run-log.jsonl)（不注入 context）
- 累计约 10 条后，主动询问用户是否总结日志为 gotcha
