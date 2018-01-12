#  cctv-service
A tiny flask app that connects COA staff to traffic camera feeds.

##  Quick Start
1. Install [Docker](https://docs.docker.com/) and launch the Docker engine `systemctl start docker`.

2. Clone this repo and on your host and `cd` into the repo: `git clone http://github.com/cityofaustin/cctv-serivce && cd cctv-serivce`.

3. Build the Docker image: `docker build -t flask .`.

4. Launch the container/app: 

```
sudo docker run -d \
    -p 5000:5000 \
    -e LANG=C.UTF-8 \
    -v "$(pwd)":/app/ \
    --rm \
    flask
```

5. Visit the app at `http://[Your host IP]:5000`