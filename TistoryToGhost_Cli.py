import App_config
import argparse
import Tistory_Read_info, TistoryToGhost
import Ghost_Write_in_HTML


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
    parser.add_argument('--post', action='store_true', help='Run Ghost_Write_in_HTML.tistory_to_ghost(slug)')
    parser.add_argument('--check', action='store_true', help='Run Tistory_Read_info.get_file_list(slug)')
    args = parser.parse_args()

    slug = args.slug
    
    # slug가 숫자일 때
    if slug.isdigit():        
        if args.post:
            print(Colors.GREEN, f'티스토리 게시물 {slug}을(를) 고스트로 옮김니다.', Colors.RESET)
            TistoryToGhost.tistory_to_ghost(slug)
        
        elif args.check:
            print(Colors.GREEN, f'{slug}의 파일 목록을 확인합니다.', Colors.RESET)
            file_list=Tistory_Read_info.get_file_list(slug)
            print(file_list)
        
        else:
            print(Colors.GREEN, f'티스토리 게시물 {slug}을(를) 고스트로 옮김니다.', Colors.RESET)
            TistoryToGhost.tistory_to_ghost(slug)
    
    # slug가 'all'일 때
    elif slug.lower() == 'all':        
        if args.post:
            print(Colors.GREEN, f'{TISTROY_BACKUP_PATH}폴더의 모든 티스토리 게시물을 고스트로 옮김니다.', Colors.RESET)          
            TistoryToGhost.tistory_to_ghost_all()

        elif args.check:            
            print(Colors.GREEN, f'{TISTROY_BACKUP_PATH} 폴더의 게시물 목록을 표시합니다.', Colors.RESET)
            slug_list=Tistory_Read_info.get_slug_list(TISTROY_BACKUP_PATH)
            for slug in slug_list:
                data_list = Tistory_Read_info.get_file_list(slug)
                print(data_list)

        else:
            print(Colors.GREEN, f'{TISTROY_BACKUP_PATH}폴더의 모든 티스토리 게시물을 고스트로 옮김니다.', Colors.RESET)          
            TistoryToGhost.tistory_to_ghost_all()
    else:
        print(Colors.RED, "오류 : Slug 값은 숫자 혹은 'all' 이어야 합니다.", Colors.RESET)
