# RaspTank-Smart-Robot

## Installation

1. Copy `robot.py`, `server.py` and `control.py` to the robots, the server and the control devices respectively.
2. Start the server : `python3 server.py`
3. `ssh` into the robots, change the robot's name (on line 12 of `robots.py`) and run the robot's script : `python3 robot.py`
4. On the controllers :
  - change the name of the robot to connect to on line 26
  - install dependency `pynput` with pip : `pip install pynput`
  - run the control script `python3 control.py`
  - Contol the robot with arrow keys, enter key to speed up and escape key to stop.
