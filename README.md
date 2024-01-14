# Application README

## Overview
This application is a web-based interface built using Flask and Flask-SocketIO. It provides a terminal-like environment with additional features such as camera control, animatronics display, and interactive tasks for custom FNAF gameplay at home. Customize as you wish.

## Requirements
- Docker installed on the host machine.
- Docker daemon running.

## Usage
1. Clone the repository to your local machine and navigate to the project directory.
    ```bash
    git clone https://github.com/Morbid1134/Sim-Complex.git
    cd Sim-Complex
    ```

2. If you have already cloned the repository and want to update it, pull the latest changes:
    ```bash
    git pull origin main
    ```

3. Build the Docker image using the provided Dockerfile. If you have already built the Docker image and want to update it, you can rebuild it with the same image name you gave it before:
    ```bash
    docker build -t your-image-name .
    ```
    or
    ```bash
    docker build -d -t your-image-name .
    ```
    If you want the docker container to run in the background instead of from the terminal.
5. Run the Docker container:
    ```bash
    docker run -p 5000:5000 your-image-name
    ```
    You can adjust the first 5000 to any port you want. If you do then that is the port you should use in the URL.

6. Access the application in your web browser at [http://localhost:5000](http://localhost:5000).

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
