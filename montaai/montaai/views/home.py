from flask import Blueprint

home_blueprint = Blueprint("home", __name__)


@home_blueprint.route("/", methods=["GET"])
def home():
    return (
        f"""
        <!doctype html>
        <html>
            <head>
                <title>Monta AI </title>
            </head>
            <body>
                <h1>Monta AI BE Task </h1>
            </body>
        </html>""",
        200,
    )
