# pip install pyjwt
import App_config
import requests
import jwt
from datetime import datetime as date

# Admin API key goes here
key = App_config.ADMIN_API
api_url = App_config.API_URL

# Split the key into ID and SECRET
id, secret = key.split(':')

# Prepare header and payload
iat = int(date.now().timestamp())

header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
payload = {
    'iat': iat,
    'exp': iat + 5 * 60,
    'aud': '/admin/'
}

# Create the token (including decoding secret)
token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)

# Make an authenticated request to create a post
endpoint = f'{api_url}/ghost/api/admin/posts/?source=html'
headers = {'Authorization': 'Ghost {}'.format(token)}
body = {
    "posts": [
        {
            "title": "My test post",
            "slug": "test123",
            "tags": ["Getting Started", "Tag Example"],
            "authors": ["mail@bonik.me"],
            "feature_image": "https://static.ghost.org/v3.0.0/images/welcome-to-ghost.png",
            "html": "<p>본문입니다. 본문. My post content. Work in progress...</p>",
            "status": "published"
        }
    ]
}
response = requests.post(endpoint, json=body, headers=headers)

# 응답 결과 확인
if response.status_code == 201:
    print('글 작성 성공')    
else:
    print('글 불러오기에 실패했습니다. 상태 코드:', response.status_code)
    print('에러 메시지:', response.text)
