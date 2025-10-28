# Python 环境搭建指南

本指南将帮助您在 macOS 系统上搭建完整的 Python 开发环境。

## 📋 目录

- [系统要求](#系统要求)
- [安装 Python](#安装-python)
- [配置虚拟环境](#配置虚拟环境)
- [安装项目依赖](#安装项目依赖)
- [验证安装](#验证安装)
- [常见问题](#常见问题)

## 🔧 系统要求

- **操作系统**：macOS 10.15+
- **Python 版本**：Python 3.10 或更高版本
- **推荐**：Python 3.12+

## 📦 安装 Python

### 方法一：使用 Homebrew 安装（推荐）

Homebrew 是 macOS 上最流行的包管理器。

#### 1. 安装 Homebrew

```bash
# 打开终端，执行以下命令
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. 安装 Python 3.12

```bash
# 安装最新版本的 Python
brew install python@3.12

# 验证安装
python3 --version
# 应该输出: Python 3.12.x
```

#### 3. 检查安装位置

```bash
which python3
# 通常输出: /opt/homebrew/bin/python3
```

### 方法二：使用 pyenv 管理多个版本（可选）

如果您需要管理多个 Python 版本，推荐使用 pyenv。

```bash
# 1. 安装 pyenv
brew install pyenv

# 2. 配置环境变量（添加到 ~/.zshrc）
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# 3. 重新加载配置
source ~/.zshrc

# 4. 安装 Python 3.12
pyenv install 3.12.0

# 5. 设置为全局版本
pyenv global 3.12.0

# 6. 验证
python --version
```

### 方法三：从官网下载安装

访问 [Python 官网](https://www.python.org/downloads/) 下载 macOS 安装包。

## 🛠️ 配置虚拟环境

### 什么是虚拟环境？虚拟环境的作用

虚拟环境（Virtual Environment）是 Python 提供的一种工具，用于为每个项目创建独立的 Python 运行环境。每个虚拟环境都有自己独立的包管理空间，可以独立安装、升级或卸载第三方库，而不会影响到全局的 Python 环境，亦不会影响到其他项目。

#### 作用和优点

- **依赖隔离**：不同项目可以使用不同版本的包，互不干扰，避免“版本地狱”。
- **降低风险**：不会污染全局 Python 环境，降低操作失误带来的系统混乱；
- **简化部署**：直接打包/复制项目目录（含虚拟环境及依赖），即可一键部署到服务器或他人电脑；
- **必备能力**：几乎所有 Python 项目开发都建议使用虚拟环境。

#### 举例说明

例如：你有两个项目——
- **项目A** 需要 `Django==3.2`
- **项目B** 需要 `Django==4.0`

如果不用虚拟环境，全局只能安装一个 Django 版本，项目切换时很容易报错。
如果为每个项目建立独立的虚拟环境，各自安装各自需要的 Django 版本，两者互不影响。

#### 常见虚拟环境工具

- `venv`（Python3内置，推荐使用）
- `virtualenv`
- `conda`（Anaconda 环境）

> ✅ **开发任何 Python 项目前，建议优先创建虚拟环境。**


### 1. 进入项目目录

```bash
cd /Users/zhifeixie/my-github/ai-developer-backend/backend
```

### 2. 创建虚拟环境

```bash
# 使用 python3 创建虚拟环境
python3 -m venv venv

# 虚拟环境已创建在 venv 目录
```

> **命令解析**：

- `python3 -m venv venv` 这条命令含义如下：

    - `python3`：调用当前系统的 Python 3 解释器。
    - `-m venv`：使用 Python 内置的 `venv` 模块（用于创建虚拟环境）。
    - `venv`：指定虚拟环境的目录名称，这里会在当前目录下创建一个名为 `venv` 的文件夹。

- 执行后，会在当前目录生成一个 `venv` 文件夹，里面包含独立的 Python 解释器及包管理工具，所有后续依赖包都将安装在此虚拟环境路径下，不影响全局 Python 配置。

> **为什么要把虚拟环境目录命名为 `venv`？**
>
> 这是业界约定俗成的习惯。你也可以自定义名称，比如 `env`、`.venv`，但推荐使用 `venv`，便于协作和识别。


### 3. 激活虚拟环境

```bash
# macOS/Linux
source venv/bin/activate

# 激活后，终端提示符会显示 (venv)
```

> **命令解析**：
>
> - `source venv/bin/activate` 这一命令作用是激活刚刚创建的虚拟环境。
> - 激活后，终端的提示符前会出现 `(venv)`，表示当前在该虚拟环境下运行 Python。
> - 此时你安装的所有 Python 包、使用的 Python 解释器版本都仅影响当前项目目录，不会影响系统其它项目或全局设置。


### 4. 验证虚拟环境

```bash
# 查看 Python 解释器位置
which python
# 应该输出: /Users/zhifeixie/.../venv/bin/python

# 查看 Python 版本
python --version
```

### 5. 退出虚拟环境

```bash
# 完成开发后，执行以下命令退出
deactivate
```

## 📚 安装项目依赖

### 1. 升级 pip

```bash
# pip 是 Python 的包管理工具
pip install --upgrade pip
```

### 2. 安装项目依赖

```bash
# 安装 requirements.txt 中的所有依赖
pip install -r requirements.txt
```

### 3. 验证关键依赖

```bash
# 检查 FastAPI 是否安装成功
python -c "import fastapi; print(f'FastAPI 版本: {fastapi.__version__}')"

# 检查 SQLAlchemy 是否安装成功
python -c "import sqlalchemy; print(f'SQLAlchemy 版本: {sqlalchemy.__version__}')"
```

## ✅ 验证安装

### 完整检查脚本

```bash
# 1. 检查 Python 版本
python --version
# 输出: Python 3.12.x

# 2. 检查 pip 版本
pip --version
# 输出: pip 24.0 from ...

# 3. 检查虚拟环境
which python
# 应该包含 venv

# 4. 列出已安装的包
pip list
# 应该看到 fastapi, sqlalchemy, uvicorn 等
```

## 🎯 开发环境配置清单

完成以下所有项，您的开发环境就搭建好了！

- [ ] Python 3.10+ 已安装
- [ ] 虚拟环境已创建并激活
- [ ] 项目依赖已安装
- [ ] 可以导入 FastAPI 模块
- [ ] 可以导入 SQLAlchemy 模块

## 🔍 常见问题

### 1. 提示 "python: command not found"

**问题原因**：系统找不到 Python 解释器

**解决方案**：
```bash
# 检查是否安装了 Python
which python3

# 如果没有，安装 Python
brew install python@3.12

# 添加到 PATH（如果需要）
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 2. 虚拟环境中还是使用了系统 Python

**问题原因**：虚拟环境创建失败或未激活

**解决方案**：
```bash
# 删除旧虚拟环境
rm -rf venv

# 重新创建
python3 -m venv venv

# 激活（很重要！）
source venv/bin/activate

# 验证
which python
```

### 3. 安装依赖包速度慢

**解决方案**：使用国内镜像源

```bash
# 临时使用清华镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 永久配置（推荐）
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 4. 提示 "This application requires Python 3.10 or later"

**问题原因**：Python 版本过低

**解决方案**：
```bash
# 检查当前版本
python3 --version

# 如果版本低于 3.10，需要升级
brew install python@3.12
```

### 5. 多个 Python 版本如何选择

**解决方案**：使用 pyenv 管理多个版本

```bash
# 查看所有版本
pyenv versions

# 切换全局版本
pyenv global 3.12.0

# 或为当前项目设置版本
pyenv local 3.10.13
```

## 总结

简单流程如下：
1. 创建并激活虚拟环境
2. （可选）升级虚拟环境内的 pip
3. 安装项目依赖

示例：
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip  # 升级的是 venv 目录下的 pip
pip install -r requirements.txt
```

## 💡 小贴士

1. **始终使用虚拟环境**：避免污染系统 Python 环境
2. **定期更新依赖**：`pip install --upgrade package-name`
3. **备份 requirements.txt**：记录当前项目的所有依赖
4. **使用 .gitignore**：忽略 venv 目录，不要提交到 Git




