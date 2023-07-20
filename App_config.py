import configparser
import os


# 현재 .py파일이 존재하는 경로를 작업 경로로 설정
app_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(app_path)


# .ini파일에서 정보 불러오기
config = configparser.ConfigParser()
config.read(f'{app_path}/TistoryToGhost.ini', encoding='UTF8')
settings = config['SETTINGS']
AUTHOR = settings["AUTHOR"]
API_URL = settings["API_URL"]
CONTENT_API = settings["CONTENT_API"]
ADMIN_API = settings["ADMIN_API"]
IMAGE_METHOD = settings["IMAGE_METHOD"]
TISTROY_BACKUP_PATH = settings["TISTROY_BACKUP_PATH"]
GHOST_IMG_PATH = settings["GHOST_IMG_PATH"]
GHOST_ATT_PATH = settings["GHOST_ATT_PATH"]
GHOST_IMG_URL = settings["GHOST_IMG_URL"]
GHOST_ATT_URL = settings["GHOST_ATT_URL"]
SEARCH_IN_HTML = settings["SEARCH_IN_HTML"]
