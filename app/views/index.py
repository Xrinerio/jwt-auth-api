from flask import Blueprint, redirect, url_for, request, render_template, abort

from app.database.models.user import User

index_bp = Blueprint("index", __name__, url_prefix="/")


@index_bp.route('/')
def index():
    encoded_token = request.cookies.get("access_token")
    token_data = User.decode_access_token(encoded_token)

    if token_data is None:
        abort(401)
    try:
        user_data = User.find_by_public_id(token_data['public_id'])
        return render_template("index.html", email=user_data)
    except:
        return render_template("index.html")

