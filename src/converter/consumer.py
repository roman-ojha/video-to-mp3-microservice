import pika
import sys
import os
import time
from pymongo import MongoClient
import gridfs
from convert import to_mp3


def main():
    # mongodb is not deployed in our cluster it is not our host machine
    client = MongoClient("host.minikube.internal", 27017)
    db_videos = client.videos  # video database
    db_mp3s = client.mp3s  # mp3s database
    # gridfs
    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)

    # rabbitmq connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        # converting video to message inside this function
        err = to_mp3.start(body, fs_videos, fs_mp3s, ch)
        if err:
            # if error then sending negative acknowledge to the channel
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            # if conversion happen then we will acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)

    # now we need to create a configuration to consume our messages from our 'video' queue
    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"), on_message_callback=callback
        # whenever the message get pulls off from the queue then 'callback' function will get execute
    )

    print("Waiting for messages. To exit press CTRL+C")

    # this function will run our consumer and listen on our Queue channel
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # After press CTRL+C
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
