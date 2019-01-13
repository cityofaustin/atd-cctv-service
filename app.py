import json

from flask import Flask, redirect, flash, request

from secrets import SECRET_KEY

CAM_DATA_PATH = "/data/cameras.json"  #  mount JSON to /data/ on container launch
CAM_ID_KEY = "CAMERA_ID"
CAM_IP_FIELD = "CAMERA_IP"
CAM_ID_PARAM = "cam_id"

app = Flask(__name__)
app.secret_key = SECRET_KEY


def get_camera_by_id(path, key, val):
    #  return camera data that matches requested camera ID
    with open(path, "r") as fin:
        data = json.loads(fin.read())
        for row in data:
            if str(row[key]) == str(val):
                return row
        #  camera not found
        return None


@app.route("/")
def redir():
    """
    Redirect client to camera feed
    """

    #  Parse URL for camera ID
    cam_id = request.args.get(CAM_ID_PARAM)

    if cam_id:
        #  Get camera data from source JSON
        cam = get_camera_by_id(CAM_DATA_PATH, CAM_ID_KEY, cam_id)

        if cam:
            ip = cam[CAM_IP_FIELD]

            #  Redirect to camera feed
            return redirect(f"http://{ip}", code=302)

        return f"Camera ID {cam_id} not found :/"

    else:
        return "No camera specified."


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
