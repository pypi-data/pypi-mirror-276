# vscode-py-template

环境是以 MacOS、Linux 为基准。

## 设置

1. 确定项目名称为 `myproject`（假名），并更改目录名称
    - 此时 `myproject` 应为 Python 可导入的名称。（例如 `tensorflow`、`torch`、`Flask`）
    - 请使用由小写字母组成的单个单词。*如果有像 '_' 这样的字符太多会显得不够优雅。*
    - 同时更改 `Makefile` 中的 `PROJECT` 变量值。
    - 同样更改 `pyproject.yaml` 中的 `name` 变量值。
2. 准备并激活虚拟环境，然后运行 `make install` 命令。
    - `make install` 会以开发模式安装包。
    - 由于是以开发模式安装，它会在虚拟环境的 `site-package` 目录下创建软链接。
    - 在使用相同虚拟环境的项目中，可以导入并使用这个 `myproject`（假名）。在这种情况下，如果在当前项目文件夹内进行修改，由于有了链接，其他项目使用 `myproject` 时会立即反映这些修改，无需额外更新。当然，如果已经导入了特定模块，则需要关闭并重新打开 Python。
3. 如果使用 Discord，请指定 GitHub Action 的秘密变量 `DISCORD_WEBHOOK_URL`。
    - 将要发送通知的 Discord 频道的 Webhook URL 作为值进行注册。
    - 相关操作在 [ci-discord-noti.yml](.github/workflows/ci-discord-noti.yml) 中。

## `Makefile`

`Makefile` 具有以下功能。

### `make lint`

- 若要使用 `.vscode` 设置，请安装 `pylint` 扩展。
- 使用 linter 的默认设置，覆盖在 `pyproject.toml` 文件中指定的选项，对代码进行 lint。

### `make format`

- 使用 google 的 `yapf` 作为格式化工具。
- 使用 `yapf` 格式化代码时，会覆盖在 `pyproject.toml` 文件中指定的选项。
- 若要使用 `.vscode` 设置，请安装 `yapf` 扩展。

### `make test`

- 使用 `unittest` 进行测试。
- 支持 `test_*.py` 和 `*_test.py` 两种模式。
- 测试文件必须与 `__init__.py` 相连接。

### `make publish`

- 请按以下格式编写 `~/.pypirc` 文件。
    ```
    [pypi]
    username = __token__
    password = pypi-xxxxxx # 请获取个人 API 令牌并填写
    ```
- 运行此命令将使用 `flit` 将包推送到 PyPI 公共注册表。
- 之前指定的 `myproject`（假名）将被上传，全球任何人都可以通过 `python3 -m pip install myproject` 安装并使用该包。