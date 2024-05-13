from montaai.models.users import User
from montaai.helpers.database import db
import bcrypt


class UserService:
    @staticmethod
    def register(username: str, password: str):
        if User.query.filter_by(username=username).first():
            return {"error": "Can not register with this username"}, 400

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        user: User = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return {"message": "User registered successfully"}, 200

    @staticmethod
    def login(username: str, password: str):
        user: User = User.query.filter_by(username=username).first()
        if not user or not bcrypt.checkpw(
            password.encode("utf-8"), user.password.encode("utf-8")
        ):
            return {"error": "Invalid username or password"}, 401

        return {"message": "Login successful"}, 200
