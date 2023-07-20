import App_config
import argparse
import Tistory_Read_info, TistoryToGhost
import Ghost_Write_in_HTML, Ghost_Read_with_admin_api


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


TISTROY_BACKUP_PATH = App_config.TISTROY_BACKUP_PATH

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tistory To Ghost CLI')

    # 위치 인자(slug)
    parser.add_argument('slug', help='Slug value (number or "all")')

    # 옵션 인자
    parser.add_argument('-p', '--post', action='store_true', help='Run Ghost_Write_in_HTML.tistory_to_ghost(slug)')
    parser.add_argument('-c', '--check', action='store_true', help='Run Tistory_Read_info.get_file_list(slug)')
    parser.add_argument('-g', '--ghost', action='store_true', help='Ghost_Read_with_admin.is_slug_in_Ghost(slug)')
    parser.add_argument('-s', '--search', action='store_true', help='Search Keywords')

    args = parser.parse_args()

    slug = args.slug

    # slug가 'all'일 때
    if slug.lower() == 'all':  
        # --post : 티스토리 백업 경로 내의 모든 폴더를 고스트로 포스팅      
        if args.post:
            print(Colors.GREEN, f'{TISTROY_BACKUP_PATH}폴더의 모든 티스토리 게시물을 고스트로 옮김니다.', Colors.RESET)          
            TistoryToGhost.tistory_to_ghost_all()
        
        # --check : 티스토리 백업 경로 내의 모든 파일 검사
        elif args.check:            
            print(Colors.GREEN, f'{TISTROY_BACKUP_PATH} 폴더의 게시물 목록을 표시합니다.', Colors.RESET)
            slug_list=Tistory_Read_info.get_slug_list(TISTROY_BACKUP_PATH)
            for slug in slug_list:
                print()
                print()
                print(Colors.BLUE, "-"*40,  f"게시물 [{slug}] 정보", "-"*40, Colors.RESET)    
                data_list = Tistory_Read_info.get_file_list(slug)
                print(data_list)

        # --ghost : 고스트에 등록된 게시물 수 확인
        elif args.ghost:            
            print(Colors.GREEN, f'고스트에 있는 게시물 수를 확인합니다.', Colors.RESET)
            number_of_contents = Ghost_Read_with_admin_api.number_of_ghost_content()
            print('고스트에 등록된 게시물 :',number_of_contents ,'개')

        # --search : 오류, 경고만 검색
        elif args.search:
            keyword = ''
            print(Colors.GREEN, f'티스토리 백업 폴더 내에서 파일과 HTML 코드의 오류를 검색합니다.', Colors.RESET)
            slug_list=Tistory_Read_info.get_slug_list(TISTROY_BACKUP_PATH)
            for slug in slug_list:                
                data_list = Tistory_Read_info.get_file_list(slug)
            #     html_file = data_list["html_file"][0]
            #     html_path = f"{TISTROY_BACKUP_PATH}\{slug}\{html_file}"
            #     Tistory_Read_info.is_in_html(html_path, keyword)                    

        # 옵션이 없을 때 : --post와 같음
        else:
            print(Colors.GREEN, f'{TISTROY_BACKUP_PATH}폴더의 모든 티스토리 게시물을 고스트로 옮김니다.', Colors.RESET)          
            TistoryToGhost.tistory_to_ghost_all()

    # slug가 'all'이 아닐 때
    else:
        # --post : 티스토리 slug폴더를 고스트로 포스팅
        if args.post:
            print(Colors.GREEN, f'티스토리 게시물 {slug}을(를) 고스트로 옮김니다.', Colors.RESET)
            TistoryToGhost.tistory_to_ghost(slug)
        
        # --check : 티스토리 slug폴더의 파일 목록 확인
        elif args.check:
            print(Colors.GREEN, f'{slug}의 파일 목록을 확인합니다.', Colors.RESET)
            file_list=Tistory_Read_info.get_file_list(slug)
            print(file_list)
        
        # --check : 고스트에 slug가 포스팅 되어 있는지 확인
        elif args.ghost:
            print(Colors.GREEN, f'고스트에 {slug}이(가) 있는지 확인합니다.', Colors.RESET)
            if Ghost_Read_with_admin_api.is_slug_in_Ghost(slug):                
                print(Colors.GREEN, f"경고 : 고스트에 {slug}이(가) 포스팅되어 있습니다.", Colors.RESET)
            else:   
                print(Colors.GREEN, f"고스트에 {slug}이(가) 없습니다.", Colors.RESET)
        
        # --search : 티스토리 게시물 키워드 검색
        elif args.search:
            keyword = args.slug
            print(Colors.GREEN, f'티스토리 백업 폴더의 .html 코드에서 [{slug}]을(를) 검색을 시작합니다.', Colors.RESET)
            slug_list=Tistory_Read_info.get_slug_list(TISTROY_BACKUP_PATH)
            for slug in slug_list:                
                data_list = Tistory_Read_info.get_file_list(slug)
                html_file = data_list["html_file"][0]
                html_path = f"{TISTROY_BACKUP_PATH}\{slug}\{html_file}"
                if Tistory_Read_info.is_in_html(html_path, keyword):
                    print(Colors.BLUE, f"[{keyword}] : {html_path}", Colors.RESET)

        # 옵션이 없을 때 : --post와 같음
        else:
            print(Colors.GREEN, f'티스토리 게시물 {slug}을(를) 고스트로 옮김니다.', Colors.RESET)
            TistoryToGhost.tistory_to_ghost(slug)

