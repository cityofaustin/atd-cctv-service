sudo docker run --name  cctv-service \
    -d \
    -p 8000:8000 \
    -e LANG=C.UTF-8 \
    -v "/home/publisher/cctv-service/app":/app \
    -v "/home/publisher/transportation-data-publishing/transportation-data-publishing/data":/data/ \
    --name  cctv-service \
    atddocker/cctv-service \
    python app.py
