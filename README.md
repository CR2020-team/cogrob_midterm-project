# cogrob_midterm-project

Midterm project for Cognitive Robotics 2020/2021 - Group 26

## Assignment

[assignment.pdf](assignment.pdf)

## Team Members

* [Giovanni Ammendola](https://github.com/giorge1)
* [Edoardo Maffucci](https://github.com/emaff)
* [Vincenzo Petrone](https://github.com/v8p1197)
* [Salvatore Scala](https://github.com/knowsx2)

## Architecture

The project is organized into 5 ROS nodes:

* [camera_node](pepper_pkg/src/camera_node/main.py)
    * Makes Pepper take pictures
* [detector_node](pepper_pkg/src/detector_node/main.py)
    * Performs object detections on pictures taken 
* [head_node](pepper_pkg/src/head_node/main.py)
    * Makes Pepper move the head left and right
* [master_node](pepper_pkg/src/master_node/main.py)
    * Coordinates the camera node and the head node: the picture is taken only when the head is in the correct position
* [speaker_node](pepper_pkg/src/speaker_node/main.py)
    * Makes Pepper speak, saying what she sees around 

## Documentation

### Code

For futher information about the implementation, please refer to the in-code documentation. Every node is fully documentated in the related `main.py` file.

### Messages

The following messages are defined in the [msg](pepper_msgs/msg) folder.

#### DetectionArrayWithDirection

#### DetectionWithScore

#### ImageWithDirection

### Services

The following services are defined in the [srv](pepper_msgs/srv) folder.

#### LookAt

This service is served by the head node and is requested by the master node in order to make the head move to a specific angle.

* [head_node](pepper_pkg\src\head_node\main.py) is the node that makes the head move. Upon receiving a request, it will start the movement of the head and will send a `True` response only when the position is reached. 
* [master_node](pepper_pkg\src\master_node\main.py) is the master node that uses the service. Before taking a picture, the node must be sure that the head is in the right position, so it will check that the response is the one expected.


#### TakePicture

This service is served by the camera node and is requested by the master node in order to take a picture. Since the picture will be published on the topic, the requests take as parameter the current position of the head.

* [camera_node](pepper_pkg\src\camera_node\main.py) is the node that takes the picture and publish it on the topic. Upon receiving a request, it will take the picture, create an [ImageWithDirection](README.md#ImageWithDirection) message and will send a `True` response only if the operation is successful.
* [master_node](pepper_pkg\src\master_node\main.py) is the master node that uses the service. Before taking a picture, the node must be sure that the head is in the right position.

## Usage

One can simply run the software with

``` bash
roslaunch pepper_pkg pepper.launch
```
