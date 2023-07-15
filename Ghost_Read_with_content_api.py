import App_config
import requests
import jwt
from datetime import datetime as date

# Admin API key goes here
key = App_config.CONTENT_API
api_url = App_config.API_URL


# Make an authenticated request to create a post
endpoint = f'{api_url}/ghost/api/content/posts/'
headers = {'Accept-Version': 'v5.0'}
params = {'key': key}

# 요청
response = requests.get(endpoint, headers=headers, params=params)

# 응답 결과 확인
if response.status_code == 200:    
    posts_data = response.json()
    posts = posts_data['posts']

    for post in posts:                
        post_title = post['title']
        post_content = post['html']
        print('제목:', post_title)
        print('내용:', post_content)
        print('---')

    # # 키값만 확인
    # for post in posts:                
    #     keys = list(post.keys())
    #     for key in keys:
    #         print(key)

else:
    print('글 불러오기에 실패했습니다. 상태 코드:', response.status_code)
    print('에러 메시지:', response.text)
