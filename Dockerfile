FROM python:3.7-alpine as build

LABEL maintainer="Ludovic Ortega mastership@hotmail.fr"

# update package
RUN apk update

# install git
RUN apk add git

# download Dynhost project
RUN git clone https://github.com/M0NsTeRRR/Dynhost

# remove config file
RUN rm Dynhost/config.json

# copy file to /app/
RUN mkdir -p /app/Dynhost/ && mv Dynhost/* /app/Dynhost/

# install dependencies
RUN pip3 install -r ./app/Dynhost/requirements.txt

FROM python:3.7-alpine

# update package
RUN apk update

# copy Dynhost
COPY --from=build /app/Dynhost/ /app/Dynhost/

# copy python library
COPY --from=build  /usr/local/lib/python3.7/site-packages/ /usr/local/lib/python3.7/site-packages/

CMD ["python3", "/app/Dynhost/main.py"]