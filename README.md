
# PH今日热榜 - PH Daily Hot List

[English Version](README_EN.md)

## 项目简介

PH今日热榜是一个基于Python的自动化工具，使用OpenAI的GPT-4模型对Product Hunt前一天的Top 30产品进行数据提取、关键词生成及描述翻译。该项目旨在帮助用户快速查看每日的Product Hunt热门榜单，并提供更详细的产品信息。

## 功能概述

- 自动获取前一天的Product Hunt Top 30产品数据
- 生成简洁易懂的中文关键词
- 使用OpenAI进行产品描述的高质量翻译
- 生成Markdown格式的每日榜单文件，方便在网站或其他平台上发布

## 使用方法

1. 克隆本项目到本地
2. 在项目根目录创建`.env`文件，添加以下内容：
```env
OPENAI_API_KEY=your_openai_api_key
PRODUCTHUNT_CLIENT_ID=your_producthunt_client_id
PRODUCTHUNT_CLIENT_SECRET=your_producthunt_client_secret
```
3. 运行`python scripts/product_hunt_list_to_md.py`生成每日榜单文件。

## 注意事项

- 本项目依赖于OpenAI API和Product Hunt API，需要配置相关的API密钥。
- 生成的Markdown文件会自动保存到`data`目录下，文件命名格式为`PH-daily-YYYY-MM-DD.md`。

## 贡献

欢迎提交Issue和Pull Request来改进本项目。
