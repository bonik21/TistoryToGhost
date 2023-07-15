import App_config
import requests
import jwt
from datetime import datetime as date


# 필요한 key 불러오기
CONTENT_API = App_config.CONTENT_API
API_URL = App_config.API_URL


# Request 정보
endpoint = f'{API_URL}/ghost/api/content/posts/'
headers = {'Accept-Version': 'v5.0'}
params = {'key': CONTENT_API}


# 모든 게시물 출력 : 모든 정보 출력
def read_all_ghost_content():
    response = requests.get(endpoint, headers=headers, params=params)
    all_ghost_content = []
    
    # 응답 결과 확인
    if response.status_code == 200:    
        posts_data = response.json()
        all_ghost_content = posts_data['posts']
        return all_ghost_content

    else:
        print('글 불러오기에 실패했습니다. 상태 코드:', response.status_code)
        print('에러 메시지:', response.text)


# 모든 게시물 출력 : 슬러그, 제목, 내용(html)만 출력
def read_all_ghost_content_simple():
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
        print('글 불러오기에 실패했습니다. 상태 코드:', response.status_code)
        print('에러 메시지:', response.text)


# 사용가능한 key리스트 출력
def read_key_list_ghost_content():
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
        print('key 불러오기에 실패했습니다. 상태 코드:', response.status_code)
        print('에러 메시지:', response.text)


# 아래는 사용 예

# # 모든 고스트 콘텐츠 확인
# all_ghost_content = Ghost_Read_with_content_api.read_all_ghost_content()
# print(all_ghost_content)


# # 모든 고스트 콘텐츠 확인(인덱스) x번째 게시물
# all_ghost_content = Ghost_Read_with_content_api.read_all_ghost_content()
# print(all_ghost_content[0])


# # 모든 고스트 콘텐츠 확인(슬러그, 제목, 내용만 표시)
# all_ghost_content_simple = Ghost_Read_with_content_api.read_all_ghost_content_simple()
# print(all_ghost_content_simple)


# # 고스트 게시물 수 확인
# all_ghost_content = Ghost_Read_with_content_api.read_all_ghost_content()
# print('고스트에 등록된 게시물 :',len(all_ghost_content) ,'개')
