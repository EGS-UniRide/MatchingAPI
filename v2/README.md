# MatchingAPI

To run the dockerized API, follow the steps bellow.

1. Build the API image.
    - ``sudo docker build --tag matching_api .``
2. Check if the image was successfully builded.
    - ``sudo docker images | grep matching_api``
3. Run the docker image.
    - ``sudo docker run -p 8030:8030 --name matching_api matching_api``
