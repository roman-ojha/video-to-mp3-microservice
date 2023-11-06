import os
# 'gridfs' allow us to store larger file on mogodb
import gridfs
# 'pick' is an interface for out Queue for that we will use RabbitMQ service
import pika
import json
from flask import Flask, request
# 'flask_pymongo' to interact with mongodb so that we can store files
from flask_pymongo import PyMongo
from auth import validate
from auth_service import access
from storage import util

server = Flask(__name__)
# accessing mongodb from k8s cluster host machine
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

# PyMongo wrap our flask server which will allow us to interact with mongodb
mongo_video = PyMongo(
    server, uri="mongodb://host.minikube.internal:27017/videos")

mongo_mp3 = PyMongo(server, uri="mongodb://host.minikube.internal:27017/mp3s")

# GridFS wrap our mongodb which will enable us to use mongodb GridFS
# GridFS Explanation: https://youtu.be/hmkF77F9TLw?t=6076
fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

# Creating RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
# 'rabbitmq' string is referencing the RabbitMQ Host from the k8s cluster
channel = connection.channel()


# This route will going to communicate with 'Auth' Service to authenticate the user
@server.route("/login", methods=["POST"])
def login():
    # this 'access.login' function will going to communicate with the auth service using http request
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err
