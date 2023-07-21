import App_config
import os
from bs4 import BeautifulSoup
import Ghost_Write_in_HTML
from datetime import datetime, timedelta
from urllib.parse import urlparse, unquote
import Tistory_Custom
import re


# 필요한 정보 불러오기
GHOST_IMG_URL = App_config.GHOST_IMG_URL
GHOST_ATT_URL = App_config.GHOST_ATT_URL
IMAGE_METHOD = App_config.IMAGE_METHOD
TISTORY_BACKUP_PATH = App_config.TISTROY_BACKUP_PATH


# 디렉토리에서 HTML파일 검색
def list_html_files(directory):
    html_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files


# URL가져오기 (Ghost Slug로 사용)
def extract_numbers_from_file_path(file_path):
    file_name = os.path.basename(file_path)
    number = ''.join(filter(str.isdigit, file_name))
    return number


# HTML : <p></p> 제거 [Pass by Object Reference(Call by Sharing)]
def remove_empty_paragraph_tags(soup):
    for paragraph in soup.find_all("p"):
        if not paragraph.contents:
            paragraph.extract()


# HTML : script, style제거(본문 첨부 애드센스 등) [Pass by Object Reference(Call by Sharing)]
def remove_script_tags(soup):
    for script in soup.find_all("script"):
        script.extract()
    for style in soup.find_all("style"):
        style.extract()


# HTML : 태그 <div class="tags"></div>의 공백 제거 (Call by Sharing 아님)
def remove_tags_space(soup):
    tags_element = soup.find("div", class_="tags")
    if tags_element:
        tags = tags_element.text.strip()
        tags_element.string = tags  # 해당 태그의 내용을 수정
    return soup  # 수정된 soup 객체를 반환   


# HTML : 태그 <div class="tags"></div> 제거 (Call by Sharing 아님)
def remove_tags(soup):
    tags_element = soup.find("div", class_="tags")
    if tags_element:
        tags_element.extract()
    return soup    


# HTML 내용 가져오기(title, category, tags, content, feature_image)
def extract_html_info(html_file):
    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")       
    
    # 타이틀 <title></title> 내용 가져오기
    title_element = soup.find("title")
    title = title_element.text if title_element else ""
    title = title.strip()
    
    # 카테고리 <p class="category"></p> 내용 가져오기
    category_element = soup.find("p", class_="category")
    category_raw = category_element.text if category_element else ""
    category_raw = category_raw.strip()
    category = Tistory_Custom.convert_category_to_slug(category_raw)    
    print(f"티스토리 카테고리 [{category_raw}]을(를) 고스트 tag [{category}](으)로 변경합니다.")    

    # 태그 <div class="tags"></div> 내용 가져오기
    tags_element = soup.find("div", class_="tags")
    tags = tags_element.text if tags_element else ""
    tags = tags.strip()

    # 본문 <div class="article-view"></div> 가져오기
    content_element = soup.find("div", class_="article-view")
    content = str(content_element) if content_element else ""

    # 대표 이미지 (최초 img 태그 인식)
    img_tag = soup.find('img')
    if img_tag:
        src = img_tag.get('src')
        feature_image=src            
    else:            
        print("Image tag not found.")
        feature_image=''

    # 발행시간 <p class="date"></p> 내용 가져오기
    date_element = soup.find("p", class_="date")
    date = date_element.text if date_element else ""
    date = date.strip()    
    published_at = convert_to_utc(date)
    
    return {
        "title": title,
        "category": category,        
        "tags": tags,
        "content": content,
        "feature_image": feature_image,
        "published_at": published_at
    }


# HTML파일 : 편집(<p></p>, <script></script>, <style></style> 제거)
def prettier_html(html_file):
    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    remove_empty_paragraph_tags(soup)
    remove_script_tags(soup)
    soup = remove_tags_space(soup)    
    indented_html = str(soup)    
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(indented_html)


# HTML파일 : img src 주소 변환(복사방식)
def convert_img_src_copy(html_file, slug):
    with open(html_file, 'r+', encoding='utf-8') as file:
        html_content = file.read()
        html_content = html_content.replace('./img/', f'{GHOST_IMG_URL}/{slug}/')
        file.seek(0)
        file.write(html_content)
        file.truncate()


