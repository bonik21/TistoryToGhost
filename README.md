# TistoryToGhost
티스토리 포스팅 자료를 고스트로 이전하는 파이썬 스크립트
(작성중)


# 티스토리 데이터 백업 파일
- 관리자로 로그인
- 관리 - 블로그 - 데이터 관리
- 블로그 백업 생성 후 다운로드
- 백업파일 압축풀기
- 게시물별 고유URL로 나열된 폴더가 있는 경로를 ini파일에 추가
- 티스토리의 고유URL은 고스트에서 'slug'에 대응


# 고스트 API 사용설정
- 고스트 관리자로 로그인
- Settings - ADVANCED - Integrations
- `+ Add custom integration` 클릭
- 생성된 `Conten API key`, `Admin API key`, API URL'을 TistoryToGhost.ini에 입력
- `Content API key`로 콘텐츠를 불러올 수는 있지만 그것을 작성할 수는 없음.


# 주의
## HTML 손실
- API를 이용한 고스트의 데이터 입출력은 Mobiledoc으로 하며, HTML이용시 HTML  to Mobiledoc 변환이 필요함.
- HTML to Mobiledoc 변환은 손실이 있으며, <script></script>등은 변환되지 않음.
- 이 스크립트에서는 HTML to Mobiledoc 변환을 사용함.
- HTML to Markdown이나 HTML to Json은 이 스크립트에서 지원하지 않음.

## API 엔드포인트
- 변환을 위해서 API Endpoint를 `/ghost/api/admin/posts`가 아닌 `/ghost/api/admin/posts/?source=html`로 해야 함.

## 파일 경로
- 티스토리의 이미지 파일 경로는 `./img/파일명.jpg`이나 고스트의 `./content/images/파일명.jpg`가 기본임. 
- 경로 변경시 `content/images` 하위 경로만 가능.
- 티스토리의 이미지 첨부 경로는 `./file/파일명.txt`이나 고스트의 `./content/files/파일명.txt`가 기본임. 
- 경로 변경시 `content/files` 하위 경로만 가능.
- HTML 코드 내의 파일 경로 변경해야 하며 상대경로 입력시 `/tag/slug/`, `author/slug` 형식의 주소에서 제대로 안보일 수 있음.


# 필요한 패키지 설치
```
pip install -r requirements.txt
```
또는
```
pip install requests, beautifulsoup4, pyjwt
```
