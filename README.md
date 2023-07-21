# TistoryToGhost
티스토리 포스팅 자료를 고스트로 이전하는 파이썬 스크립트
고스트 CMS : https://ghost.org/

# 준비물
## 티스토리 데이터 백업 파일
- 관리자로 로그인
- 관리 - 블로그 - 데이터 관리
- 블로그 백업 생성 후 다운로드
- 백업파일 압축풀기
- 게시물별 고유URL로 나열된 폴더가 있는 경로를 ini파일에 추가
- 티스토리의 고유URL은 고스트에서 'slug'에 대응
- 티스토리 서식, 공지는 미리 삭제후 백업 다운로드 혹은 다운로드 후 해당 폴더를 격리

## 고스트 API 사용설정
- 고스트 관리자로 로그인
- Settings - ADVANCED - Integrations
- `+ Add custom integration` 클릭
- 생성된 `Conten API key`, `Admin API key`, API URL'을 TistoryToGhost.ini에 입력
- `Content API key`로 콘텐츠를 불러올 수는 있지만 그것을 작성할 수는 없음.


## 필요한 패키지 설치
```
pip install -r requirements.txt
```
또는
```
pip install requests, beautifulsoup4, pyjwt
```

## TistoryToGhost.ini 파일을 작성
- TistoryToGhost-example.ini을 참고해서 TistoryToGhost.ini 파일 작성
- 한글 포함시 인코딩 확인(UTF-8)

## Tistory_Custom.py 파일을 본인 설정에 맞게 수정
- 기존 내용을 참고해서 수정


# 참고
## HTML 손실
- API를 이용한 고스트의 데이터 입출력은 Mobiledoc으로 하며, HTML이용시 HTML  to Mobiledoc 변환이 필요함.
- HTML to Mobiledoc 변환은 손실이 있으며, <script></script>등은 변환되지 않음.
- 이 스크립트에서는 HTML to Mobiledoc 변환을 사용함.
- HTML to Markdown이나 HTML to Json은 이 스크립트에서 지원하지 않음.

## API 엔드포인트
- 변환을 위해서 API Endpoint를 `/ghost/api/admin/posts`가 아닌 `/ghost/api/admin/posts/?source=html`로 해야 함.

## 파일 처리 방식
### 이미지 파일 : 복사
- 이미지 파일을 서버로 직접 복사 (rclone등으로 서버의 스토리지를 로컬에 마운트 해야 함)

### 이미지 파일 : 업로드(추천)
- 이미지 파일을 서버로 업로드 (외부이미지도 서버에 저장 가능)

### 첨부파일 : 복사만 지원(마운트 필요)
- 첨부파일은 복사 밖에 지원하지 않음 (서버가 외부에 있을 경우 rclone등으로 서버의 스토리지를 로컬에 마운트 해야 함)
- 첨부파일을 수동으로 복사하려면 file폴더를 미리 수동으로 복사한 후에 백업 폴더에서 삭제 후 스크립트 실행

# CLI 사용법(윈도우에서만 테스트 됨)
- ini 작성 제대로 되었는지 확인
- html소스에 따라 오류가 발생할 수 있으므로 TISTROY_BACKUP_PATH에 게시물을 조금씩 옮겨서 실행하는 것을 추천

### 사용 예
```
# 123번 게시물의 파일 확인
python TistoryToGhost_Cli.py --check 123

# 123번 게시물 고스트로 포스팅
python TistoryToGhost_Cli.py 123
python TistoryToGhost_Cli.py --post 123
python TistoryToGhost_Cli.py -p 123

# TISTORY_BACKUP_PATH의 모든 게시물 확인
python TistoryToGhost_Cli.py --check all
python TistoryToGhost_Cli.py -c all

# TISTORY_BACKUP_PATH의 모든 게시물 포스팅
python TistoryToGhost_Cli.py all
python TistoryToGhost_Cli.py --post all
python TistoryToGhost_Cli.py -p all


# TISTORY_BACKUP_PATH의 모든 .html파일에서 키워드 검색
python TistoryToGhost_Cli.py --search "검색어"
python TistoryToGhost_Cli.py -s "검색어"

# TISTORY_BACKUP_PATH의 모든 파일 유효성 검사 및 .html 오류 검색
python TistoryToGhost_Cli.py --search all
python TistoryToGhost_Cli.py -s all
```