# 06 Codex 配置

## 官方技能目录

Codex 官方文档支持的 skill 位置主要包括：

- 仓库级：`.agents/skills/`
- 用户级：`~/.agents/skills/`
- 管理员级：`/etc/codex/skills`

Codex 支持两种使用方式：

- 显式调用：在 prompt 中提到 skill，或使用 `/skills`
- 隐式调用：当任务与 skill 的 `description` 匹配时自动选择

## MeOS 推荐安装方式

因为 skill 名是 `meos`，建议安装时使用**小写目录名**。

### 用户级

```bash
mkdir -p ~/.agents/skills
ln -s /path/to/MeOS ~/.agents/skills/meos
```

### 仓库级

```bash
mkdir -p .agents/skills
ln -s /path/to/MeOS .agents/skills/meos
```

如果不方便用软链接，也可以复制到一个名为 `meos` 的目录中。

## 如何使用

### 初始化

```text
Use meos in init mode. Build the first sanitized operating-layer assets from the local history sources.
```

### 刷新

```text
Use meos in refresh mode. Update the existing MeOS assets from newly added local history without duplicating stale rules.
```

### 应用

```text
Use meos in apply mode for this task. Read only the minimum relevant assets and follow the owner's SOP, preferences, and correction rules while you work.
```

## 备注

- `description` 要写得足够具体，这样 Codex 才更容易自动触发。
- 如果更新后的 skill 没有立即生效，重启 Codex 是最稳妥的做法。
