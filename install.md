### 1. 创建虚拟环境

- uv init
- uv venv

### 2. 激活虚拟环境

#### 2.1. Windows

- .venv\Scripts\activate

#### 2.2. Linux / macOS

- source .venv/bin/activate

### 3. 安装依赖

- pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
- set UV_CACHE_DIR=D:\Workspace\PycharmProjects\uv-cache
- uv add fastapi[standard] sqlalchemy asyncmy qdrant-client "elasticsearch[async]>=8,<9" langchain langchain-huggingface
  langgraph jieba omegaconf pyyaml loguru cryptography

### 4. 锁定和重安装依赖

- uv sync

### 5. Embedding模型下载

- https://www.modelscope.ai/models/BAAI/bge-large-zh-v1.5/files

### 6. 启动Docker容器

- wsl --install (Windows OS)
- $env:DOCKER_BUILDKIT=0 (Windows OS) | export DOCKER_BUILDKIT=0 (Linux | MacOS)
- cd docker
- docker compose up -d
- docker compose down

