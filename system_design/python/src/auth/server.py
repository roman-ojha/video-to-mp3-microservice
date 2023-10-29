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


# First route
@server.route("/login", methods=["POST"])
def login():
    # request.authorization provide the credentials from the basic 'Authentication' Header which contain username and the password
    auth = request.authorization
    # auth.username for the username
    # auth.password for the password
    if not auth:
        return "missing credentials", 401

    # check db for username and password
