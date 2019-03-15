"""
CCTV Redirect Service
"""
import json
import logging
import os
import urllib.request

import requests
from sanic import Sanic
from sanic import response
from sanic import exceptions

CAM_DATA_PATH = "/data/cameras.json"  #  mount JSON to /data/ on container launch
CAM_ID_KEY = "CAMERA_ID"
CAM_IP_FIELD = "CAMERA_IP"
CAM_ID_PARAM = "cam_id"


def load_data(path):
    with open(path, "r") as fin:
        data = json.loads(fin.read())

    return data


def get_camera_by_id(key, val):
    # we load data on every request to ensure the most recent 
    # source file is referenced
    data = load_data(CAM_DATA_PATH)

    #  return camera data that matches requested camera ID
    for row in data:
        if str(row[key]) == str(val):
            return row

    #  camera not found
    return None

app = Sanic()

@app.route("/")
async def index(request):
    """
    Redirect client to camera feed
    """

    #  Parse URL for camera ID
    cam_id = request.args.get(CAM_ID_PARAM)

    if cam_id:
        #  Get camera data from source JSON
        cam = get_camera_by_id(CAM_ID_KEY, cam_id)

        if cam:
            ip = cam[CAM_IP_FIELD]
            #  Redirect to camera feed
            return response.html(f"<h1><a href=\"http://{ip}\">Click here to view camera feed for camera {cam_id}</a></h1>")

        else:
            return response.text(f"Camera ID {cam_id} not found :/")

    else:
        return response.text("No camera specified.")


@app.exception(exceptions.NotFound)
async def ignore_404s(request, exception):
    return response.text("WHY: {}".format(exception))


if __name__ == "__main__":
    logging.basicConfig(filename='error.log',level=logging.DEBUG)
    app.run(debug=True, host="0.0.0.0")
