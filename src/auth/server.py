import jwt
# to set expiration date on our token
import datetime
import os
# using flask for server
from flask import Flask, request
from flask_mysqldb import MySQL
from decouple import config

# creating server
server = Flask(__name__)

# init MySQL
mysql = MySQL(server)

# config the server with different values:
# server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
# we can use command 'export MYSQL_HOST=localhost' to create env variable on our shell

# but we can use third party package to get env from '.env' files
server.config["MYSQL_HOST"] = config("MYSQL_HOST")
# print(server.config["MYSQL_HOST"])
server.config["MYSQL_USER"] = config("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = config("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = config("MYSQL_DB")
server.config["MYSQL_PORT"] = config("MYSQL_PORT")
# added all of the configuration variable here for the MySQL database connection


# First route
@server.route("/login", methods=["POST"])
def login():
    # request.authorization provide the credentials from the basic 'Authentication' Header which contain username and the password
    auth = request.authorization
    # auth.username for the username
    # auth.password for the password
    if not auth:
        return "missing credentials", 401

    # Basic Authentication Scheme
    # Authorization: Basic base64(<username>:<password>)
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization

    # check db for username and password
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )
    if res > 0:
        # if user exist
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]
        if auth.username != email or auth.password != password:
            return "Invalid credentials", 401
        else:
            return createJWT(auth.username, config("JWT_SECRET"), True)
    else:
        return "Invalid Credentials", 401


# route which will validate the JWT coming from the 'Authorization' Header
@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    # Bearer Authentication Scheme
    # Authorization: Bearer <token>

    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, config("JWT_SECRET"), algorithms=["HS256"]
        )
    except:
        return "not authorized", 403

    return decoded, 200


def createJWT(username, secret, authz):
    # authz is something that identify whether user is admin or not
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            # token expire in 1 days
            "iat": datetime.datetime.utcnow(),  # issued at
            "admin": authz,
        },
        secret,
        algorithm="HS256",  # single private key algorithm
    )


if __name__ == "__main__":
    # running the server on public ip
    server.run(host="0.0.0.0", port=5000)
    # Explanation: https://youtu.be/hmkF77F9TLw?t=2631
