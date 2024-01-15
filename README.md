# Sim Complex

Sim Complex is a web-based interface inspired by FNAF, designed for home use, specifically developed for [darkness](https://github.com/killas121).

## Table of Contents

- [Sim Complex](#sim-complex)
  - [Table of Contents](#table-of-contents)
  - [About the Project](#about-the-project)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation with Python](#installation-with-python)
    - [Updating with Python](#updating-with-python)
    - [Installation with Docker](#installation-with-docker)
    - [Updating with Docker](#updating-with-docker)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## About the Project

Sim Complex is built as a web-based interface using Flask and Flask-SocketIO. It offers a terminal-like environment enriched with features such as camera control, animatronics display, and interactive tasks, allowing for a customized FNAF gameplay experience at home. Feel free to customize it according to your preferences.

## Getting Started

You can choose to run the game either on your local environment or isolate it in a Docker container.

### Prerequisites

Ensure that you have either Docker or Python installed on your system.

### Installation with Python

1. Navigate to your project directory:
   ```bash
   cd path/to/project/folder/
   ```
2. Clone the repository to your directory:
   ```bash
   git clone https://github.com/Morbid1134/Sim-Complex.git .
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask server:
   ```bash
   flask run --port 80 --host 0.0.0.0
   ```

### Updating with Python

1. Navigate to your project directory:
   ```bash
   cd path/to/project/folder/
   ```
2. Pull the latest changes from the Git repository:
   ```bash
   git pull
   ```
3. Update the required packages:
   ```bash
   pip install -r requirements.txt --upgrade
   ```
4. Restart the Flask server:
   ```bash
   flask run --port 80 --host 0.0.0.0
   ```

### Installation with Docker

1. Navigate to your project directory:
   ```bash
   cd path/to/project/folder/
   ```
2. Clone the repository to your directory:
   ```bash
   git clone https://github.com/Morbid1134/Sim-Complex.git .
   ```
3. Build the Docker image:
   ```bash 
   docker build -t your-image-name .
   ```
4. Run the Docker image in a container:
   ```bash
   docker run -p 80:5000 your-image-name
   ```

### Updating with Docker

1. Navigate to your project directory:
   ```bash
   cd path/to/project/folder/
   ```
2. Pull the latest changes from the Git repository:
   ```bash
   git pull
   ```
3. Build the updated Docker image:
   ```bash
   docker build -t your-image-name .
   ```
4. Stop and remove the existing Docker container:
   ```bash
   docker stop $(docker ps -a -q --filter ancestor=your-image-name)
   ```
   ```bash
   docker rm $(docker ps -a -q --filter ancestor=your-image-name)
   ```
5. Run the updated Docker image in a container:
   ```bash
   docker run -p 80:5000 your-image-name
   ```

Note: Adjust port mapping if your Docker container runs on different ports. Replace `your-image-name` with the actual name specified during Docker image building.

## Disclaimer

This application is for demonstration purposes only and should be used solely on a local intranet. It was not designed for general use, and specific features may need redesign for reproduction. Some features are included for illustrative purposes and may lack actual functionality. Additionally, certain features may not be easily changed and could require considerable effort for others to replicate in their use of this project.

## Contributing

This application was developed using Flask and Flask-SocketIO. Special thanks to the Flask and Socket.IO communities for their contributions. The sole Front-end/Back-end developer is [Morbid](https://github.com/Morbid1134), and the majority of built-in tasks were procured and re-designed to fit this application by [darkness](https://github.com/killas121).

## License

This application is licensed under the [MIT License](LICENSE).