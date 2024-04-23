import os
from os import path, getcwd

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{path.join(getcwd(),'app/database/database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "open sesame")
    TOKEN_EXPIRE_HOURS = 0
    TOKEN_EXPIRE_MINUTES = 5
    REFRESH_TOKEN_LIFETIME = 2000000
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SWAGGER_UI_DOC_EXPANSION = "list"
    RESTX_MASK_SWAGGER = False
    JSON_SORT_KEYS = False