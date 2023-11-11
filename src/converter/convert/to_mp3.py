import pika
import json
import tempfile
import os
from bson.objectid import ObjectId
import moviepy.editor
# we will use 'moviepy' package to convert video to mp3: https://pypi.org/project/moviepy/


def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)  # loading our message as python object

    # creating empty temp file in temp directory where we can write our video so that later we can access the video to convert into mp3
    tf = tempfile.NamedTemporaryFile()
    # video contents:
    # get file from mongodb
    out = fs_videos.get(ObjectId(message["video_fid"]))
    # add video contents to empty file
    tf.write(out.read())
    # create audio from temp video file
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()

    # write audio to the file
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)

    # save file to mongo
    f = open(tf_path, "rb")
    data = f.read()
    fid = fs_mp3s.put(data)
    f.close()
    os.remove(tf_path)

    # Now we need to update the message
    message["mp3_fid"] = str(fid)

    # Now we need to put this updated message to new Queue called 'mp3'
    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        # if we can't add message to the queue then remove mp3 from mongodb
        fs_mp3s.delete(fid)
        return "failed to publish message"
