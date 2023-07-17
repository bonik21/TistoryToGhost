import App_config
import os
from pathlib import Path
import shutil


TISTROY_BACKUP_PATH = App_config.TISTROY_BACKUP_PATH
GHOST_IMG_PATH = App_config.GHOST_IMG_PATH
GHOST_ATT_PATH = App_config.GHOST_ATT_PATH


# 티스토리 백업 폴더에서 slug 리스트 가져오기
def get_slug_list(directory_path):
    file_list = os.listdir(directory_path)    
    return file_list


# slug 번호로 티스토리 html, 이미지, 첨부파일 정보를 찾기
def get_file_list(slug):
    slug = str(slug) # int로 들어오는 것을 방지
    all_files_list = {"slug":slug, "html_file":[], "img_files":[], "att_files":[]}
    
    html_path = Path(TISTROY_BACKUP_PATH) / slug
    if os.path.isdir(html_path):        
        html_files_list = html_path.iterdir()
        for item in html_files_list:
            if item.is_file():
                # print('파일명 :', item.name, '전체경로 :', item)
                all_files_list["html_file"].append(item.name)                            

    img_path = Path(TISTROY_BACKUP_PATH) / slug / 'img'
    if os.path.isdir(img_path):        
        img_files_list = img_path.iterdir()
        for item in img_files_list:
            if item.is_file():
                # print('파일명 :', item.name, '전체경로 :', item)
                all_files_list["img_files"].append(item.name)                
            
    att_path = Path(TISTROY_BACKUP_PATH) / slug / 'file'
    if os.path.isdir(att_path):        
        att_files_list = att_path.iterdir()
        for item in att_files_list:
            if item.is_file():
                # print('파일명 :', item.name, '전체경로 :', item)
                all_files_list["att_files"].append(item.name)                     
    
    return all_files_list


# slug 번호로 티스토리 이미지, 첨부파일 파일 고스트로 복사
def copy_img_and_att(slug):
    slug = str(slug) # int로 들어오는 것을 방지                         

    # 티스토리 백업에 이미지 파일이 있을 때
    img_path = Path(TISTROY_BACKUP_PATH) / slug / 'img'
    if os.path.isdir(img_path):
        # 고스트 content/img 내 slug 폴더 생성
        target_img_path = GHOST_IMG_PATH+'\\'+slug
        Path(target_img_path).mkdir(exist_ok=True)        
        
        img_files_list = img_path.iterdir()
        for item in img_files_list:
            if item.is_file():
                # print('파일명 :', item.name, '전체경로 :', item)                                
                source_img_file = item                
                target_img_file = target_img_path+'\\'+item.name
                if os.path.isfile(target_img_file):
                    print(f"{target_img_file}이(가) 이미 있습니다.")                    
                else:
                    print(f"{target_img_file}을 복사합니다.")
                    shutil.copyfile(source_img_file, target_img_file)

    # 티스토리 백업에 첨부 파일이 있을 때            
    att_path = Path(TISTROY_BACKUP_PATH) / slug / 'file'
    if os.path.isdir(att_path):
        # 고스트 content/files 내 slug 폴더 생성
        target_att_path = GHOST_ATT_PATH+'\\'+slug
        Path(target_att_path).mkdir(exist_ok=True)
        
        att_files_list = att_path.iterdir()
        for item in att_files_list:
            if item.is_file():
                # print('파일명 :', item.name, '전체경로 :', item)                
                source_att_file = item                
                target_att_file = target_att_path+'\\'+item.name
                if os.path.isfile(target_att_file):
                    print(f"{target_att_file}이(가) 이미 있습니다.")                    
                else:
                    print(f"{target_att_file}을 복사합니다.")
                    shutil.copyfile(source_att_file, target_att_file)
    
    return


# slug 번호로 첨부파일 파일 고스트로 복사
def copy_att(slug):
    slug = str(slug) # int로 들어오는 것을 방지                             

    # 티스토리 백업에 첨부 파일이 있을 때            
    att_path = Path(TISTROY_BACKUP_PATH) / slug / 'file'
    if os.path.isdir(att_path):
        # 고스트 content/files 내 slug 폴더 생성
        target_att_path = GHOST_ATT_PATH+'\\'+slug
        Path(target_att_path).mkdir(exist_ok=True)
        
        att_files_list = att_path.iterdir()
        for item in att_files_list:
            if item.is_file():
                # print('파일명 :', item.name, '전체경로 :', item)                
                source_att_file = item                
                target_att_file = target_att_path+'\\'+item.name
                if os.path.isfile(target_att_file):
                    print(f"{target_att_file}이(가) 이미 있습니다.")                    
                else:
                    print(f"{target_att_file}을 복사합니다.")
                    shutil.copyfile(source_att_file, target_att_file)
    
    return



# 아래는 사용 예

# # 티스토리 백업 폴더에 있는 게시물 수 확인
# print(f'{TISTROY_BACKUP_PATH}에 게시물이 {len(slug_list)}개 있습니다.')


# # 티스토리 백업 폴더에 있는 게시물 slug 확인
# print(f'게시물 목록 " {slug_list}')


# # 티스토리 백업 폴더에 있는 파일 목록 확인
# for slug in slug_list:    
#     data_list = Tistory_Read_info.get_file_list(slug)
#     print(data_list)


# # 티스토리 백업 폴더에 있는 파일 목록 확인(HTML파일만)
# for slug in slug_list:    
#     data_list = Tistory_Read_info.get_file_list(slug)
#     print(data_list['html_file'])


# # 티스토리 백업 폴더에 있는 파일 목록 확인(이미지 파일만)
# for slug in slug_list:    
#     data_list = Tistory_Read_info.get_file_list(slug)
#     print(data_list['img_files'])


# # 티스토리 백업 폴더에 있는 파일 목록 확인(첨부 파일만)
# for slug in slug_list:    
#     data_list = Tistory_Read_info.get_file_list(slug)
#     print(data_list['att_files'])  
