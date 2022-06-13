FROM python:3.9.13-bullseye

RUN apt update && apt install -y --no-install-recommends \
     p7zip-full rdfind wget curl \
     git 

COPY . .

RUN pip3 install -r requirements.txt

CMD [ "bash", "start.sh" ]
