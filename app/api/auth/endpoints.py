from time import time
from flask_restx import Namespace, Resource
from flask import make_response, request, jsonify, json, current_app

from app.database.models.user import User
from app.database.models.sessions import Session
from app.database import db
from .schema import SignUpSchema, LoginSchema
from .models import signup_model, login_model

api = Namespace("auth", path="/auth")


@api.route("/signup")
class Sign_up(Resource):

    @api.expect(api.model("Sign up", signup_model, strict=True))
    def post(self):
        payload: json = SignUpSchema().load(request.get_json())
        email, password = payload["email"], payload["password"]

        if User.find_by_email(email):
            return {"Error": "email already registered."}, 409
        
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        token_time = current_app.config.get(
            "TOKEN_EXPIRE_MINUTES") * 60 + current_app.config.get(
                "TOKEN_EXPIRE_HOURS") * 3600
        
        token = user.encode_access_token()
        user_agent = request.headers.get("user-agent")
        id = user.create_session(user_agent)

        response = make_response(
            jsonify(status="success",
                    message="email successfuly registered",
                    access_token=token,
                    expire=time() + token_time), 200)
        response.set_cookie("access_token", token, max_age=token_time)
        response.set_cookie("refresh_token", id, max_age=current_app.config.get("REFRESH_TOKEN_LIFETIME"))
        return response


@api.route("/login")
class Login(Resource):

    @api.expect(api.model("Log in", login_model, strict=True))
    def post(self):
        user_agent = request.headers.get("user-agent")
        payload: json = LoginSchema().load(request.get_json())
        email, password = payload["email"], payload["password"]

        user = User.find_by_email(email)

        if not user:
            return {"Error":"not registered"}
        
        if not user.check_password(password):
            return {"Error": "wrond password"}
        
        token = user.encode_access_token()
        Session.drop_email(email)
        id = user.create_session(user_agent)
        token_time = current_app.config.get("TOKEN_EXPIRE_MINUTES") * 60 + current_app.config.get("TOKEN_EXPIRE_HOURS") * 3600
        
        response = make_response(
            jsonify(status="success",
                    message="user successfuly log in",
                    access_token=token,
                    expire=time() + token_time), 200)
        response.set_cookie("access_token", token, max_age=token_time)
        response.set_cookie("refresh_token", id, max_age=current_app.config.get("REFRESH_TOKEN_LIFETIME"))

        return response


@api.route("/logout")
class Logout(Resource):

    def get(self):
        try:
            refresh = request.cookies.get("refresh_token")
            Session.drop_id(refresh)
        except:
            pass

        response = make_response(jsonify(status="success",
                                 message="user successfuly log out."), 201)
        response.set_cookie("access_token", '', expires=0)
        response.set_cookie("refresh_token", '', expires=0)
        
        return response


@api.route("/refresh")
class Refresh_Token(Resource):

    def get(self):
        user_agent = request.headers.get("user-agent")
        old_refresh_token = request.cookies.get("refresh_token")
        try:
            old_token_data = Session.get(old_refresh_token).verify(user_agent)

            if not old_token_data:
                raise {"Error": "user's token time out."}
            
            Session.drop_id(old_refresh_token)

            user = User.find_by_email(old_token_data.get("email"))
            id = user.create_session(user_agent)
            token = user.encode_access_token()
            token_time = current_app.config.get(
            "TOKEN_EXPIRE_MINUTES") * 60 + current_app.config.get(
                "TOKEN_EXPIRE_HOURS") * 3600
            
            response = make_response(
                jsonify(status="success",
                        message="tokens refreshed",
                        access_token=token,
                        expire=time() + token_time), 200)
            response.set_cookie("access_token", token, max_age=token_time)
            response.set_cookie("refresh_token", id, max_age=current_app.config.get("REFRESH_TOKEN_LIFETIME"))
            return response
        
        except:
            response = make_response("Invalid tokens", 400)
            response.set_cookie("access_token", "", expires=0)
            response.set_cookie("refresh_token", "", expires=0)
            return response

