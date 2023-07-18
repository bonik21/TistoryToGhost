import App_config
import requests
import jwt
from datetime import datetime as date
import tempfile
from urllib.parse import urlparse, urlunparse
import os
import Tistory_Read_info


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


# 이미지에서 ?original 쿼리 제거 (param입력시 ?없이)
def remove_specific_query_param(url, param):
    parsed_url = urlparse(url)
    query_params = parsed_url.query
    if query_params.startswith(param):
        query_params = query_params[len(param):].lstrip('&')
    parsed_url = parsed_url._replace(query=query_params)
    return urlunparse(parsed_url)


# 이미지 업로드(로컬파일이나 url을 입력하면 업로드 후 새 url 반환)
def upload_image(img_file):    
    endpoint = f'{API_URL}/ghost/api/admin/images/upload/'
    headers = {'Authorization': 'Ghost {}'.format(token)}

    # URL 파싱
    parsed_url = urlparse(img_file)

    if parsed_url.scheme in ('http', 'https'):
        # 외부 파일인 경우, 파일 다운로드

        # ?original 쿼리 제거
        img_file = remove_specific_query_param(img_file, "original")
        
        # 파일명 추출(확장자가 없을 땐 .png 추가)
        ref = os.path.basename(parsed_url.path)        
        if not os.path.splitext(ref)[1]:        
            ref += '.png'
        try:
            response = requests.get(img_file)           
            if response.status_code == 200:
                # 임시 파일 생성
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                # temp_file = tempfile.NamedTemporaryFile(delete=False)
                with open(temp_file.name, 'wb') as f:
                    f.write(response.content)                
                temp_file.close()

                # 파일 업로드
                files = {
                    'file': (ref, open(temp_file.name, 'rb'), 'image/png'),
                    "ref": (None, ref)
                }
                response = requests.post(endpoint, headers=headers, files=files)
                if response.status_code == 201:
                    print('업로드 성공 :', response.json())
                    new_url = response.json()['images'][0]['url'] 
                    replaced_url = new_url.replace(API_URL,'')
                    return replaced_url
                else:
                    print('업로드 실패. 상태 코드:', response.status_code)
                    print('에러 메시지:', response.text)    
            else:
                print('파일 다운로드 실패. 상태 코드:', response.status_code)
                               
        except requests.exceptions.RequestException as e:
            print(f"요청 오류 발생: {e}")
               
    else:
        # 로컬 파일인 경우

        # 유효한 확장자를 가졌는지 확인 없으면 .jpg추가
        if not Tistory_Read_info.is_valid_image_extension(img_file):
            img_file = Tistory_Read_info.add_image_extension(img_file)
            print(f"{img_file}으로 변환됨")        

        # 파일명 재추출
        parsed_url = urlparse(str(img_file))
        ref = os.path.basename(parsed_url.path)

        files = {
            'file': (ref, open(img_file, 'rb'), 'image/png'),
            "ref": (None, ref)
        }
        response = requests.post(endpoint, headers=headers, files=files)

        # 업로드 응답 결과 확인
        if response.status_code == 201:        
            print('업로드 성공 :', response.json())
            new_url = response.json()['images'][0]['url']
            
            # 내부경로로 변경
            replaced_url = new_url.replace(API_URL,'')        
            return replaced_url
        else:
            print('업로드 실패. 상태 코드:', response.status_code)
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
        print(f'{slug} 글 작성 성공')
        print('-'*100)
        # print('Response:', response.json())                
    else:
        print(f'{slug} 글 작성 실패. 상태 코드:', response.status_code)
        print('에러 메시지:', response.text)
