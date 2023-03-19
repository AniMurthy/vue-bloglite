
class Config():
    DEBUG =True
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECUIRTY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"



class LocalDevelomentConfig(Config):
    SQLALCHEMY_DATABASE_URI= "sqlite:///BlogLiteDatabase.sqlite3"
    DEBUG = True
    SECRET_KEY= '123456'
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "really salt"
    SECURITY_REGISTERABLE = True
    SECURITY_USERNAME_ENABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    WTF_CSRF_ENABLED = False

