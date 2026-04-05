# 10 如何应用 MeOS

## 核心思想

MeOS 不应该只负责创建或刷新资产。
它真正的价值在于：让后续 agent 在任务中真正用上这些资产。

## `apply` 模式应该做什么

当 MeOS 以 `apply` 模式使用时，agent 应该：

1. 先识别当前任务类型
2. 只读取最相关的资产
3. 让这些资产影响：
   - 思考方式
   - 工作流程
   - 输出风格
   - 纠偏规则
4. 如果没有真正稳定的新信息，就不要随便改资产层

## 不同任务优先读哪些资产

### 技术实现任务

优先读：

- `assets/live/work/`
- `assets/live/thought-style/`
- `assets/live/workflow/`
- `assets/live/principles/`

### UI / 产品任务

优先读：

- `assets/live/taste/`
- `assets/live/work/`
- `assets/live/workflow/`
- `assets/live/corrections/`

### 研究 / 写作任务

优先读：

- `assets/live/work/`
- `assets/live/thought-style/`
- `assets/live/principles/`
- `assets/live/knowledge/`
- `assets/live/workflow/`

### 风格敏感型回复

优先读：

- `assets/live/preferences/`
- `assets/live/corrections/`

## 最高优先级

如果 `assets/live/corrections/` 中的规则与其他层冲突，以 correction 为准。
