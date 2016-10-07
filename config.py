import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
	SECRET_KEY = 'DEBINANDHUIYANG'

	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	FLASKY_MAIL_SUBJECT_PREFIX = '[CEE-2016]'
	FLASKY_MAIL_SENDER = '18752026450@163.com'
	FLASKY_ADMIN = '710119343@qq.com'
	FLASKY_POSTS_PER_PAGE_1 = 13
	FLASKY_POSTS_PER_PAGE_2 = 15
	
	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.163.com'
	MAIL_PORT = '25'
	MAIL_USE_TLS = True
	MAIL_USERNAME = '18752026450@163.com'
	MAIL_PASSWORD = 'debin21'
	SQLALCHEMY_DATABASE_URI =\
		'sqlite:///' + os.path.join(basedir,'data-dev.sqlite')
class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI =\
		'sqlite:///' + os.path.join(basedir,'data-test.sqlite')
class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI =\
		'sqlite:///' + os.path.join(basedir,'data.sqlite')

config = {
	'development':DevelopmentConfig,
	'test':TestingConfig,
	'production':ProductionConfig,

	'default':DevelopmentConfig
}
