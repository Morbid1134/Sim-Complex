# Application Readme

## Overview
This application is a web-based interface built using Flask and Flask-SocketIO. It provides a terminal-like environment with additional features such as camera control, animatronics display, and interactive tasks for custom FNAF gameplay at home. Customize as you wish.

## Requirements
- Docker installed on the host machine.
- Docker daemon running.

## Usage
1. Clone the repository to your local machine.
2. Build the Docker image using the provided Dockerfile:
    ```bash
    docker build -t your-image-name .
    ```
3. Run the Docker container:
    ```bash
    docker run -p 5000:5000 your-image-name
    ```
4. Access the application in your web browser at [http://localhost:5000](http://localhost:5000).

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

# Application Readme

## Overview
This application is a web-based interface built using Flask and Flask-SocketIO. It provides a terminal-like environment with additional features such as camera control, animatronics display, and interactive tasks.

## Requirements
- Docker installed on the host machine.

## Usage
1. Clone the repository to your local machine.
2. Build the Docker image using the provided Dockerfile:
    ```bash
    docker build -t your-image-name .
    ```
3. Run the Docker container:
    ```bash
    docker run -p 5000:5000 your-image-name
    ```
4. Access the application in your web browser at [http://localhost:5000](http://localhost:5000).

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
This application is for demonstration purposes only and should only be used on a local intranet. Some features may not have actual functionality and are included for illustrative purposes. Their are also features that are not easily changed and could take some time for others to try to replicate in their own use of this project.

## Credits
This application was developed using Flask and Flask-SocketIO. Special thanks to the Flask and Socket.IO communities for their contributions. [Morbid](https://github.com/Morbid1134) was the sole Front-end/Back-end developer. Majority of built-in tasks were procured and re-designed to fit this application by **thecomplexer** (unknown reference URL).

## License
This application is licensed under the [MIT License](LICENSE).