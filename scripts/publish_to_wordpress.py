import os
import markdown 
import requests
from datetime import datetime, timezone

# 加载 .env 文件
# load_dotenv()

def publish_to_wordpress():
    wordpress_url = os.getenv('WORDPRESS_URL')
    wordpress_username = os.getenv('WORDPRESS_USERNAME')
    wordpress_password = os.getenv('WORDPRESS_PASSWORD')

    # 获取今天的日期并格式化
    today = datetime.now(timezone.utc)
    date_today = today.strftime('%Y-%m-%d')

    # 获取最新的Markdown文件内容
    file_name = f'data/producthunt-daily-{date_today}.md'
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File not found: {file_name}")
        return

    # 去掉第一行的大标题
    lines = content.splitlines()
    if lines and lines[0].startswith('#'):
        lines = lines[1:]
    content_without_title = '\n'.join(lines)

    # 将Markdown内容转换为HTML
    html_content = markdown.markdown(content_without_title)

    # 获取文件中的第一行作为标题
    title = content.splitlines()[0].strip('#').strip()

    # 获取文件名作为固定链接
    slug = os.path.basename(file_name).replace('.md', '')

    # 构建请求数据
    post_data = {
        'title': title,
        'content': html_content,
        'status': 'publish',  # 将发布状态 草稿draft
        'slug': slug,  # 添加固定链接
        'categories': [337]  # 添加分类目录
    }

    # 构建请求头
    headers = {
        'Content-Type': 'application/json'
    }

    # 构建请求URL
    api_url = f'{wordpress_url}/wp-json/wp/v2/posts'

    # 发送POST请求，禁用重定向
    response = requests.post(api_url, json=post_data, headers=headers, auth=(wordpress_username, wordpress_password), allow_redirects=False)

    # 检查响应状态
    if response.status_code == 201:
        print("Post published successfully.")
    else:
        print(f"Failed to publish post: {response.status_code}, {response.text}")

if __name__ == "__main__":
    publish_to_wordpress()
