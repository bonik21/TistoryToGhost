import App_config
import os
from bs4 import BeautifulSoup
import Ghost_Write_in_HTML
from datetime import datetime, timedelta
from urllib.parse import urlparse
import Tistory_Category_to_Slug


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


# HTML : <p></p> 제거
def remove_empty_paragraph_tags(soup):
    for paragraph in soup.find_all("p"):
        if not paragraph.contents:
            paragraph.extract()


# HTML : script, style제거(본문 첨부 애드센스 등)
def remove_script_tags(soup):
    for script in soup.find_all("script"):
        script.extract()
    for style in soup.find_all("style"):
        style.extract()    


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
    category = Tistory_Category_to_Slug.convert_category_to_slug(category_raw)    
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


# HTML파일 : iframe height 편집, ghost에서 height의 px이 %로 인식됨
def convert_iframe_height(html_file, height):
    height = str(height)
    with open(html_file, 'r+', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    for iframe_tag in soup.find_all("iframe"):
        if iframe_tag:
            original_height = iframe_tag.get('height')            
            iframe_tag["height"] = height
    indented_html = str(soup)            
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(indented_html)             
