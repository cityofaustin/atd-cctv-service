import json
import logging

from flask import Flask, redirect, flash, request

from secrets import SECRET_KEY

CAM_DATA_PATH = "data/cameras.json"  #  mount JSON to /data/ on container launch
CAM_ID_KEY = "CAMERA_ID"
CAM_IP_FIELD = "CAMERA_IP"
CAM_ID_PARAM = "cam_id"

app = Flask(__name__)
app.secret_key = SECRET_KEY


def load_data(path):
    with open(path, "r") as fin:
        data = json.loads(fin.read())

    return data


def get_camera_by_id(data, key, val):
    #  return camera data that matches requested camera ID
    for row in data:
        if str(row[key]) == str(val):
            return row
    #  camera not found
    return None


@app.route("/")
def return_camera_url():
    """
    Redirect client to camera feed
    """

    # temp debugging to understand dropped requests
    logging.info(request)

    #  Parse URL for camera ID
    cam_id = request.args.get(CAM_ID_PARAM)

    if cam_id:
        #  Get camera data from source JSON
        cam = get_camera_by_id(data, CAM_ID_KEY, cam_id)

        if cam:
            ip = cam[CAM_IP_FIELD]

            #  Redirect to camera feed
            logging.info(f"return {ip}")
            
            return f"<h1><a href=\"http://{ip}\">{ip}</a></h1>"

        return f"Camera ID {cam_id} not found :/"

    else:
        return "No camera specified."


if __name__ == "__main__":
    logging.basicConfig(filename='error.log',level=logging.DEBUG)

    data = load_data(CAM_DATA_PATH)

    app.run(debug=True, host="0.0.0.0")
