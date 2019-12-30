import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

WIN = sys.platform.startswith('win')
if WIN:
	prefix = 'sqlite:///'
else:
	prefix = 'sqlite:////'

class Operations:
	CONFIRM = 'confirm'
	RESET_PASSWORD = 'reset-password'
	CHANGE_EMAIL = 'change-email'

class BaseConfig:
	ALBUMY_ADMIN_EMAIL = os.getenv('ALBUMY_ADMIN', 'laonana@laonana.com')
	ALBUMY_PHOTO_PER_PAGE = 12
	ALBUMY_COMMENT_PER_PAGE = 15
	ALBUMY_NOTIFICATION_PER_PAGE = 20
	ALBUMY_USER_PER_PAGE = 20
	ALBUMY_MANAGE_PHOTO_PER_PAGE = 20
	ALBUMY_MANAGE_USER_PER_PAGE = 30
	ALBUMY_MANAGE_TAG_PER_PAGE = 50
	ALBUMY_MANAGE_COMMENT_PER_PAGE = 30
	ALBUMY_SEARCH_RESULT_PER_PAGE = 20
	ALBUMY_MAIL_SUBJECT_PREFIX = '[Albumy]'
	ALBUMY_UPLOAD_PATH = os.path.join(basedir, 'uploads')
	ALBUMY_PHOTO_SIZE = {'small': 400, 'medium': 800}
	ALBUMY_PHOTO_SUFFIX = {ALBUMY_PHOTO_SIZE['small']: '_s', ALBUMY_PHOTO_SIZE['medium']: '_m',}
	SECRET_KEY = os.getenv('SECRET_KRY', 'I am a sexy boy')
	MAX_CONTENT_LENGTH = 3*1024*1024
	BOOTSTRAP_SERVE_LOCAL = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	AVATARS_SAVE_PATH = os.path.join(ALBUMY_UPLOAD_PATH, 'avatars')
	AVATARS_SIZE_TUPLE = (30, 100, 200)
	MAIL_SERVER = os.getenv('MAIL_SERVER')
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USERNAME = os.getenv('MAIL_USERNAME')
	MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
	MAIL_DEFAULT_SENDER = ('Albumy Admin', MAIL_USERNAME)
	DROPZONE_ALLOWED_FILE_TYPE = 'image'
	DROPZONE_MAX_FILE_SIZE = 3
	DROPZONE_MAX_FILES = 30
	DROPZONE_ENABLE_CSRF = True
	WHOOSHEE_MIN_STRING_LEN = 1

class DevelopmentConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')
	REDIS_URL = "redis://localhost"

class TestingConfig(BaseConfig):
	TESTING = True
	WTF_CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///'

class ProductionConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))

config = {'development': DevelopmentConfig, 'testing': TestingConfig, 'production': ProductionConfig, }
