# Product Hunt 每日中文热榜

[English](README.en.md) | [中文](README.md)

![License](https://img.shields.io/github/license/ViggoZ/producthunt-daily-hot) ![Python](https://img.shields.io/badge/python-3.x-blue)

Product Hunt 每日热榜是一个基于 GitHub Action 的自动化工具，它能够每天定时生成 Product Hunt 上的热门产品榜单 Markdown 文件，并自动提交到 GitHub 仓库中。该项目旨在帮助用户快速查看每日的 Product Hunt 热门榜单，并提供更详细的产品信息。

榜单会在每天下午4点自动更新，可以在 [🌐 这里查看](https://decohack.com/category/producthunt/)。

## 预览

![Preview](./preview.gif)

## 功能概述

- **自动获取数据**：每天自动获取前一天的 Product Hunt Top 30 产品数据。
- **关键词生成**：生成简洁易懂的中文关键词，帮助用户更好地理解产品内容。
- **高质量翻译**：使用 OpenAI 的 GPT-4 模型对产品描述进行高质量翻译。
- **Markdown 文件生成**：生成包含产品数据、关键词和翻译描述的 Markdown 文件，方便在网站或其他平台上发布。
- **每日自动化**：通过 GitHub Actions 自动生成并提交每日的 Markdown 文件。
- **可配置工作流**：支持手动触发或通过 GitHub Actions 定时生成内容。
- **灵活定制**：脚本易于扩展或修改，可以包括额外的产品细节或调整文件格式。
- **自动发布到 WordPress**：生成的 Markdown 文件可以自动发布到 WordPress 网站。

## 快速开始

### 前置条件

- Python 3.x
- GitHub 账户及仓库
- OpenAI API Key
- Product Hunt Developer Token (从 Product Hunt 开发者设置页面获取)
- WordPress 网站及凭证（用于自动发布）

### 安装

1. **克隆仓库：**

```bash
git clone https://github.com/ViggoZ/producthunt-daily-hot.git
cd producthunt-daily-hot
```

2. **安装 Python 依赖：**

确保您的系统已安装 Python 3.x。然后安装所需的依赖包：

```bash
pip install -r requirements.txt
```

### 设置

1. **GitHub Secrets：**

   在您的 GitHub 仓库中添加以下 Secrets：

   - `OPENAI_API_KEY`: 您的 OpenAI API 密钥
   - `PRODUCTHUNT_DEVELOPER_TOKEN`: 您的 Product Hunt Developer Token
   - `PAT`: 用于推送更改到仓库的个人访问令牌
   - `WORDPRESS_URL`: 您的 WordPress 网站 URL
   - `WORDPRESS_USERNAME`: 您的 WordPress 用户名
   - `WORDPRESS_PASSWORD`: 您的 WordPress 密码

2. **获取 Product Hunt Developer Token：**

   1. 访问 [Product Hunt 开发者设置页面](https://www.producthunt.com/v2/oauth/applications)
   2. 登录您的账户
   3. 在开发者设置中创建一个新的应用
   4. 获取 Developer Token

3. **GitHub Actions 工作流：**

   工作流定义在 `.github/workflows/generate_markdown.yml` 和 `.github/workflows/publish_to_wordpress.yml` 中。该工作流每天 UTC 时间 07:01（北京时间 15:01）自动运行，也可以手动触发。

### 使用

设置完成后，GitHub Action 将自动生成并提交包含 Product Hunt 每日热门产品的 Markdown 文件，并自动发布到 WordPress 网站。文件存储在 `data/` 目录下。

### 自定义

- 您可以修改 `scripts/product_hunt_list_to_md.py` 文件来自定义生成文件的格式或添加额外内容。
- 如果需要，可以在 `.github/workflows/generate_markdown.yml` 中调整定时任务的运行时间。

### 示例输出

生成的文件存储在 `data/` 目录下。每个文件以 `PH-daily-YYYY-MM-DD.md` 的格式命名。

### 贡献

欢迎任何形式的贡献！如有任何改进或新功能的建议，请提交 issue 或 pull request。

### 许可证

本项目基于 MIT 许可证开源 - 有关详细信息，请参阅 [LICENSE](LICENSE) 文件。
