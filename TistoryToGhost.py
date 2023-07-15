import App_config
import Ghost_Read_with_content_api


## 현재 고스트 게시물 수 확인
all_ghost_content = Ghost_Read_with_content_api.read_all_ghost_content()
print('고스트에 등록된 게시물 :',len(all_ghost_content) ,'개')


