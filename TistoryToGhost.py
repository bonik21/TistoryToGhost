import App_config
import Ghost_Read_with_content_api, Ghost_Write_in_HTML
import Tistory_Read_info, Tistory_Edit_HTML


API_URL = App_config.API_URL
TISTROY_BACKUP_PATH = App_config.TISTROY_BACKUP_PATH
IMAGE_METHOD = App_config.IMAGE_METHOD
slug_list = Tistory_Read_info.get_slug_list(TISTROY_BACKUP_PATH)


# 작성중 : 티스토리에서 고스트로 옮기기 (단일 slug)
def tistory_to_ghost(slug):
    file_list = Tistory_Read_info.get_file_list(slug)
    print('file_list :', file_list)
    html_file_name = file_list["html_file"][0]
    html_file = f'{TISTROY_BACKUP_PATH}\{slug}\{html_file_name}'
    # HTML 편집(url변환, <p></p>, <script></script>, <style></style> 제거)
    print(html_file)
    Tistory_Edit_HTML.convert_url(html_file)
    Tistory_Edit_HTML.prettier_html(html_file)

    # iframe height 60%로 수정
    Tistory_Edit_HTML.convert_iframe_height(html_file, '60%')

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
        print("이미지 및 첨부파일 처리 실패")

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
    for slug in slug_list:
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
