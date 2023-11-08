import pika
import json


# This function fist upload the video into MongoDB and after file being successfully uploaded we need to put Message into RabbitMQ so that downstream service can pull the message from the queue and pull The video from MongoDB
def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)  # putting file into MongoDB
    except Exception as err:
        print(err)
        return "internal server error", 500

    # Creating message to send into Queue
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        # Putting message into the Queue
        channel.basic_publish(
            exchange="",  # default exchange
            routing_key="video",  # name of our Queue
            # convert python object message into json formatted string
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )

    except Exception as err:
        print(err)
        fs.delete(fid)
        return "internal server error", 500
