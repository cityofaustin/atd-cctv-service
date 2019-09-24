#  cctv-service
CCTV service is a tiny Sanic app that connects COA staff to traffic camera feeds. It serves the purpose of re-directing on-network visitors to the public [Device Status Dashboard](http://transportation.austintexas.io/device-status) to the CCTV camera feeds which sit behind the COA firewall, and avoids the need for us to expose the CCTV IP addresses to the public internet.

Here's how it works:

1. You are connected to the City of Austin network, and you have been whitelisted to access the CCTV camera feeds.

2. You visit the [Device Status Dashboard](http://transportation.austintexas.io/device-status), select a CCTV camera, and click the link to view its video feed.

3. The link to view the feed hits the CCTV service, and looks like this `http://<server ip>:<port>?cam_id=204`. Where `cam_id` is the unique ID of the camera feed your're trying to view.

4. The CCTV service is only available on the city network, in which case the service will look up the IP address of the camera you requested, and redirect you to it.

##  Quick Start
1. Install [Docker](https://docs.docker.com/) and launch the Docker engine `systemctl start docker`.

2. Clone this repo and on your host and `cd` into the repo: `git clone http://github.com/cityofaustin/cctv-serivce && cd cctv-serivce`.

3. Build the Docker image: `docker build -t atddocker/cctv-service .`.

4. Launch the container/app (note how we mount an absolute path to our cctv camera data): 

```
sudo docker run -d \
    -p 5000:5000 \
    -e LANG=C.UTF-8 \
    -v "$(pwd)":/app/ \
    -v "/home/publisher/transportation-data-publishing/transportation-data-publishing/data":/data/ \
    --name  cctv-service \
    --rm \
    atddocker/cctv-service
```

5. Visit the app at `http://<your host IP>:5000?cam_id=<a valid camera id>`

## License

As a work of the City of Austin, this project is in the public domain within the United States.

Additionally, we waive copyright and related rights in the work worldwide through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
