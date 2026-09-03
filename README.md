# SDD Development Skill

本目录是 `sdd-development` skill 的正式本地源仓库。

## 目录职责

- `SKILL.md`：skill 入口和触发边界；
- `references/`：流程、产物、文档纪律和 issue 前置检查；
- `gotchas.md`：经过实际开发验证的踩坑规则；
- `.run-log.jsonl`：skill 自迭代操作日志，不注入默认上下文。

## 使用关系

本目录是可编辑、可审阅、可回滚的源目录；运行时安装副本位于用户 skill 目录。修改完成后，应先在本地完成检查，再同步安装副本并记录变更。

本仓库当前只注册本地 Git，不配置远端。需要发布或同步到远端时，必须由用户明确指定远端地址和动作。

## 当前基线

- 交付协议：摘要优先，源文件可追溯；
- Review：plan review 与 implementation review 分开；
- 效果：区分确定、可能、未知，不作无证据的乐观承诺；
- 生效日期：2026-09-03。
