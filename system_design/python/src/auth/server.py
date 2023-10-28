import jwt
# to set expiration date on our token
import datetime
import os
# using flask for server
from flask import Flask, request
from flask_mysqldb import MySQL
