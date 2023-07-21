import App_config
import requests
import jwt
from datetime import datetime as date


# 필요한 key 불러오기
CONTENT_API = App_config.CONTENT_API
API_URL = App_config.API_URL


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


# 특정 게시물 업로드 확인 (업로드 되어 있으면 True)
def is_slug_in_Ghost(slug):
    # Request 정보
    endpoint = f'{API_URL}/ghost/api/content/posts/slug/{slug}'
    headers = {'Accept-Version': 'v5.0'}
    params = {'key': CONTENT_API}

    response = requests.get(endpoint, headers=headers, params=params)    
    
    # 응답 결과 확인
    if response.status_code == 200:            
        return True

    else:
        # print(Colors.RED, '오류 : 글 불러오기 실패. 상태 코드:', response.status_code, Colors.RESET)
        # print('에러 메시지:', response.text)
        return False  


# 모든 게시물 출력 : 모든 정보 출력
def read_all_ghost_content():
    endpoint = f'{API_URL}/ghost/api/content/posts/?limit=all'
    headers = {'Accept-Version': 'v5.0'}
    params = {'key': CONTENT_API}

    response = requests.get(endpoint, headers=headers, params=params)
    all_ghost_content = []
    
    # 응답 결과 확인
    if response.status_code == 200:    
        posts_data = response.json()
        all_ghost_content = posts_data['posts']
        return all_ghost_content

    else:
        print(Colors.RED, '오류 : 글 불러오기 실패. 상태 코드:', response.status_code, Colors.RESET)
        print(Colors.RED,'에러 메시지:', response.text, Colors.RESET)


# 모든 게시물 출력 : 슬러그, 제목, 내용(html)만 출력
def read_all_ghost_content_simple():
    endpoint = f'{API_URL}/ghost/api/content/posts/?limit=all'
    headers = {'Accept-Version': 'v5.0'}
    params = {'key': CONTENT_API}

    response = requests.get(endpoint, headers=headers, params=params)
    all_ghost_content = []

    # 응답 결과 확인
    if response.status_code == 200:    
        posts_data = response.json()
        posts = posts_data['posts']

        for post in posts:                
            post_slug = post['slug']            
            post_title = post['title']
            post_content = post['html']            
            this_post = {"slug": post_slug, "title": post_title, 'html': post_content}
            all_ghost_content.append(this_post)         

        return all_ghost_content    

    else:
        print(Colors.RED, '오류 : 글 불러오기 실패. 상태 코드:', response.status_code, Colors.RESET)
        print(Colors.RED,'에러 메시지:', response.text, Colors.RESET)


# 사용가능한 key리스트 출력

def read_key_list_ghost_content():
    endpoint = f'{API_URL}/ghost/api/content/posts/'
    headers = {'Accept-Version': 'v5.0'}
    params = {'key': CONTENT_API}

    response = requests.get(endpoint, headers=headers, params=params)

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
        print(Colors.RED, '오류 : key 불러오기 실패. 상태 코드:', response.status_code, Colors.RESET)
        print(Colors.RED,'에러 메시지:', response.text, Colors.RESET)


# 아래는 사용 예

# # 모든 고스트 콘텐츠 확인
# all_ghost_content = read_all_ghost_content()
# print(all_ghost_content)


# # 모든 고스트 콘텐츠 확인(인덱스) x번째 게시물
# all_ghost_content = read_all_ghost_content()
# print(all_ghost_content[0])


# # 모든 고스트 콘텐츠 확인(슬러그, 제목, 내용만 표시)
# all_ghost_content_simple = read_all_ghost_content_simple()
# print(all_ghost_content_simple)


# # 고스트 게시물 수 확인
# all_ghost_content = read_all_ghost_content()
# print('고스트에 등록된 게시물 :',len(all_ghost_content) ,'개')

# # 콘텐츠가 고스트에 올라갔는지 확인(slug)
# slug_ghost_content = is_slug_in_Ghost('123')
# print(slug_ghost_content)
