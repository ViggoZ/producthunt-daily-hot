import os
import requests
from datetime import datetime

# 从环境变量中获取API密钥
openai_api_key = os.getenv('OPENAI_API_KEY')
producthunt_client_id = os.getenv('PRODUCTHUNT_CLIENT_ID')
producthunt_client_secret = os.getenv('PRODUCTHUNT_CLIENT_SECRET')

# 你的其他代码在这里...