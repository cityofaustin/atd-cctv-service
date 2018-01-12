import os
import json

from flask import Flask,redirect,flash,request

from secrets import SECRET_KEY

CAM_ID_KEY = 'CAMERA_ID'
CAM_ID_PARAM = 'cam_id'

path = os.environ.get('TDP_PATH')
app = Flask(__name__)
app.secret_key = SECRET_KEY


def get_camera_by_id(path, key, val):
    #  return camera data that matches requested camera ID
    with open(path, 'r') as fin:
        data = json.loads(fin)
        for row in data:
            if row[key] == val:
                return row
        #  camera not found
        return None


@app.route('/')
def redir():
    '''
    Redirect client to camera feed
    '''
    
    #  Parse URL for camera ID
    cam_id = request.args.get(CAM_ID_PARAM)
    
    #  Get camera data from source JSON
    cam = get_camera_by_id(
        path,
        CAM_ID_KEY,
        cam_id
    )
    ip = cam['ip']

    #  Redirect to camera feed
    return f'http://{ip}'


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')