import App_config
import Ghost_Read_with_content_api
import Tistory_Read_info


API_URL = App_config.API_URL
TISTROY_BACKUP_PATH = Tistory_Read_info.TISTROY_BACKUP_PATH
slug_list = Tistory_Read_info.get_slug_list(TISTROY_BACKUP_PATH)


# 현재 고스트에 등록된 게시물 수 확인
all_ghost_content = Ghost_Read_with_content_api.read_all_ghost_content()
print(f'{API_URL}에 등록된 게시물 : {len(all_ghost_content)}개')


# 티스토리 백업 폴더에 있는 게시물 수 확인
print(f'{TISTROY_BACKUP_PATH}에 게시물 {len(slug_list)}개')


# 티스토리 백업 폴더에 있는 게시물 slug 확인
print(f'티스토리 게시물 목록 " {slug_list}')


# # 티스토리 백업 폴더에 있는 파일 목록 확인
# for slug in slug_list:    
#     data_list = Tistory_Read_info.get_file_list(slug)
#     print(data_list)


# 티스토리 백업 폴더에 있는 파일 고스트 /content로 복사
# for slug in slug_list:    
#     Tistory_Read_info.copy_img_and_att(slug)
