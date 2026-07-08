# cctv-service

CCTV service is a flask app that connects COA staff to traffic camera feeds.

It serves the purpose of re-directing on-network visitors to the public [Traffic Cameras Dashboard](https://data.mobility.austin.gov/traffic-cameras) to the CCTV camera feeds which sit behind the COA firewall, and avoids the need for us to expose the CCTV IP addresses to the public internet.

Here's how it works:

1. You are connected to the City of Austin network, and you have been whitelisted to access the CCTV camera feeds.

2. You visit the [Traffic Cameras Dashboard](https://data.mobility.austin.gov/traffic-cameras), select a CCTV camera, and click the link to view its video feed.

3. The link to view the feed hits the CCTV service, and looks like this `http://<server ip>:<port>/camera/<camera_id>`. Where `camera_id` is the unique ID of the camera feed you're trying to view.

4. The CCTV service is only available on the city network, in which case the service will look up the IP address of the camera you requested, and redirect you to it.

5. Behind the scenes, another service (`cctv-fetcher`) periodically refreshes the list of camera's that the redirect server reads from.

## Components

The app has two containerized components which are orchestrated by Docker Compose:

### Server

The server (`/server`) container runs the Flask API that provides the camera IP lookup + redirect.

### Fetcher

The fetcher (`/fetcher`) container periodically fetches camera asset data and refreshes the list of cameras that the API reads from. The fetcher container itself uses `cron` to execute a short script that uses `knackpy` to query out Knack-based asset management app.

Whenever the `/fetcher` service fetches new cameras, it also writes a timestamp to `cameras.log`. This timestamp is consumed by the API healthcheck to provide observability. See [Monitoring](#monitoring).

## Monitoring

The `/healthz` endpoint is available for monitoring the state of the service. It runs three checks in order, returning on the first failure:

1. **Data loadable** — confirms the camera data file at `CAM_DATA_PATH` can be loaded.
2. **Timestamp readable** — confirms the last fetch timestamp can be read from `FETCH_LOG_PATH`.
3. **Data freshness** — confirms the data's age does not exceed `MAX_DATA_AGE_SECONDS`.

### Responses

#### `200 OK` — Healthy

```json
{
  "status": "healthy",
  "last_fetch_timestamp": 1719763200,
  "message": "ok"
}
```

#### `503 Service Unavailable` — Unhealthy

Returned when any check fails. The `message` field describes the cause:

| Failure                          | `message`                               |
| -------------------------------- | --------------------------------------- |
| Data file missing or unparseable | `Unable to load camera data`            |
| Timestamp read error             | `Unable to read last fetch timestamp`   |
| Data is stale                    | `Camera data is stale (age: N minutes)` |

```json
{
  "status": "unhealthy",
  "last_fetch_timestamp": null,
  "message": "Unable to load camera data"
}
```

## Local development

1. Install [Docker](https://docs.docker.com/) and launch the Docker engine `systemctl start docker`.

2. Clone this repo and on your host and `cd` into the repo: `git clone http://github.com/cityofaustin/cctv-service && cd cctv-service`.

3. Save a copy of `env_template` as `.env` and fill in the values.

4. Build the Docker images and start the service, using the `local` compose override to mount your local copy of the app into the container:

```shell
docker compose -f docker-compose.yml -f docker-compose.local.yml up --build
```

5. Test the redirect service by visiting a URL with a known camera ID, such as: `http://localhost:5001/camera/100`

## Production setup

The service is managed by docker compose. This command will build and start the stack in detached mode (`-d`).

```
docker compose up --build -d
```

## License

As a work of the City of Austin, this project is in the public domain within the United States.

Additionally, we waive copyright and related rights in the work worldwide through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
