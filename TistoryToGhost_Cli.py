import App_config
import argparse
import Tistory_Read_info, TistoryToGhost
import Ghost_Write_in_HTML

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
            print(f'티스토리 게시물 {slug}을(를) 고스트로 옮김니다.')
            TistoryToGhost.tistory_to_ghost(slug)
        
        elif args.check:
            print(f'{slug}의 파일 목록을 확인합니다.')
            file_list=Tistory_Read_info.get_file_list(slug)
            print(file_list)
        
        else:
            print(f'티스토리 게시물 {slug}을(를) 고스트로 옮김니다.')
            TistoryToGhost.tistory_to_ghost(slug)
    
    # slug가 'all'일 때
    elif slug.lower() == 'all':        
        if args.post:
            print(f'{TISTROY_BACKUP_PATH}폴더의 모든 티스토리 게시물을 고스트로 옮김니다.')          
            TistoryToGhost.tistory_to_ghost_all()

        elif args.check:            
            print(f'{TISTROY_BACKUP_PATH} 폴더의 게시물 목록을 표시합니다.')
            slug_list=Tistory_Read_info.get_slug_list(TISTROY_BACKUP_PATH)
            for slug in slug_list:
                data_list = Tistory_Read_info.get_file_list(slug)
                print(data_list)

        else:
            print(f'{TISTROY_BACKUP_PATH}폴더의 모든 티스토리 게시물을 고스트로 옮김니다.')          
            TistoryToGhost.tistory_to_ghost_all()
    else:
        print("Slug 값은 숫자 혹은 'all' 이어야 합니다.")
