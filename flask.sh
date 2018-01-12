#!/bin/bash

#  verify that the TDP path env var exists in the bash profile
cat ~/.bashrc

#  If needed append the transportat-data-publishing build path var to bash profile
#  Only need to do this once -- it persists
TDP_PATH=$(pwd) 
echo export TDP_PATH=$TDP_PATH >> ~/.bashrc

#  Copy files to host (dev only)
scp * claryj@atdatmsscript.austintexas.gov:/home/claryj/flask

#  launch Flask container
docker run -it --rm -p 5000:5000 -e LANG=C.UTF-8 -v "$(pwd)":/app/ flask

# boom!
http://10.66.2.55:5000/