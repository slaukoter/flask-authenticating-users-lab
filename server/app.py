#!/usr/bin/env python3

from flask import Flask, request, session
from flask_migrate import Migrate
from models import db, User, UserSchema

app = Flask(__name__)
app.secret_key = b'a\xdb\xd2\x13\x93\xc1\xe9\x97\xef2\xe3\x004U\xd1Z'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.get("/clear")
def clear():
    session.clear()
    return {}, 204


@app.post("/login")
def login():
    data = request.get_json() or {}
    username = data.get("username")

    user = User.query.filter(User.username == username).first()

    if user:
        session["user_id"] = user.id
        return UserSchema().dump(user), 200

    return {}, 401


@app.delete("/logout")
def logout():
    session.pop("user_id", None)
    return "", 204


@app.get("/check_session")
def check_session():
    user_id = session.get("user_id")

    if user_id:
        user = User.query.get(user_id)
        if user:
            return UserSchema().dump(user), 200

    return {}, 401


if __name__ == "__main__":
    app.run(port=5555, debug=True)
