# SDD Development Skill

本目录是 sdd-development Skill 的正式本地源仓库。

## 目录职责

- SKILL.md：Skill 入口、触发边界和上游输入门；
- references/：流程、交付协议、文档纪律和 handoff 兼容规则；
- gotchas.md：经过实际开发验证的踩坑规则；
- .run-log.jsonl：Skill 自迭代操作日志，不注入默认上下文。

## 使用关系

three-space-development 负责：

Problem → Intention → Specification → Solution Architecture

sdd-development 负责：

Approved Specification → Issue → Plan → Implementation → Verification → Delivery

本目录是可编辑、可审阅、可回滚的源目录。运行时安装副本位于用户 Skill 目录。修改完成后，应先在本地完成检查，再同步安装副本并记录变更。

## 跨 Skill 契约

SDD 不拥有上游规格的定义权，只消费并验证 SDD Handoff Contract。

当前兼容说明：

references/three-space-handoff-compatibility.md

支持的契约版本：

0.1.0

## GitHub 更新流程

1. 从 main 创建任务分支；
2. 只修改 SDD 职责范围内的文件；
3. 小步提交，提交信息说明真实变更；
4. 推送到已明确配置的远程分支；
5. 创建 PR，写明测试、影响范围和契约版本；
6. Review 后合并到 main；
7. 创建版本标签；
8. 再同步运行时安装副本。

main 不直接提交。当前仓库尚未配置远程，配置前不得向未知地址推送。

## 版本规则

- Patch：文字、示例或不改变语义的修正；
- Minor：新增兼容字段或兼容行为；
- Major：删除字段、改变语义或改变交接流程。

## 实现偏差回流

如果实现发现规格缺失、冲突或不可行，提交 Specification Change Request，返回 three-space-development 重新审查。实现细节问题留在 SDD 内部解决。

## 当前状态

- 本地 Git：已建立；
- 远程 GitHub：待用户确认仓库名称和可见性；
- Handoff Contract：已接入 v0.1.0。
