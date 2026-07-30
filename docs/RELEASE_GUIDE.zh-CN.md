# 第一次用 Codex 发布到 GitHub：完整操作手册

本手册对应公开版本：`v0.1.0-alpha`。

## 你会用到两个 ZIP

1. **仓库源码包**：`godot-game-development-director-v0.1.0-alpha-public-release.zip`  
   解压后让 Codex 初始化 Git、创建仓库并推送。
2. **Release 附件包**：`dist/godot-game-development-director-v0.1.0-alpha.zip`  
   不需要提交进 Git；创建 GitHub Release 时作为下载附件上传。

GitHub 会自动为 Tag 生成 Source code ZIP，但那个只是仓库快照。这里单独构建的 Release 附件带有项目指定目录结构和 SHA-256 校验。

## 发布前准备

你需要：

- GitHub 账号
- 本机安装 Git
- 安装 GitHub CLI `gh`
- Codex 可以访问解压后的仓库目录
- 允许 Codex 运行 `git` 和 `gh` 命令

先在终端确认：

```bash
git --version
gh --version
```

登录 GitHub：

```bash
gh auth login
```

选择 GitHub.com、HTTPS 和浏览器登录。完成后检查：

```bash
gh auth status
```

## 给 Codex 的完整提示词

把源码包解压后，在该目录打开 Codex，然后粘贴下面的任务：

```text
你正在处理 Godot Game Development Director 的首次公开发布。

目标版本：v0.1.0-alpha
建议仓库名：godot-game-development-director
默认可见性：public

先执行只读检查：
1. 阅读 README.md、README.zh-CN.md、RELEASE_NOTES.md、LICENSE、SECURITY.md、AGENTS.md。
2. 运行：python -m pip install -r requirements-dev.txt
3. 运行：python scripts/validate_public_release.py
4. 运行：python tests/validate_package.py
5. 运行：python -m unittest discover -s tests -v
6. 运行：python scripts/build_release.py --version v0.1.0-alpha
7. 检查 dist/godot-game-development-director-v0.1.0-alpha.zip 和 dist/SHA256SUMS。

在任何联网写操作前，告诉我：
- 当前 gh 登录账号
- 准备创建的 owner/repository
- 仓库是否 public
- 将要执行的完整命令
等待我确认后再继续。

确认后：
1. 如果当前目录不是 Git 仓库，执行 git init -b main。
2. git add .，但不要强行加入被 .gitignore 排除的 dist/。
3. 创建提交：chore: publish v0.1.0-alpha preview
4. 使用 gh repo create 创建 public 仓库并推送 main。
5. 创建并推送 annotated tag v0.1.0-alpha。
6. 使用 gh release create 创建 pre-release，标题为：
   Godot Game Development Director v0.1.0-alpha
7. 发布说明使用 RELEASE_NOTES.md。
8. 上传 dist/godot-game-development-director-v0.1.0-alpha.zip 和 dist/SHA256SUMS。
9. 最后用 gh repo view 和 gh release view 验证，并返回仓库 URL、Release URL、Tag 和附件列表。

安全要求：
- 不修改仓库可见性，除非我再次确认。
- 不删除远程仓库、分支、Tag 或 Release。
- 不使用 --force。
- 不提交凭证、.env、私钥、export_credentials.cfg、.godot 或 dist。
- 如果仓库已存在或名称冲突，停止并向我报告，不要覆盖。
```

## 手动命令参考

在解压后的源码目录中：

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_public_release.py
python tests/validate_package.py
python -m unittest discover -s tests -v
python scripts/build_release.py --version v0.1.0-alpha
```

初始化：

```bash
git init -b main
git add .
git commit -m "chore: publish v0.1.0-alpha preview"
```

检查将要提交的文件：

```bash
git status --short
git ls-files | grep -E '(^|/)(\.env|export_credentials\.cfg|\.godot)(/|$)' && echo "STOP: sensitive/generated file found" || true
```

创建仓库并推送。将 `<OWNER>` 换成你的 GitHub 用户名或组织名：

```bash
gh repo create <OWNER>/godot-game-development-director \
  --public \
  --source=. \
  --remote=origin \
  --push
