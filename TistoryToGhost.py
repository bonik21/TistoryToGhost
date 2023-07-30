import App_config
import Ghost_Read_with_content_api, Ghost_Read_with_admin_api, Ghost_Write_in_HTML
import Tistory_Read_info, Tistory_Edit_HTML, Tistory_Custom


API_URL = App_config.API_URL
TISTROY_BACKUP_PATH = App_config.TISTROY_BACKUP_PATH
IMAGE_METHOD = App_config.IMAGE_METHOD
# 티스토리백업 폴더의 slug_list
slug_list = Tistory_Read_info.get_slug_list(TISTROY_BACKUP_PATH)
# 
ghost_slug_list = Ghost_Read_with_content_api.read_all_ghost_slug()


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


# 작성중 : 티스토리에서 고스트로 옮기기 (단일 slug)
def tistory_to_ghost(slug):
    file_list = Tistory_Read_info.get_file_list(slug)
    print('file_list :', file_list)
    html_file_name = file_list["html_file"][0]
    html_file = f'{TISTROY_BACKUP_PATH}\{slug}\{html_file_name}'
    # HTML 편집(url변환, <p></p>, <script></script>, <style></style> 제거)        
    Tistory_Edit_HTML.prettier_html(html_file)

    # URL 치환
    Tistory_Custom.convert_url(html_file)

    # 유튜브, 사운드클라우드 코드 수정(embed, iframe 재작성)
    Tistory_Edit_HTML.rewrite_youtube_iframe(html_file)
    Tistory_Edit_HTML.rewrite_youtube_embed(html_file)
    Tistory_Edit_HTML.rewrite_soundcloud_embed(html_file)

    # 다음 밀어주기 제거
    Tistory_Edit_HTML.remove_daumgift(html_file)

    # iframe width, height 제거(미사용)
    # Tistory_Edit_HTML.remove_iframe_width_height(html_file)

    # 이미지 및 첨부파일 처리
    if IMAGE_METHOD == 'Upload':
        Tistory_Read_info.copy_att(slug)
        # img src 편집
        Tistory_Edit_HTML.convert_img_src_upload(html_file, slug)
        # 첨부파일 a href 편집
        Tistory_Edit_HTML.convert_file_src(html_file, slug)
    elif IMAGE_METHOD == 'Copy':
        Tistory_Read_info.copy_img_and_att(slug)
        # img src 편집
        Tistory_Edit_HTML.convert_img_src_copy(html_file, slug)
        # 첨부파일 a href 편집
        Tistory_Edit_HTML.convert_file_src(html_file, slug)
    else:
        print(Colors.RED,"오류 : 이미지 및 첨부파일 처리 실패", Colors.RESET)

    # 등록되어 있는지 확인
    if Ghost_Read_with_content_api.is_slug_in_Ghost(slug):
        print(Colors.GREEN, f"[{slug}]은(는) 이미 고스트에 포스팅되어 있습니다.", Colors.RESET)
        return
    
    upload_data = Tistory_Edit_HTML.extract_html_info(html_file)
    
    Ghost_Write_in_HTML.write_to_ghost(
        title=upload_data["title"],
        slug=slug,
        tags=upload_data["category"],
        feature_image=upload_data["feature_image"],
        html=upload_data["content"],
        status='published',
        published_at=upload_data["published_at"]
        )
    

# 작성중 : 티스토리에서 고스트로 옮기기 (티스토리 백업 폴더 전체)
def tistory_to_ghost_all():
    for slug in ghost_slug_list:
        tistory_to_ghost(slug)
    return


# # 현재 고스트에 등록된 게시물 수 확인
# all_ghost_content = Ghost_Read_with_content_api.read_all_ghost_content()
# print(f'{API_URL}에 등록된 게시물 : {len(all_ghost_content)}개')


# # 티스토리 백업 폴더에 있는 게시물 수 확인
# print(f'{TISTROY_BACKUP_PATH}에 게시물 {len(slug_list)}개')


# # 티스토리 백업 폴더에 있는 게시물 slug 확인
# print(f'티스토리 게시물 목록 " {slug_list}')


# # 티스토리 백업 폴더에 있는 파일 목록 확인
# for slug in slug_list:    
#     data_list = Tistory_Read_info.get_file_list(slug)
#     print(data_list)


# # 티스토리 백업 폴더에 있는 파일 고스트 /content로 복사
# for slug in slug_list:    
#     Tistory_Read_info.copy_img_and_att(slug)


# 단일 포스팅
# tistory_to_ghost('603')


# # 전체 포스팅
# tistory_to_ghost_all()


# 고스트에 포스팅된 게시물 중 meta decription 없는 것
# for slug in ghost_slug_list:    
#     meta_desc = Ghost_Read_with_admin_api.if_exist_meta_desc(slug)
#     if meta_desc is False:
#         print(f'{slug}: {meta_desc}')