import App_config
import requests
import jwt
from datetime import datetime as date
import tempfile
from urllib.parse import urlparse
import os


# 필요한 정보 불러오기
ADMIN_API = App_config.ADMIN_API
API_URL = App_config.API_URL
AUTHOR = App_config.AUTHOR


# ADMIN_API를 ID와 SECRET으로 분리
id, secret = ADMIN_API.split(':')


# 인증을 위한 헤더 및 페이로드 작성
iat = int(date.now().timestamp())

header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
payload = {
    'iat': iat,
    'exp': iat + 5 * 60,
    'aud': '/admin/'
}

# 토큰 생성 (SECRET 디코딩 포함)
token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)


# 이미지 업로드
def upload_image(file=''):
    endpoint = f'{API_URL}/ghost/api/admin/images/upload/'
    headers = {'Authorization': 'Ghost {}'.format(token)}

    # URL 파싱
    parsed_url = urlparse(file)
    print('parsed_url :', parsed_url)

    # 파일명 추출
    ref = os.path.basename(parsed_url.path)    

    if parsed_url.scheme in ('http', 'https'):
        # 외부 파일인 경우, 파일 다운로드
        response = requests.get(file)
        if response.status_code != 200:
            print('파일 다운로드 실패. 상태 코드:', response.status_code)
            return

        # 임시 파일 생성
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        with open(temp_file.name, 'wb') as f:
            f.write(response.content)
        temp_file.close()

        # 파일 업로드
        files = {
            'file': (ref, open(temp_file.name, 'rb'), 'image/png'),
            "ref": (None, ref)
        }
        response = requests.post(endpoint, headers=headers, files=files)
    else:
        # 로컬 파일인 경우, 그대로 업로드
        files = {
            'file': (ref, open(file, 'rb'), 'image/png'),
            "ref": (None, ref)
        }
        response = requests.post(endpoint, headers=headers, files=files)

    # 응답 결과 확인
    if response.status_code == 201:
        print('이미지 업로드 성공')
        print('Response:', response.text)
    else:
        print('이미지 업로드 실패. 상태 코드:', response.status_code)
        print('에러 메시지:', response.text)


# 고스트에 글 작성
def write_to_ghost(title='', slug='', tags='', feature_image='', html='', status='published', published_at=''):
    endpoint = f'{API_URL}/ghost/api/admin/posts/?source=html'
    headers = {'Authorization': 'Ghost {}'.format(token)}
    body = {
        "posts": [
            {
                "title": title,
                "slug": slug,
                "tags": [f"{tags}"],
                "authors": [f"{AUTHOR}"],
                "feature_image": feature_image,
                "html": html,
                "status": status,
                "published_at": published_at
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


# # Make an authenticated request to create a post
# endpoint = f'{API_URL}/ghost/api/admin/posts/?source=html'
# headers = {'Authorization': 'Ghost {}'.format(token)}
# body = {
#     "posts": [
#         {
#             "title": "My test post2",
#             "slug": "test123",
#             "tags": ["Getting Started", "Tag Example"],
#             "authors": [f"{AUTHOR}"],
#             "feature_image": "https://static.ghost.org/v3.0.0/images/welcome-to-ghost.png",
#             "html": "<p>본문입니다. 본문. My post content. Work in progress...</p>",
#             "status": "published"
#         }
#     ]
# }
# response = requests.post(endpoint, json=body, headers=headers)

# # 응답 결과 확인
# if response.status_code == 201:
#     print('글 작성 성공')    
# else:
#     print('글 불러오기에 실패했습니다. 상태 코드:', response.status_code)
#     print('에러 메시지:', response.text)


# write_to_ghost(title='제목',slug='test4534',tags='News, 음악', feature_image=r'E:\\Code\\Python\\Ghost\\tistory-temp\\471\\img\\d0005363_4f3b353aecb9e.jpg', html='<p>본문</p>')
