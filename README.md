# V2V Communication and Autonomous Driving Simulation

![Python](https://img.shields.io/badge/python-3.9-blue.svg)
![OpenCV](https://img.shields.io/badge/opencv-4.x-green.svg)
![Pygame](https://img.shields.io/badge/pygame-2.x-orange.svg)
![Arduino](https://img.shields.io/badge/arduino-C++-00979D.svg)

A simulation environment for Vehicle-to-Vehicle (V2V) communication and autonomous driving, showcasing the evolution of the project through different versions.

## About The Project

This project explores the concepts of V2V communication and autonomous driving through a series of simulations and hardware implementations. The project is divided into several versions, each building upon the previous one and demonstrating different aspects of the system.

## Features

*   **Client-Server Architecture:** Utilizes Python's socket programming for real-time communication between vehicles and a central server.
*   **Computer Vision:** Employs OpenCV and AprilTags for vehicle localization and orientation detection.
*   **Real-time Visualization:** A Pygame-based visualizer to display the positions and orientations of vehicles and other objects in the simulation.
*   **Hardware Integration:** Includes Arduino code for implementing V2V communication using nRF24L01 wireless modules.

## Project Structure

The project is organized into several directories, each representing a different version or component:

*   `Template/`: Basic client and server templates.
*   `Version_1/`: An early implementation of a client-server chat system for communication.
*   `Version_2/`: A refined version of the client-server communication system.
*   `Version_3/`: Arduino-based hardware implementation for V2V communication using nRF24L01 modules.
*   `Version_4/`: The most advanced version, featuring computer vision-based localization and a graphical visualizer.

## Getting Started

To get the `Version_4` simulation running, you'll need to have Python 3 and the following libraries installed.

### Prerequisites

It is recommended to create a `requirements.txt` file in the `Version_4` directory with the following content:

```txt
numpy
opencv-python
pyapriltags
pygame
```

You can then install these dependencies using pip:

```sh
pip install -r requirements.txt
```

### Running the Simulation

1.  **Start the Server:**
    ```sh
    python Version_4/server.py
    ```
2.  **Run the Vision System:**
    Connect a camera and run the vision script. You may need to adjust the camera index in `vision.py`.
    ```sh
    python Version_4/vision.py
    ```
3.  **Start the Visualizer:**
    ```sh
    python Version_4/visualize_server.py
    ```
4.  **Run the Client(s):**
    (Assuming you have client scripts that interact with the server)
    ```sh
    python Version_4/client.py
    ```

## Usage

Each version directory contains scripts that can be run independently. Refer to the source code in each directory for more details on how to run the specific simulations or hardware implementations.

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Project Link: [https://github.com/your_username/your_project_name](https://github.com/your_username/your_project_name)
