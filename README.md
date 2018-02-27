#  cctv-service
A tiny flask app that connects COA staff to traffic camera feeds.

##  Quick Start
1. Install [Docker](https://docs.docker.com/) and launch the Docker engine `systemctl start docker`.

2. Clone this repo and on your host and `cd` into the repo: `git clone http://github.com/cityofaustin/cctv-serivce && cd cctv-serivce`.

3. Build the Docker image: `docker build -t atddocker/cctv-service .`.

4. Launch the container/app: 

```
sudo docker run -d \
    -p 5000:5000 \
    -e LANG=C.UTF-8 \
    -v "$(pwd)":/app/ \
    --rm \
    atddocker/cctv-service
```

5. Visit the app at `http://[Your host IP]:5000`

## License

As a work of the City of Austin, this project is in the public domain within the United States.

Additionally, we waive copyright and related rights in the work worldwide through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
