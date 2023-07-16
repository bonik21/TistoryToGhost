import App_config
import os
from bs4 import BeautifulSoup
import Ghost_Write_in_HTML
from datetime import datetime, timezone


# 필요한 정보 불러오기
GHOST_IMG_URL = App_config.GHOST_IMG_URL
GHOST_ATT_URL = App_config.GHOST_ATT_URL


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
def extract_html_info(soup):   
    
    # 타이틀 <title></title> 내용 가져오기
    title_element = soup.find("title")
    title = title_element.text if title_element else ""
    title = title.strip()
    
    # 카테고리 <p class="category"></p> 내용 가져오기
    category_element = soup.find("p", class_="category")
    category = category_element.text if category_element else ""
    category = category.strip()

    # 태그 <div class="tags"></div> 내용 가져오기
    tags_element = soup.find("div", class_="tags")
    tags = tags_element.text if tags_element else ""
    tags = tags.strip()

    # 본문 <div class="article-view"></div> 가져오기
    content_element = soup.find("div", class_="article-view")
    content = str(content_element) if content_element else ""

    # # 대표 이미지(최초의 figure태그 인식)
    # figure_tag = soup.find('figure', class_='imageblock alignCenter')
    # if figure_tag:
    #     img_tag = figure_tag.find('img')
    #     if img_tag:
    #         src = img_tag.get('src')
    #         feature_image=src            
    #     else:            
    #         print("Image tag not found.")
    #         feature_image=''
    # else:
    #     print("Figure tag not found.")
    #     feature_image=''
    
    # return {
    #     "title": title,
    #     "category": category,        
    #     "tags": tags,
    #     "content": content,
    #     "feature_image": feature_image
    # }

    # 대표 이미지 (최초 img 태그 인식)
    img_tag = soup.find('img')
    if img_tag:
        src = img_tag.get('src')
        feature_image=src            
    else:            
        print("Image tag not found.")
        feature_image=''
    
    return {
        "title": title,
        "category": category,        
        "tags": tags,
        "content": content,
        "feature_image": feature_image
    }


# HTML파일 : 보기좋게 재정렬
def prettier_html(html_file):
    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    remove_empty_paragraph_tags(soup)
    remove_script_tags(soup)        
    indented_html = soup.prettify()
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(indented_html)


# HTML파일 : img src 주소 변환
def convert_img_src(html_file, slug):
    with open(html_file, 'r+', encoding='utf-8') as file:
        html_content = file.read()
        html_content = html_content.replace('./img/', f'{GHOST_IMG_URL}/{slug}/')
        file.seek(0)
        file.write(html_content)
        file.truncate()


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
    
    # 입력한 시간에 한국 표준시(UTC+9)를 적용하여 datetime 객체 생성
    kst_timezone = timezone(datetime.timedelta(hours=9))
    kst_datetime = input_datetime.replace(tzinfo=kst_timezone)
    
    # UTC로 변환
    utc_datetime = kst_datetime.astimezone(timezone.utc)
    
    # 출력 형식에 맞게 변환
    output_time = utc_datetime.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    
    return output_time


def tistory_to_ghost(directory):
    html_files = list_html_files(directory)
    for file_path in html_files:
        slug = extract_numbers_from_file_path(file_path)
        prettier_html(file_path)
        convert_img_src(file_path, slug)
        convert_file_src(file_path, slug)
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, "html.parser")        
        title = extract_html_info(soup)["title"]
        category = extract_html_info(soup)["category"]
        tags = extract_html_info(soup)["tags"]
        content = extract_html_info(soup)["content"]
        feature_image = extract_html_info(soup)["feature_image"]        
        Ghost_Write_in_HTML.write_to_ghost(title=title, slug=slug, tags=category, feature_image=feature_image, html=content, status='published')


# 사용 예시
directory_path = "E:\\Code\\Python\\Ghost\\tistory-temp"
tistory_to_ghost(directory_path)

