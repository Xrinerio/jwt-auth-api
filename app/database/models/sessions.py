from app.database import db
from time import time


class Session(db.Model):
    id = db.Column(db.String(18),
                   primary_key=True,
                   unique=True,
                   nullable=False)
    user_agent = db.Column(db.String(200), nullable=False)
    expiry = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    admin = db.Column(db.Boolean, default=False)

    @classmethod
    def drop_id(cls, identificator):
        try:
            cls.query.filter_by(id=identificator).delete()
            db.session.commit()
        except:
            db.session.rollback()

    @classmethod
    def drop_email(cls, identificator):
        try:
            cls.query.filter_by(email=identificator).delete()
            db.session.commit()
        except:
            db.session.rollback()

    @classmethod
    def get(cls, id):
        refresh_session = cls.query.filter_by(id=id).first()
        return refresh_session

    def verify(self, user_agent):
        token_data = self.__dict__
        if token_data.get("expiry") > int(
                time()) and token_data.get("user_agent") == user_agent:
            return token_data
        return False
