from time import time
from uuid import uuid4

import jwt
from flask import current_app, jsonify

from app.database import db
from app.bcrypt import bcrypt
from app.database.models.sessions import Session


class User(db.Model):

    __tablename__ = "site_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    public_id = db.Column(db.String(36),
                          unique=True,
                          default=lambda: str(uuid4()))

    def __repr__(self):
        return (
            f"<User email={self.email}, public_id={self.public_id}, admin={self.admin}>"
        )

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password):
        log_rounds = current_app.config.get("BCRYPT_LOG_ROUNDS")
        hash_bytes = bcrypt.generate_password_hash(password, log_rounds)
        self.password_hash = hash_bytes.decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_public_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()

    def create_session(self, user_agent): 
        try:
            id = str(uuid4())
            refresh_session = Session(
                id=id,
                user_agent=user_agent,
                expiry=int(time()) +
                current_app.config.get('REFRESH_TOKEN_LIFETIME'),
                email=self.email,
                admin=self.admin)
            db.session.add(refresh_session)
            db.session.commit()
            return id
        except Exception as ex:
            print(ex)
            db.session.rollback()
            return False

    def encode_access_token(self):
        token_age_h = current_app.config.get("TOKEN_EXPIRE_HOURS")
        token_age_m = current_app.config.get("TOKEN_EXPIRE_MINUTES")
        expire = int(time()) + token_age_h * 3600 + token_age_m * 60
        payload = dict(exp=expire,
                       iat=int(time()),
                       sub=self.public_id,
                       admin=self.admin)
        key = current_app.config.get("SECRET_KEY")
        return jwt.encode(payload, key, algorithm="HS256")

    @staticmethod
    def decode_access_token(access_token):
        try:
            key = current_app.config.get("SECRET_KEY")
            payload = jwt.decode(access_token, key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            error = "Access token expired. Please log in again."
            return {"Error": error}
        except jwt.InvalidTokenError:
            error = "Invalid token. Please log in again."
            return {"Error": error}, 404

        user_dict = dict(
            public_id=payload["sub"],
            admin=payload["admin"],
            token=access_token,
            expires_at=payload["exp"],
        )
        return user_dict