# HTML파일 : a href 원하는 주소 변환(커스텀)
def convert_url(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()    
    html_content = html_content.replace('http://fevernigga.tistory.com', 'https://bonik.me')
    html_content = html_content.replace('https://fevernigga.tistory.com', 'https://bonik.me')
    html_content = html_content.replace('http://', 'https://')
    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(html_content)


# HTML파일 : img src 주소 변환, 이미지 업로드 실행(업로드 방식)
def convert_img_src_upload(html_file, slug):
    with open(html_file, 'r+', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    for img_tag in soup.find_all("img"):
        if img_tag:
            original_src = img_tag.get('src')

            # 파일 이름 찾기
            parsed_url = urlparse(original_src)
            file_name = os.path.basename(parsed_url.path)            

            # 이미 처리 되었을 때
            if '/content/images/' in original_src: 
                print('html 편집 이미 처리됨') 

            # 내부 파일일 때
            elif './img/' in original_src:                 
                tistory_file_path = f'{TISTORY_BACKUP_PATH}\{slug}\img\{file_name}'
                # 업로드 실행 후 새 url(new_src) 받기
                new_src = Ghost_Write_in_HTML.upload_image(tistory_file_path)                
                # HTML 수정
                print(f'HTML 파일내의 "{original_src}"를 "{new_src}"로 교체 합니다.')
                img_tag["src"] = new_src                 

            # 외부 파일일 때
            elif parsed_url.scheme in ('http', 'https'):                                
                # 업로드 실행 후 새 url(new_src) 받기
                new_src = Ghost_Write_in_HTML.upload_image(original_src)                
                # HTML 수정
                print(f'HTML 파일내의 "{original_src}"를 "{new_src}"로 교체 합니다.')
                img_tag["src"] = new_src                                  
                    
    indented_html = str(soup)
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(indented_html)    
    return       


# HTML파일 : file href 주소 변환
def convert_file_src(html_file, slug):
    with open(html_file, 'r+', encoding='utf-8') as file:
        html_content = file.read()
        html_content = html_content.replace('./file/', f'{GHOST_ATT_URL}/{slug}/')
        file.seek(0)
        file.write(html_content)
        file.truncate()        


# 발행 시간 변환(KST to UTC)
def convert_to_utc(input_time):
    # 입력한 시간을 datetime 객체로 변환
    input_datetime = datetime.strptime(input_time, '%Y-%m-%d %H:%M:%S')

    # 입력한 시간에 UTC+9 시간을 더해줌
    kst_datetime = input_datetime + timedelta(hours=9)

    # UTC로 변환
    utc_datetime = kst_datetime - timedelta(hours=9)

    # 출력 형식에 맞게 변환
    output_time = utc_datetime.strftime('%Y-%m-%dT%H:%M:%S.000+00:00')

    return output_time


# HTML파일 : iframe width, height 제거(미사용)
def remove_iframe_width_height(html_file):    
    with open(html_file, 'r+', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    for iframe_tag in soup.find_all("iframe"):
        if iframe_tag:
            iframe_tag.attrs.pop('height', None)
            iframe_tag.attrs.pop('width', None)
    indented_html = str(soup)            
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(indented_html)             


# HTML파일 : 유튜브 iframe 태그에서 Youtube id추출 후 iframe 새로 작성
def rewrite_youtube_iframe(html_file):    
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    new_html_content = html_content

    for iframe_tag in re.finditer(r'<iframe.*?>.*?</iframe>', html_content):
        src_url = re.search(r'src="(.*?)"', iframe_tag.group(0))
        if src_url:
            video_id_match = re.search(r'youtube\.com/embed/([a-zA-Z0-9_-]+)', src_url.group(1))
            if video_id_match:
                video_id = video_id_match.group(1)
                # 기존 iframe_tag 텍스트를 새로운 태그로 대체
                new_iframe_tag = f'<iframe src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'
                new_html_content = new_html_content.replace(iframe_tag.group(0), new_iframe_tag)

    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(new_html_content)


# Code : Youtube object to iframe 형식으로 변환
def convert_youtube_embed(old_embed_code):
    # 유튜브 비디오 ID를 추출합니다.
    video_id_match = re.search(r'youtube\.com/v/([a-zA-Z0-9_-]+)', old_embed_code)
    if not video_id_match:
        # 유튜브 비디오 ID를 찾지 못한 경우 원래의 embed 코드를 그대로 반환합니다.
        return old_embed_code

    video_id = video_id_match.group(1)
    new_embed_code = f'<iframe src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>'
    return new_embed_code 


# HTML파일 : 오래된 Youtube object 태그에서 id추출 후 iframe 새로 작성
def rewrite_youtube_embed(html_file):    
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    new_html_content = html_content

    for object_tag in re.finditer(r'<object.*?>.*?</object>', html_content):        
        if object_tag:
            object_str = object_tag.group(0)
            new_object_tag = convert_youtube_embed(object_str)            
            new_html_content = new_html_content.replace(object_str, new_object_tag)

    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(new_html_content)


# HTML파일 : 오래된 Soundcloud object 태그에서 id추출 후 iframe 새로 작성
def rewrite_soundcloud_embed(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    new_html_content = html_content

    for object_tag in re.finditer(r'<object.*?>.*?</object>', html_content):        
        if object_tag:
            object_str = object_tag.group(0)
            new_object_tag = convert_soundcloud_embed(object_str)            
            new_html_content = new_html_content.replace(object_str, new_object_tag)

    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(new_html_content)


# Code : Soundcloud object to iframe 형식으로 변환
def convert_soundcloud_embed(old_embed_code):
    # src 값 추출
    src_match = re.search(r'src="(.*?)"', old_embed_code)
    if not src_match:
        print("사운드클라우드 embed 코드에서 src 값을 찾지 못함")
        return old_embed_code
    src = src_match.group(1)    
    decoded_src = unquote(src)

    # SoundCloud 트랙 ID 추출
    track_id_match = re.search(r'tracks/(\d+)', decoded_src)
    if not track_id_match:
        print("사운드클라우드 track id를 찾지 못함")
        return old_embed_code

    track_id = track_id_match.group(1)

    # 새로운 embed 코드 생성
    new_embed_code = f'<iframe width="100%" scrolling="no" frameborder="no" allow="autoplay" ' \
                     f'src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/{track_id}' \
                     f'&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&' \
                     f'show_reposts=false&show_teaser=true&visual=true"></iframe>'
    return new_embed_code


# HTML파일 : 다음 밀어주기 제거
def remove_daumgift(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    new_html_content = html_content

    for iframe_tag in re.finditer(r'<iframe.*?>.*?</iframe>', html_content):        
        if iframe_tag:
            iframe_str = iframe_tag.group(0)
            new_iframe_tag = remove_daumgift_iframe(iframe_str)            
            new_html_content = new_html_content.replace(iframe_str, new_iframe_tag)

    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(new_html_content)


# Code : iframe이 다음 밀어주기인 경우 빈값 리턴
def remove_daumgift_iframe(old_iframe_code):
    # src 값 추출
    src_match = re.search(r'src="(.*?)"', old_iframe_code)
    if not src_match:
        print("iframe코드에서 src 값을 찾지 못함")
        return old_iframe_code
    src = src_match.group(1)    
    decoded_src = unquote(src)

    # SoundCloud 트랙 ID 추출
    track_id_match = re.search(r'gift.blog.daum.net', decoded_src)
    if not track_id_match:        
        return old_iframe_code

    # 새로운 iframe 코드 생성
    new_iframe_code = ''
    return new_iframe_code

# temp_html = rf"{TISTORY_BACKUP_PATH}\87\87-가요---90's-댄스-(보컬X).html"
# remove_daumgift(temp_html)

# # 실행
# temp_object_str1 = '''
# <object width=0 height="81" width="100%"> <param width=0 name="movie" value="http://player.soundcloud.com/player.swf?url=http%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F5386404%3Fsecret_token%3Ds-UtvX6&amp;secret_url=false"></param> <param width=0 name="allowscriptaccess" value="always"></param> <embed width=0 allowscriptaccess="always" height="81" src="http://player.soundcloud.com/player.swf?url=http%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F5386404%3Fsecret_token%3Ds-UtvX6&amp;secret_url=false" type="application/x-shockwave-flash" width="100%"></embed> </object>
# '''

# temp_object_str2 = '''
# <object width=0 height="81" width="100%"> <param width=0 name="movie" value="http://player.soundcloud.com/player.swf?url=http%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F4942788%3Fsecret_token%3Ds-yXd0a&amp;secret_url=false"></param> <param width=0 name="allowscriptaccess" value="always"></param> <embed width=0 allowscriptaccess="always" height="81" src="http://player.soundcloud.com/player.swf?url=http%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F4942788%3Fsecret_token%3Ds-yXd0a&amp;secret_url=false" type="application/x-shockwave-flash" width="100%"></embed> </object>
# '''

# result_embed_code = convert_soundcloud_embed(temp_object_str1)
# print(result_embed_code)

