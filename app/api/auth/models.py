from flask_restx import fields, Model

signup_model: dict = {
    "email": fields.String(description="User's email address.", example="test@test.test"),
    "password": fields.String(description="User's password", min_lenght=6, max_lenght=64, example="test")
}

login_model: dict = {
    "email": fields.String(description="User's email address.", example="test@test.test"),
    "password": fields.String(description="User's password", min_lenght=6, max_lenght=64, example="test")
}

refresh_model: dict = {
    "refresh_token": fields.String(description="User's refresh token. (from cookie)", example="usersrefreshtoken")
}
