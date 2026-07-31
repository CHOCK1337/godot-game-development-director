# Codex + GitHub 安全发布手册

本手册对应候选版本 `v0.1.0-alpha.1`。发布是外部写操作；检查和构建可以自动执行，提交、推送、创建标签与 Release 必须由仓库所有者明确确认。

## 发布物

- Git 仓库：源码、文档、测试和工作流。
- Release 附件：`dist/godot-game-development-director-v0.1.0-alpha.1.zip`
- 校验文件：`dist/SHA256SUMS`
- GitHub attestation：由 Release 工作流为 ZIP 生成。

GitHub 自动生成的 Source code ZIP 是标签快照，不等同于本项目构建的确定性附件。

## 0. 基本条件

```bash
git --version
gh --version
gh auth status
```

不要把 Token、`.env`、私钥、Godot 导出凭证或私有项目材料放进仓库或聊天记录。

## 1. 本地只读检查

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_public_release.py
python tests/validate_package.py
python -m unittest discover -s tests -v
python scripts/run_godot_validation.py --godot /Godot4/可执行文件路径
```

只有真实执行过最后一条命令，才能声称完成本地 Godot 编译与烟测。CI 会另行使用固定 Godot 4.6.3 和固定 SHA-256。

## 2. 构建附件

```bash
python scripts/build_release.py --version v0.1.0-alpha.1 --clean
```

检查：

```bash
git status --short
python -c "from pathlib import Path; print((Path('dist')/'SHA256SUMS').read_text())"
```

`dist/` 不需要提交到 Git；工作流会从标签源码重新构建。

## 3. 提交前人工门禁

发布者应确认：

- 当前 `main` 是准备发布的源码；
- `CHANGELOG.md`、`RELEASE_NOTES.md`、`README.md`、`README.zh-CN.md` 和 `CITATION.cff` 版本一致；
- 所有门禁通过；
- `git diff --check` 无错误；
- 没有凭证、生成缓存、`.godot/`、本地存档或第三方商业素材；
- 远程仓库、可见性和目标版本正确。

创建提交：

```bash
git add .
git commit -m "chore: prepare v0.1.0-alpha.1"
git push origin main
```

不要使用 `--force`。

## 4. 先建不可变标签

确保本地 `HEAD` 与远程 `main` 是同一提交，再创建 annotated tag：

```bash
git status --short
git rev-parse HEAD
git rev-parse origin/main
git tag -a v0.1.0-alpha.1 -m "Godot Game Development Director v0.1.0-alpha.1"
git push origin v0.1.0-alpha.1
```

标签一旦公开就不应移动。如果内容发生变化，发布新版本，不要重打同名标签。

## 5. 推荐：用 GitHub Actions 发布

1. 打开仓库的 **Actions**。
2. 选择 **Build or publish release**。
3. 运行时将 ref 选择为刚创建的 `v0.1.0-alpha.1`。
4. `version` 填 `v0.1.0-alpha.1`。
5. 首次运行保持 `publish=false`，下载 workflow artifact 并核对 ZIP 和 SHA。
6. 确认后再次从同一标签运行，设置 `publish=true`。

工作流会：

- 校验标签已经存在，且指向本次运行验证的提交；
- 下载官方 Godot 4.6.3 并校验 SHA-256；
- 运行仓库、单元、安装、Doctor 和真实 GDScript 门禁；
- 构建 ZIP 与 `SHA256SUMS`；
- 为 ZIP 生成 attestation；
- 如果同名 Release 已存在则拒绝覆盖；
- 创建新的 pre-release。

工作流不会创建或移动标签，也不会 `--clobber` 已有附件。

## 6. 手动发布备选

只在工作流不可用且本地全部门禁通过时使用：

```bash
gh release view v0.1.0-alpha.1
```

如果上面的命令找到已有 Release，停止，不要删除或覆盖。若不存在：

```bash
gh release create v0.1.0-alpha.1 \
  dist/godot-game-development-director-v0.1.0-alpha.1.zip \
  dist/SHA256SUMS \
  --verify-tag \
  --title "Godot Game Development Director v0.1.0-alpha.1" \
  --notes-file RELEASE_NOTES.md \
  --prerelease
```

手动方式不会自动获得工作流的 artifact attestation，因此优先使用 Actions。

## 7. 发布后验证

```bash
gh repo view
gh release view v0.1.0-alpha.1
```

检查：

- 标签指向预期提交；
- Release 是 pre-release；
- 附件只有预期 ZIP 和 `SHA256SUMS`；
- SHA-256 与下载后的 ZIP 一致；
- Actions `Validate` 和发布工作流均为绿色；
- attestation 可在 GitHub 上验证；
- README 与 Release Notes 没有夸大尚未执行的项目级验证。

## 给 Codex 的授权边界模板

```text
先只读检查并构建 v0.1.0-alpha.1 候选包。
返回当前账号、remote、HEAD、目标标签、将执行的推送/发布命令和全部门禁结果。
在我明确回复“确认发布”前，不提交、不推送、不创建标签、不创建或修改 Release。
不得 force push、移动已有标签、覆盖已有 Release、改变仓库可见性或提交凭证。
```

## 常见故障

- **Tag 已存在但指向不同提交：** 停止，创建新版本号。
- **Release 已存在：** 停止；修复内容后发布新版本，不使用 `--clobber`。
- **Godot 下载哈希不一致：** 停止，不解压、不运行。
- **只有静态测试通过：** 不能声称 GDScript 已经在真实 Godot 中验证。
- **Doctor 报安装引用缺失：** 不发布；修复 Skill 自包含目录或安装器。
- **Actions 失败：** 修复后重新提交并创建新标签；不要移动已经公开的标签。

## 官方参考

- [GitHub CLI authentication](https://cli.github.com/manual/gh_auth_login)
- [Creating GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [Artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations)
- [Codex Skills](https://developers.openai.com/codex/skills/)
- [Codex plugins](https://developers.openai.com/plugins/build/plugins)
- [Godot command line](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)
