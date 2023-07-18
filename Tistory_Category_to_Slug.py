# "원래 티스토리 카테고리": "원하는 고스트 tag" 띄워쓰기 정확해야 함
def convert_category_to_slug(category):
    mod_keywords = {"BoniK's WORKS/발매앨범": "BoniK's WORKS",
                    "BoniK's WORKS/작곡,편곡,미디편곡": "BoniK's WORKS",
                    "BoniK's WORKS/작사": "BoniK's WORKS",
                    "BoniK's WORKS/레슨,작업의뢰": "BoniK's WORKS",
                    "BoniK's WORKS/ETC.": "BoniK's WORKS",
                    "BoniK's WORKS/소프트웨어,스크립트": "BoniK's WORKS",
                    "실용음악 레슨/DAW로 배우는 재즈화성학": "강의-음악이론",
                    "실용음악 레슨/화성학 레슨": "강의-음악이론",
                    "실용음악 레슨/미디 (MIDI) 레슨": "강의-컴퓨터음악",
                    "실용음악 레슨/작곡, 편곡 레슨": "강의-작곡, 편곡",
                    "실용음악 레슨/청음 레슨": "강의-청음, 리듬트레이닝",
                    "실용음악 레슨/실용음악 자료실": "강의 자료실",
                    "실용음악 이야기/주목할 앨범, 공연": "음악 추천",
                    "실용음악 이야기/공모전,이벤트": "음악 이야기",
                    "실용음악 이야기/음악계 소식": "음악 이야기",
                    "실용음악 이야기/음악 소프트웨어": "음악 소프트웨어",
                    "실용음악 이야기/음악 장비": "음악 장비/작업실",
                    "실용음악 이야기/음악작업실, 룸튜닝": "음악 장비/작업실",
                    "실용음악 이야기/음악관련잡담": "음악 이야기",
                    "실용음악 이야기/Billboard Chart": "Billboard Chart",
                    "IT,게임,문학 이야기/컴퓨터, OS, 소프트웨어": "컴퓨터, 소프트웨어",
                    "IT,게임,문학 이야기/WEB, 인터넷": "Web, 인터넷",
                    "IT,게임,문학 이야기/통신, 스마트폰": "모바일",
                    "IT,게임,문학 이야기/게임": "게임",
                    "IT,게임,문학 이야기/문학, 출판": "독서/출판",
                    "다른 이야기/추천장비": "사용기",
                    "다른 이야기/추천서적": "독서/출판", # 재활용
                    "다른 이야기/유용한 정보": "삶의 지혜",
                    "다른 이야기/잡담": "잡담",
                    }
    for x, y in mod_keywords.items():
        category = category.replace(x, y)
        category = category.strip()  # 좌우 공백 제거
        category = ' '.join(category.split())  # 연속 공백 제거
    converted_category = category
    return converted_category
