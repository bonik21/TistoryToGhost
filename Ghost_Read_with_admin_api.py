import App_config
import requests
import jwt
from datetime import datetime as date


class Colors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


# 필요한 key 불러오기
ADMIN_API = App_config.ADMIN_API
API_URL = App_config.API_URL


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


# 특정 게시물 출력 : 모든 정보 출력
def read_slug_ghost_content(slug):
    # Request 정보
    endpoint = f'{API_URL}/ghost/api/admin/posts/slug/{slug}'
    headers = {'Authorization': f'Ghost {token}'}
    response = requests.get(endpoint, headers=headers)
    all_ghost_content = []
    
    # 응답 결과 확인
    if response.status_code == 200:    
        posts_data = response.json()
        all_ghost_content = posts_data['posts']
        return all_ghost_content

    else:
        print('글 불러오기에 실패했습니다. 상태 코드:', response.status_code)
        print('에러 메시지:', response.text)


# 특정 게시물 업로드 확인 (업로드 되어 있으면 True)
def is_slug_in_Ghost(slug):
    # Request 정보
    endpoint = f'{API_URL}/ghost/api/admin/posts/slug/{slug}'
    headers = {'Authorization': f'Ghost {token}'}
    response = requests.get(endpoint, headers=headers)
    all_ghost_content = []
    
    # 응답 결과 확인
    if response.status_code == 200:            
        return True

    else:
        print('글 불러오기에 실패했습니다. 상태 코드:', response.status_code)
        # print('에러 메시지:', response.text)
        return False        


# 고스트의 모든 게시물 출력 : 모든 정보 출력
def read_all_ghost_content():
    # Request 정보
    endpoint = f'{API_URL}/ghost/api/admin/posts/?limit=all'
    headers = {'Authorization': f'Ghost {token}'}
    response = requests.get(endpoint, headers=headers)
    all_ghost_content = []
    
    # 응답 결과 확인
    if response.status_code == 200:    
        posts_data = response.json()
        all_ghost_content = posts_data['posts']
        return all_ghost_content

    else:
        print('글 불러오기에 실패했습니다. 상태 코드:', response.status_code)
        print('에러 메시지:', response.text)


# 고스트의 게시물 수 출력
def number_of_ghost_content():
    # Request 정보
    endpoint = f'{API_URL}/ghost/api/admin/posts/?limit=all'
    headers = {'Authorization': f'Ghost {token}'}
    response = requests.get(endpoint, headers=headers)
    all_ghost_content = []
    
    # 응답 결과 확인
    if response.status_code == 200:    
        posts_data = response.json()
        all_ghost_content = posts_data['posts']
        return len(all_ghost_content)

    else:
        print('글 불러오기에 실패했습니다. 상태 코드:', response.status_code)
        print('에러 메시지:', response.text)        


# # (html key 사용불가)모든 게시물 출력 : 슬러그, 제목, 내용(html)만 출력
# # admin_api로 조회할 때는 html키 값이 없음.
# def read_all_ghost_content_simple():
#     response = requests.get(endpoint, headers=headers)
#     all_ghost_content = []

#     # 응답 결과 확인
#     if response.status_code == 200:    
#         posts_data = response.json()
#         posts = posts_data['posts']

#         for post in posts:                
#             post_slug = post['slug']            
#             post_title = post['title']
#             post_content = post['html']            
#             this_post = {"slug": post_slug, "title": post_title, 'html': post_content}
#             all_ghost_content.append(this_post)         

#         return all_ghost_content    

#     else:
#         print('글 불러오기에 실패했습니다. 상태 코드:', response.status_code)
#         print('에러 메시지:', response.text)


# 사용가능한 key리스트 출력
def read_key_list_ghost_content():
    # Request 정보
    endpoint = f'{API_URL}/ghost/api/admin/posts/'
    headers = {'Authorization': f'Ghost {token}'}   
    response = requests.get(endpoint, headers=headers)

    key_list = []
    # 응답 결과 확인
    if response.status_code == 200:    
        posts_data = response.json()
        posts = posts_data['posts']        

        # 키값만 확인
        for post in posts:                
            keys = list(post.keys())
            for key in keys:
                # print(key)                
                key_list.append(key)                
        return key_list            

    else:
        print('key 불러오기에 실패했습니다. 상태 코드:', response.status_code)
        print('에러 메시지:', response.text)


# slug에 해당하는 meta description이 있는지 확인
def if_exist_meta_desc(slug):    
    try:
        meta_description = read_slug_ghost_content(slug)[0]["meta_description"]                
        if type(meta_description) is str:
                # print(f'{slug} :', meta_description[:20], '...')
                return True
        elif meta_description is None:
            return False
        else:
            return False
    except TypeError as e:
        print(e)
        return False


# 아래는 사용 예

# # 모든 고스트 콘텐츠 확인
# all_ghost_content = read_all_ghost_content()
# print(all_ghost_content)


# # 모든 고스트 콘텐츠 확인(인덱스) x번째 게시물
# all_ghost_content = read_all_ghost_content()
# print(all_ghost_content[0])


# # 고스트 게시물 수 확인
# all_ghost_content = read_all_ghost_content()
# print('고스트에 등록된 게시물 :',len(all_ghost_content) ,'개')


# # 특정 고스트 콘텐츠 확인(slug)
# slug_ghost_content = read_slug_ghost_content('123')
# print(slug_ghost_content)


# # 콘텐츠가 고스트에 올라갔는지 확인(slug)
# slug_ghost_content = is_slug_in_Ghost('123')
# print(slug_ghost_content)


# 특정 고스트 콘텐츠의 meta_description 확인(slug)
# slug_ghost_content = read_slug_ghost_content('975')
# print(slug_ghost_content[0]["meta_description"])


# meta description이 있는지 확인
# print(if_exist_meta_desc('927'))
