import os
import markdown 
import requests
import argparse
from datetime import datetime, timezone
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

def republish_to_wordpress(file_path):
    """重新发布指定的 Markdown 文件到 WordPress"""
    wordpress_url = os.getenv('WORDPRESS_URL')
    wordpress_username = os.getenv('WORDPRESS_USERNAME')
    wordpress_password = os.getenv('WORDPRESS_PASSWORD')

    if not all([wordpress_url, wordpress_username, wordpress_password]):
        print("错误: 缺少 WordPress 凭据。请确保在 .env 文件中设置了 WORDPRESS_URL, WORDPRESS_USERNAME 和 WORDPRESS_PASSWORD。")
        return

    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误: 文件不存在: {file_path}")
        return

    # 读取 Markdown 文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return

    # 去掉第一行的大标题
    lines = content.splitlines()
    if lines and lines[0].startswith('#'):
        title = lines[0].strip('#').strip()
        lines = lines[1:]
    else:
        # 如果没有标题，使用文件名作为标题
        title = os.path.basename(file_path).replace('.md', '')
    
    content_without_title = '\n'.join(lines)

    # 将 Markdown 内容转换为 HTML
    html_content = markdown.markdown(content_without_title)

    # 获取文件名作为固定链接
    slug = os.path.basename(file_path).replace('.md', '')

    # 构建请求数据
    post_data = {
        'title': title,
        'content': html_content,
        'status': 'publish',  # 发布状态
        'slug': slug,  # 固定链接
        'categories': [337]  # 分类目录 ID
    }

    # 构建请求头
    headers = {
        'Content-Type': 'application/json'
    }

    # 构建请求 URL
    api_url = f'{wordpress_url}/wp-json/wp/v2/posts'

    # 发送 POST 请求
    try:
        response = requests.post(api_url, json=post_data, headers=headers, auth=(wordpress_username, wordpress_password), allow_redirects=False)
        
        # 检查响应状态
        if response.status_code == 201:
            print(f"文章发布成功: {title}")
            post_id = response.json().get('id')
            post_link = response.json().get('link')
            print(f"文章 ID: {post_id}")
            print(f"文章链接: {post_link}")
        else:
            print(f"发布文章失败: {response.status_code}")
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"发送请求时出错: {e}")

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='重新发布 Markdown 文件到 WordPress')
    parser.add_argument('file_path', help='要发布的 Markdown 文件路径')
    args = parser.parse_args()

    # 重新发布文件
    republish_to_wordpress(args.file_path)

if __name__ == "__main__":
    main() 