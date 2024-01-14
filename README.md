# Application README

## Overview
This application is a web-based interface built using Flask and Flask-SocketIO. It provides a terminal-like environment with additional features such as camera control, animatronics display, and interactive tasks for custom FNAF gameplay at home. Customize as you wish.

## Requirements
- Docker installed on the host machine.
- Docker daemon running.

## Instructions for Usage

1. Clone the repository to your local machine and navigate to the project directory:

```bash
git clone https://github.com/Morbid1134/Sim-Complex.git
cd Sim-Complex
```

2. If you have already cloned the repository and wish to update it with the latest changes, execute the following command:

```bash
git pull origin main
```

3. Build or rebuild the Docker image using the provided Dockerfile. Note: If you have previously built the Docker image and intend to update it, delete the previous container and image before rebuilding:

```bash
docker build -t your-image-name .
```

4. Execute the Docker container using the command below for foreground operation:

```bash
docker run -p 80:5000 your-image-name
```

Alternatively, for background execution:

```bash
docker run -d -p 80:5000 your-image-name
```

> Be sure to replace the `80` with your preferred port number. Use the updated port number in the URL. Only modify the first port number, as indicated by the `80:5000` format.

5. Access the application in your web browser by navigating to [http://localhost/](http://localhost/).

## Dockerfile
```Dockerfile
FROM ubuntu

RUN apt update
RUN apt install python3-pip -y
RUN pip3 install Flask==3.0.0
RUN pip3 install Flask_SocketIO==5.3.6

WORKDIR /app

COPY . .

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]
```

## Disclaimer
This application is for demonstration purposes only and should only be used on a local intranet. The creation of this application was not designed for general use and has specific features that would need redesigned for usable reproduction. Some features may not have actual functionality and are included for illustrative purposes. Their are also features that are not easily changed and could take some time for others to try to replicate in their own use of this project.

## Credits
This application was developed using Flask and Flask-SocketIO. Special thanks to the Flask and Socket.IO communities for their contributions. [Morbid](https://github.com/Morbid1134) was the sole Front-end/Back-end developer. Majority of built-in tasks were procured and re-designed to fit this application by [darkness](https://github.com/killas121).

## License
This application is licensed under the [MIT License](LICENSE).
