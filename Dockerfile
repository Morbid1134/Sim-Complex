FROM ubuntu

RUN apt update
RUN apt install python3-pip -y
RUN pip3 install Flask==3.0.0
RUN pip3 install Flask_SocketIO==5.3.6

WORKDIR /app

COPY . .

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]