```

创建 Tag：

```bash
git tag -a v0.1.0-alpha -m "Godot Game Development Director v0.1.0-alpha"
git push origin v0.1.0-alpha
```

创建预发布并上传附件：

```bash
gh release create v0.1.0-alpha \
  dist/godot-game-development-director-v0.1.0-alpha.zip \
  dist/SHA256SUMS \
  --title "Godot Game Development Director v0.1.0-alpha" \
  --notes-file RELEASE_NOTES.md \
  --prerelease
```

验证：

```bash
gh repo view --web
gh release view v0.1.0-alpha
```

## GitHub 页面建议设置

进入仓库：

- **About**：添加说明和 topics，例如 `godot`、`game-development`、`agent-skills`、`game-design`、`procedural-generation`。
- **Settings → General**：确认默认分支是 `main`。
- **Settings → Security**：启用 Private vulnerability reporting。
- **Actions**：确认 `Validate` 工作流通过。
- **Releases**：确认 `v0.1.0-alpha` 标记为 Pre-release，并有两个附件。

## 常见错误

### `gh: command not found`

安装 GitHub CLI 后重新打开终端。

### `gh auth status` 显示未登录

运行 `gh auth login`，不要把 Token 粘贴进仓库文件或聊天记录。

### 仓库名已存在

不要覆盖。换一个仓库名，或者明确选择已有空仓库后再添加 remote。

### `remote origin already exists`

先检查：

```bash
git remote -v
```

只有确认地址错误后才修改：

```bash
git remote set-url origin https://github.com/<OWNER>/godot-game-development-director.git
```

### Release 已存在

查看：

```bash
gh release view v0.1.0-alpha
```

不要直接删除。确认是同一个版本后，可以用 `gh release upload --clobber` 更新附件；如果内容已经变化，优先发布新版本。

### Actions 测试失败

不要发布稳定版。先打开失败日志，修复后重新推送。Alpha 可以保留，但 Release Notes 必须诚实记录未通过项。

## 发布完成检查表

- [ ] `main` 分支包含源码而不是只有一个 ZIP
- [ ] `LICENSE` 能被 GitHub 识别
- [ ] README 首页正常显示
- [ ] Actions Validate 通过
- [ ] Tag 为 `v0.1.0-alpha`
- [ ] Release 为 Pre-release
- [ ] Release 有 ZIP 和 `SHA256SUMS`
- [ ] Release Notes 明确已验证和未验证内容
- [ ] 仓库中没有 `.env`、私钥、Token、`.godot/` 和 `export_credentials.cfg`
- [ ] 没有把第三方商业素材打包上传

## 可选：使用 GitHub Actions 构建附件

仓库包含 `.github/workflows/release.yml`。它默认不会因推送 Tag 自动发布，避免与 Codex 的手动 `gh release create` 重复。

需要使用时：

1. 打开 GitHub 仓库的 **Actions** 页面。
2. 选择 **Build or publish release**。
3. 点击 **Run workflow**。
4. 填写版本，例如 `v0.1.0-alpha`。
5. 首次建议让 `publish` 保持关闭，只下载并检查工作流生成的附件。
6. 确认无误后，才在下一次执行时启用 `publish`。

## 官方命令参考

- GitHub CLI 登录：https://cli.github.com/manual/gh_auth_login
- 从现有目录创建仓库：https://cli.github.com/manual/gh_repo_create
- 创建 GitHub Release：https://cli.github.com/manual/gh_release_create
- GitHub Release 页面操作：https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository
- Codex 入门：https://openai.com/codex/get-started/
- Codex 的 `AGENTS.md` 作用域说明：https://openai.com/index/introducing-codex/

