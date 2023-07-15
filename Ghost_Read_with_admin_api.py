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
endpoint = f'{api_url}/ghost/api/admin/posts/'
headers = {'Authorization': 'Ghost {}'.format(token)}
body = {'posts': [{'title': 'Hello World'}]}

# 요청
response = requests.get(endpoint, headers=headers)

# 응답 결과 확인
if response.status_code == 200:
    print('요청성공')
    posts_data = response.json()
    posts = posts_data['posts']
    
    # 각 글의 제목과 내용 출력(admin api로 할 때는 html이 없음)
    # for post in posts:        
    #     post_title = post['title']
    #     post_content = post['html']
    #     print('제목:', post_title)
    #     print('내용:', post_content)
    #     print('---')
    # # 키값만 확인
    for post in posts:                
        keys = list(post.keys())
        for key in keys:
            print(key)        
else:
    print('글 불러오기에 실패했습니다. 상태 코드:', response.status_code)
    print('에러 메시지:', response.text)
