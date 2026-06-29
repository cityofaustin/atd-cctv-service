# cctv-service

CCTV service is a flask app that connects COA staff to traffic camera feeds. 

It serves the purpose of re-directing on-network visitors to the public [Traffic Cameras Dashboard](https://data.mobility.austin.gov/traffic-cameras) to the CCTV camera feeds which sit behind the COA firewall, and avoids the need for us to expose the CCTV IP addresses to the public internet.

Here's how it works:

1. You are connected to the City of Austin network, and you have been whitelisted to access the CCTV camera feeds.

2. You visit the [Traffic Cameras Dashboard](https://data.mobility.austin.gov/traffic-cameras), select a CCTV camera, and click the link to view its video feed.

3. The link to view the feed hits the CCTV service, and looks like this `http://<server ip>:<port>/camera/<camera_id>`. Where `camera_id` is the unique ID of the camera feed your're trying to view.

4. The CCTV service is only available on the city network, in which case the service will look up the IP address of the camera you requested, and redirect you to it.

5. Behind the scenes, another service (`cctv-fetcher`) periodicallyrefreshes the list of camera's that redirect server reads from.

## Local development

1. Install [Docker](https://docs.docker.com/) and launch the Docker engine `systemctl start docker`.

2. Clone this repo and on your host and `cd` into the repo: `git clone http://github.com/cityofaustin/cctv-serivce && cd cctv-serivce`.

3. Save a copy of `env_template` as `.env` and fill in the values.

4. Build the Docker images and start the service, using the `local` compose override to mount your local copy of the app into the container:

5. Test the redirect service by visiting a URL with a known camera ID, such as: `http://localhost:5001/camera/100`

```shell
docker compose -f docker-compose.yml -f docker-compose.local.yml up --build
```

## Production setup

6. The service is managed by `systemd`. To start, stop and restart the service, use the following:

```
# todo
sudo systemctl start cctv-service
sudo systemctl stop cctv-service
sudo systemctl restart cctv-service
```



## Testing



## License

As a work of the City of Austin, this project is in the public domain within the United States.

Additionally, we waive copyright and related rights in the work worldwide through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
